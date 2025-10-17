# WhisperWriter Hybrid Fork - Development Roadmap

This document tracks planned features to be ported from other forks and new features to be developed.

## Phase 1: Foundation Work

- [x] Fork dariox1337/whisper-writer
- [x] Clone locally
- [x] Check licenses for compatibility
- [x] Create CREDITS.md
- [ ] Update README.md to reflect fork status
- [ ] Understand base architecture (AudioManager, TranscriptionManager, EventBus)
- [ ] Map out post-processing script system

## Phase 2: Port Existing Features

### High Priority

#### 1. Continuous Recording Queue (from danobot/whisper-writer)
- [ ] Fetch danobot's branch: `git fetch https://github.com/danobot/whisper-writer feat/improve-continuous-recording`
- [ ] Examine queue implementation
- [ ] Adapt to dariox's architecture
- [ ] Test recording continuity
- [ ] Document changes

**Why**: Closest to pause/resume requirement - maintains continuity without interrupting user

#### 2. Transcription Correction Step (from asapostolov/whisper-writer)
- [ ] Fetch: `git fetch https://github.com/asapostolov/whisper-writer main`
- [ ] Find correction step implementation
- [ ] Integrate with TranscriptionManager
- [ ] Test correction workflow
- [ ] Document changes

**Why**: Foundation for voice-based editing capabilities

#### 3. LLM Post-Processing (from TomFrankly/whisper-writer)
- [ ] Fetch: `git fetch https://github.com/TomFrankly/whisper-writer main`
- [ ] Port LLM provider abstraction
- [ ] Port cleanup and instruction modes
- [ ] Port regex find/replace (if not in base)
- [ ] Test with local Ollama
- [ ] Test with OpenAI API
- [ ] Document changes

**Why**: Enables intelligent error correction and command interpretation

### Medium Priority

#### 4. Press Hotkey Twice to Complete (from danshapiro/whisper-writer or thfrei/whisper-writer)
- [ ] Examine both implementations
- [ ] Choose best approach
- [ ] Integrate toggle mechanism
- [ ] Test with continuous queue feature
- [ ] Document changes

**Why**: Manual pause/resume control mechanism

#### 5. Clipboard & Gaming Mode Reliability (from j-goodz/whisper-writer)
- [ ] Port clipboard improvements (Windows API verify/restore)
- [ ] Port gaming mode detection
- [ ] Port process enumeration fixes
- [ ] Port DPI scaling fixes
- [ ] Test cross-platform
- [ ] Document changes

**Why**: Production-quality reliability

### Low Priority

#### 6. Socket Control (from pshriwise/whisper-writer)
- [ ] Examine socket control implementation
- [ ] Design API for external control
- [ ] Implement basic socket interface
- [ ] Test with external app
- [ ] Document API

**Why**: Enable external pause/resume control

#### 7. Wake/Sleep & Plugin System (from R4ND3LL/whisper-writer)
- [ ] Study plugin architecture
- [ ] Consider for v2.0 design
- [ ] Document patterns for future use

**Why**: Good architectural patterns for extensibility

## Phase 3: Implement New Features

### 1. Pause/Resume with Buffer Preservation
- [ ] Design pause/resume state machine
- [ ] Modify AudioManager to support paused state
- [ ] Create audio buffer that persists across pause cycles
- [ ] Add hotkey for pause (marks position without stopping recording)
- [ ] Add hotkey for resume (continues from mark)
- [ ] Add hotkey for complete (sends entire buffer to transcription)
- [ ] Ensure audio during pause is discarded, not captured
- [ ] Test with various pause/resume scenarios
- [ ] Document usage

**Goal**: Start recording "The widget should be...", pause while having unrelated conversation, resume "...round too", get full context "The widget should be round too"

### 2. Voice Command Detection
- [ ] Create VoiceCommandParser class
- [ ] Add command detection layer after transcription
- [ ] Implement "scratch that" - delete last phrase
- [ ] Implement "correct that" - re-transcribe last phrase with context
- [ ] Implement "correct [word]" - find and correct specific word
- [ ] Implement "undo" - undo last action
- [ ] Integrate with correction step mechanism
- [ ] Use LLM for intelligent command interpretation
- [ ] Test command detection accuracy
- [ ] Document supported commands

**Goal**: Fix errors like "round 2" → "round too" hands-free by voice

## Phase 4: Testing & Polish

- [ ] Test pause/resume with real-world scenarios
- [ ] Test voice commands in daily usage
- [ ] Test cross-platform (Mac/Linux/Windows if available)
- [ ] Performance testing and optimization
- [ ] Create user documentation
- [ ] Create demo videos
- [ ] Update README with new features

## Phase 5: Documentation & Release

- [ ] Update README.md with implemented features
- [ ] Document installation for new dependencies
- [ ] Create usage examples for pause/resume
- [ ] Create usage examples for voice commands
- [ ] Document configuration options
- [ ] Create CHANGELOG.md
- [ ] Tag first release

## Success Criteria

- ✅ Can start recording, pause (while speaking to someone), resume, and complete with full context preserved
- ✅ Can say "scratch that" and last phrase is deleted
- ✅ Can say "correct [word]" and word is corrected using context
- ✅ Works locally with Whisper (no required cloud services)
- ✅ Works system-wide with any application
- ✅ Proper attribution given to all source forks

## Questions to Investigate

1. How does asapostolov's correction step work? Is it voice-based or manual?
2. Can danobot's queue be adapted to buffer audio without processing?
3. How to distinguish voice commands from dictation? (LLM? keyword detection? separate hotkey?)
4. Best way to handle "pause" vs "complete" - separate hotkeys or press twice?
5. How to handle context window for Whisper during resume?

## Notes

- All ported code must maintain GPL-3.0 license compatibility
- Document all changes with commit references
- Keep CREDITS.md updated as features are ported
- Test each feature independently before moving to next
