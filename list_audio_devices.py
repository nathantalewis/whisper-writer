import pyaudio


def list_audio_devices():
    p = pyaudio.PyAudio()

    print("Available audio devices:")
    print("------------------------")

    # Get the default input and output device indices
    default_input = p.get_default_input_device_info()['index']
    default_output = p.get_default_output_device_info()['index']

    # Iterate through all available audio devices
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)

        # Create a string to indicate if it's a default device
        default_str = ""
        if i == default_input:
            default_str = " (Default Input)"
        elif i == default_output:
            default_str = " (Default Output)"

        # Print device information
        print(f"Index {i}: {dev_info['name']}{default_str}")
        print(f"    Host API: {p.get_host_api_info_by_index(dev_info['hostApi'])['name']}")
        print(f"    Max Input Channels: {dev_info['maxInputChannels']}")
        print(f"    Max Output Channels: {dev_info['maxOutputChannels']}")
        print(f"    Default Sample Rate: {dev_info['defaultSampleRate']} Hz")
        print()

    p.terminate()


if __name__ == "__main__":
    list_audio_devices()
