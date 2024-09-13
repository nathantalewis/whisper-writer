import threading
import numpy as np
import pyaudio
import webrtcvad
import wave
import os
import datetime
from collections import namedtuple
from queue import Queue, Empty

from config_manager import ConfigManager
from event_bus import EventBus
from enums import RecordingMode, AudioManagerState
from profile import Profile

RecordingContext = namedtuple('RecordingContext', ['profile', 'session_id'])


class AudioManager:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.state = AudioManagerState.STOPPED
        self.recording_queue = Queue()
        self.thread = None
        self.pyaudio = pyaudio.PyAudio()
        self.debug_recording_dir = 'debug_audio'
        os.makedirs(self.debug_recording_dir, exist_ok=True)

    def start(self):
        if self.state == AudioManagerState.STOPPED:
            self.state = AudioManagerState.IDLE
            self.thread = threading.Thread(target=self._audio_thread)
            self.thread.start()

    def stop(self):
        if self.state != AudioManagerState.STOPPED:
            self.state = AudioManagerState.STOPPED
            self.recording_queue.put(None)  # Sentinel value to stop the thread
            if self.thread:
                self.thread.join(timeout=2)
                if self.thread.is_alive():
                    ConfigManager.log_print("Warning: Audio thread did not terminate gracefully.")
        self.pyaudio.terminate()

    def start_recording(self, profile: Profile, session_id: str):
        self.recording_queue.put(RecordingContext(profile, session_id))

    def stop_recording(self):
        self.recording_queue.put(None)  # Sentinel value to stop current recording

    def is_recording(self):
        return self.state == AudioManagerState.RECORDING

    def _audio_thread(self):
        while self.state != AudioManagerState.STOPPED:
            try:
                context = self.recording_queue.get(timeout=0.2)
                if context is None:
                    continue  # Skip this iteration, effectively stopping the current recording
                self.state = AudioManagerState.RECORDING
                self._record_audio(context)
                if self.state != AudioManagerState.STOPPED:
                    self.state = AudioManagerState.IDLE
            except Empty:
                continue

    def _record_audio(self, context: RecordingContext):
        recording = []
        recording_options = ConfigManager.get_section('recording_options', context.profile.name)
        sample_rate = recording_options.get('sample_rate', 16000)
        gain = recording_options.get('gain', 1.0)
        channels = 1
        streaming_chunk_size = context.profile.streaming_chunk_size or 4096

        frame_size = self._calculate_frame_size(sample_rate, streaming_chunk_size,
                                                context.profile.is_streaming)
        frame_duration_ms = int(frame_size / sample_rate * 1000)
        silence_duration_ms = recording_options.get('silence_duration', 900)
        silence_frames = int(silence_duration_ms / frame_duration_ms)
        recording_mode = RecordingMode[recording_options.get('recording_mode', 'PRESS_TO_TOGGLE')
                                       .upper()]

        vad = None
        if recording_mode in (RecordingMode.VOICE_ACTIVITY_DETECTION, RecordingMode.CONTINUOUS):
            vad = webrtcvad.Vad(2)
        # Skip running vad for the first 0.15 seconds to avoid mistaking keyboard noise for voice
        initial_frames_to_skip = int(0.15 * sample_rate / frame_size)
        speech_detected = False
        silent_frame_count = 0

        sound_device = self._get_sound_device(recording_options.get('sound_device'))
        stream = self.pyaudio.open(format=pyaudio.paFloat32,
                                   channels=channels,
                                   rate=sample_rate,
                                   input=True,
                                   input_device_index=sound_device,
                                   frames_per_buffer=frame_size)

        save_debug_audio = recording_options.get('save_debug_audio', False)

        debug_wav_file = None
        if save_debug_audio:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{context.profile.name}_{timestamp}.wav"
            debug_wav_file = wave.open(os.path.join(self.debug_recording_dir, filename), 'wb')
            debug_wav_file.setnchannels(channels)
            debug_wav_file.setsampwidth(2)  # 16-bit audio
            debug_wav_file.setframerate(sample_rate)

        try:
            while self.state != AudioManagerState.STOPPED and self.recording_queue.empty():
                frame = stream.read(frame_size)
                frame_array = self._process_audio_frame(frame, gain)
                recording.extend(frame_array)

                if save_debug_audio:
                    # Convert float32 to int16 for WAV file
                    int16_frame = (frame_array * 32767).astype(np.int16)
                    debug_wav_file.writeframes(int16_frame.tobytes())

                if context.profile.is_streaming and len(recording) >= streaming_chunk_size:
                    arr = np.array(recording[:streaming_chunk_size], dtype=np.float32)
                    self._push_audio_chunk(context, arr, sample_rate, channels)
                    recording = recording[streaming_chunk_size:]

                if vad:
                    if initial_frames_to_skip > 0:
                        initial_frames_to_skip -= 1
                        continue
                    # Convert to int16 for VAD
                    int16_frame = (frame_array * 32767).astype(np.int16)
                    if vad.is_speech(int16_frame.tobytes(), sample_rate):
                        silent_frame_count = 0
                        if not speech_detected:
                            ConfigManager.log_print("Speech detected.")
                            speech_detected = True
                    else:
                        silent_frame_count += 1

                    if speech_detected and silent_frame_count > silence_frames:
                        break

        finally:
            stream.stop_stream()
            stream.close()
            if debug_wav_file:
                debug_wav_file.close()

        if not context.profile.is_streaming:
            audio_data = np.array(recording, dtype=np.float32)
            duration = len(audio_data) / sample_rate

            ConfigManager.log_print(f'Recording finished. Size: {audio_data.size} samples, '
                                    f'Duration: {duration:.2f} seconds')

            min_duration_ms = recording_options.get('min_duration', 200)

            if vad and not speech_detected:
                ConfigManager.log_print('Discarded because no speech has been detected.')
                self.event_bus.emit("audio_discarded", context.session_id)
            elif (duration * 1000) >= min_duration_ms:
                self._push_audio_chunk(context, audio_data, sample_rate, channels)
            else:
                ConfigManager.log_print('Discarded due to being too short.')
                self.event_bus.emit("audio_discarded", context.session_id)

        context.profile.audio_queue.put(None)  # Push sentinel value

        # Notify ApplicationController of automatic termination due to silence detected by vad
        if vad and self.state != AudioManagerState.STOPPED:
            self.event_bus.emit("recording_stopped", context.session_id)

    def _calculate_frame_size(self, sample_rate: int, streaming_chunk_size: int,
                              is_streaming: bool) -> int:
        if is_streaming:
            valid_frame_durations = [10, 20, 30]  # in milliseconds, accepted by webrtcvad
            for duration in sorted(valid_frame_durations, reverse=True):
                frame_size = int(sample_rate * (duration / 1000.0))
                if streaming_chunk_size % frame_size == 0:
                    return frame_size
            return int(sample_rate * 0.01)  # default to 10ms if no perfect divisor found
        else:
            return int(sample_rate * 0.03)  # 30ms for non-streaming

    def _get_sound_device(self, device):
        if device == '' or device is None:
            return None
        try:
            return int(device)
        except ValueError:
            ConfigManager.log_print(f"Invalid device index: {device}. Using default.")
            return None

    def _process_audio_frame(self, frame: bytes, gain: float) -> np.ndarray:
        frame_array = np.frombuffer(frame, dtype=np.float32).copy()
        frame_array *= gain
        np.clip(frame_array, -1.0, 1.0, out=frame_array)
        return frame_array

    def _push_audio_chunk(self, context: RecordingContext, audio_data: np.ndarray,
                          sample_rate: int, channels: int):
        context.profile.audio_queue.put({
            'session_id': context.session_id,
            'sample_rate': sample_rate,
            'channels': channels,
            'language': 'auto',
            'audio_chunk': audio_data
        })

    def cleanup(self):
        self.stop()
        self.thread = None
        self.pyaudio = None
        self.recording_queue = None
