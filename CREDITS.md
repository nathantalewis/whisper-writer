# Credits and Attribution

This fork combines features from multiple whisper-writer forks to create an enhanced speech-to-text application with advanced pause/resume and voice command capabilities.

## Base Architecture

**dariox1337/whisper-writer** - Full rewrite with clean architecture
- Streaming transcription support
- VOSK backend integration
- Post-processing script system
- PyQt6 migration
- Improved error handling and debugging
- Audio saving for debugging purposes
- https://github.com/dariox1337/whisper-writer

## Planned Feature Ports

The following forks have features planned for integration:

### High Priority Features

**danobot/whisper-writer** - Continuous recording queue
- Audio recorded continuously and saved in temp files
- Queue-based processing for uninterrupted workflow
- Sequential transcription without blocking user input
- https://github.com/danobot/whisper-writer

**asapostolov/whisper-writer** - Transcription correction step
- Correction workflow after transcription
- Foundation for voice-based editing capabilities
- https://github.com/asapostolov/whisper-writer

**TomFrankly/whisper-writer** - LLM post-processing (16 stars - most popular maintained fork)
- Multi-provider LLM integration (OpenAI, Anthropic, Google, Groq, Ollama)
- LLM-based cleanup and instruction processing
- Advanced find & replace with regex
- Clipboard cleanup hotkey
- https://github.com/TomFrankly/whisper-writer

### Medium Priority Features

**danshapiro/whisper-writer** - Press hotkey twice to complete
- Manual control over recording completion
- Press activation key second time to stop before timeout
- https://github.com/danshapiro/whisper-writer

**thfrei/whisper-writer** - Press hotkey twice variant
- Alternative implementation of double-press completion
- https://github.com/thfrei/whisper-writer

**j-goodz/whisper-writer** - Gaming mode and reliability improvements
- Game detection mode for gaming scenarios
- Clipboard reliability fixes using Windows API
- In-app log viewer
- Intelligent gaming mode
- Windows native app experience
- Process enumeration and DPI scaling fixes
- https://github.com/j-goodz/whisper-writer

### Low Priority Features

**pshriwise/whisper-writer** - Socket control interface
- Control recording via socket connections
- External application integration capabilities
- https://github.com/pshriwise/whisper-writer

**R4ND3LL/whisper-writer** - Wake/sleep and plugin system
- Wake/sleep functionality with state management
- Plugin system for dynamic text processing
- Theme management and DPI scaling
- https://github.com/R4ND3LL/whisper-writer

## Other Notable Forks (Future Reference)

**Aarkan1/vibe-writer** (97 commits, 0 stars)
- Chat interface with history
- Clipboard prompting and inline popup
- Voice transcription in popup windows
- Markdown parsing in output
- Streaming API support
- https://github.com/Aarkan1/vibe-writer

**King-of-Infinite-Space/whisper-writer-fork** (79 commits, 0 stars)
- Clipboard pasting instead of typing
- Start minimized
- System tray integration improvements
- Better clipboard restore
- https://github.com/King-of-Infinite-Space/whisper-writer-fork

**seheepeak/whisper-writer** (66 commits, 0 stars)
- Voice activity indicator with animations
- Auto-launch scripts
- Status window with shadows
- Pulse bars and voice wave visualization
- Progress animation for transcription
- https://github.com/seheepeak/whisper-writer

**Alexis-benoist/whisper-writer**
- Wayland compatibility fixes
- https://github.com/Alexis-benoist/whisper-writer

**rkilchmn/whisper-writer**
- WSL whisper.cpp integration
- Remote API support
- https://github.com/rkilchmn/whisper-writer

**lksmoe/whisper-writer**
- whisper.cpp support
- https://github.com/lksmoe/whisper-writer

**wugui9/whisper-writer**
- Compact icon-only status display
- https://github.com/wugui9/whisper-writer

**waLLxAck/whisper-writer**
- Auto-copy functionality
- Transcription result dialog
- https://github.com/waLLxAck/whisper-writer

## Original Project

**savbell/whisper-writer** - Original whisper-writer project
- Foundation for all forks
- Initial implementation of local Whisper transcription
- System-wide hotkey integration
- https://github.com/savbell/whisper-writer

## New Features (nathantalewis/whisper-writer)

This fork adds the following novel features not found in any other fork:

- **Pause/Resume with Buffer Preservation**: True pause/resume functionality that maintains audio context across pause cycles, allowing you to speak about unrelated things during pause without capturing them
- **Voice-Based Editing Commands**: Hands-free correction of transcription errors using voice commands like "scratch that", "correct that", and "correct [word]"
- **Context-Aware Command Parsing**: Intelligent distinction between voice commands and dictation content
- **Enhanced Context Management**: Full sentence context preservation for accurate transcription when resuming

## License

All code in this repository, including ported features and original contributions, is licensed under the **GNU General Public License v3.0 (GPL-3.0)**, consistent with the original whisper-writer project and all contributing forks.

See the [LICENSE](LICENSE) file for full license text.

## Acknowledgments

Special thanks to:
- **OpenAI** for creating the Whisper model and providing the API
- **Guillaume Klein** for creating the faster-whisper Python package
- All contributors to the original whisper-writer project
- All fork maintainers whose work has contributed to this project
- The open-source community for making collaborative development possible
