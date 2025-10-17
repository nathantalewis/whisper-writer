# WhisperWriter Forks Analysis - Complete Context for Development

**Date:** January 16, 2025
**Total Forks Analyzed:** 137
**Forks with Unique Commits:** 47
**Your Fork:** https://github.com/nathantalewis/whisper-writer (forked from dariox1337/whisper-writer)

---

## Original Requirements - Use Case Example

You need a speech-to-text tool with two critical features that NO existing fork has:

### 1. Pause/Resume Recording with Context Preservation

**Example scenario:**
- You start recording: "The widget should be..."
- You pause mid-thought to:
  - Think through your idea
  - Talk to a colleague who walked by
  - Answer a question from someone else
  - Have an unrelated conversation
- You resume and continue: "...round too"
- The entire phrase "The widget should be round too" is sent to Whisper as a single transcription

**Why this matters:** Without context, Whisper might transcribe "round too" as "round 2" because it lacks the beginning of the sentence. You need to be able to actively speak about unrelated things during your pause without those words being captured.

**Why longer silence detection doesn't work:** Standard tools just use extended silence detection, but you need to actively speak about unrelated things during your pause without those words being captured in your recording.

### 2. Voice-Based Editing/Correction

After transcription, you need to fix mistakes using voice commands rather than typing or mouse interaction:

- "Correct that" - to fix the last word/phrase
- "Correct [specific word]" - to fix a particular word anywhere in the text
- "Scratch that" - to delete the last phrase
- Voice commands to select, replace, or modify transcribed text

**Why this matters:** Errors like "round 2" → "round too" are common when context is lost, and you want to fix them hands-free by voice rather than switching to keyboard/mouse.

### Additional Preferences

- Works with VSCode or any application (system-wide dictation)
- Uses OpenAI Whisper model (local preferred for privacy/cost)
- Cross-platform support (Windows/Linux/Mac) preferred
- No subscription fees - either free/open source or one-time purchase
- Preferably something you can build/customize yourself if needed

### Deal Breakers

- Subscription-based pricing (even at reasonable rates)
- Cloud-only solutions requiring constant internet
- Tools that force you to stay completely silent during pauses
- Tools that don't allow voice-based correction of transcription errors

---

## Critical Finding

**NONE of the 47 active forks implement either of your core requirements.**

However, several forks have features that could serve as a foundation.

---

## Most Notable Forks

### 1. **Aarkan1/vibe-writer** (97 commits, 0 stars)
**Best overall fork for extended functionality**

- **Unique Features:**
  - Chat interface with history
  - Clipboard prompting and inline popup prompt
  - Voice transcription in popup windows
  - Markdown parsing in output
  - Streaming API support

- **Why it's interesting:** Has the most advanced UI work, showing significant development effort
- **Missing:** Still no pause/resume or voice commands
- **Link:** https://github.com/Aarkan1/vibe-writer

### 2. **dariox1337/whisper-writer** (84 commits, 11 stars)
**Most comprehensive rewrite - THIS IS YOUR BASE**

- **Unique Features:**
  - Full rewrite with streaming transcription
  - VOSK support
  - Post-processing via separate scripts
  - PyQt6 migration
  - Better error handling
  - Saves audio for debugging

- **Why it's interesting:** Clean architecture, well-documented, multiple backends
- **Why chosen as base:** Best foundation for building new features
- **Missing:** No pause/resume or voice commands
- **Link:** https://github.com/dariox1337/whisper-writer

### 3. **King-of-Infinite-Space/whisper-writer-fork** (79 commits, 0 stars)
**Two major custom branches**

- **Unique Features:**
  - Clipboard pasting instead of typing
  - Start minimized
  - System tray integration
  - Better clipboard restore

- **Why it's interesting:** Combines dariox1337's rewrite with custom features
- **Missing:** No pause/resume or voice commands
- **Link:** https://github.com/King-of-Infinite-Space/whisper-writer-fork

### 4. **seheepeak/whisper-writer** (66 commits, 0 stars)
**Korean code-switching focus with advanced UI**

- **Unique Features:**
  - Voice activity indicator with animations
  - Auto-launch scripts
  - Fancy status window with shadows
  - Pulse bars and voice wave visualization
  - Progress animation for transcription

- **Why it's interesting:** Most advanced UI/UX work, shows what's possible
- **Missing:** No pause/resume or voice commands (focused on Korean language)
- **Link:** https://github.com/seheepeak/whisper-writer

### 5. **j-goodz/whisper-writer** (52 commits, 0 stars)
**Gaming mode and reliability focus**

- **Unique Features:**
  - Game detection mode
  - Clipboard reliability fixes
  - In-app log viewer
  - Intelligent gaming mode
  - Windows native app experience

- **Why it's interesting:** Focus on reliability and edge cases
- **Missing:** No pause/resume or voice commands
- **Link:** https://github.com/j-goodz/whisper-writer

---

## Features to Port - Priority Order

### HIGH PRIORITY - Core Functionality

#### 1. Continuous Recording Queue (from danobot/whisper-writer)
- **Link:** https://github.com/danobot/whisper-writer
- **Feature:** Audio recorded continuously, saved in temp files, added to queue and processed sequentially so user's train of thought isn't interrupted
- **Relevance:** **This is the closest to your pause/resume requirement!** It maintains continuity without interrupting the user.
- **Commit reference:** See line 846 in whisper-writer-forks-analysis-all-branches.md
- **Implementation approach:**
  - Enhance the queueing system to allow manual pause/resume
  - Add buffer preservation across pause cycles
  - Allow voice to be spoken during pause without capturing it

#### 2. Transcription Correction Step (from asapostolov/whisper-writer)
- **Link:** https://github.com/asapostolov/whisper-writer
- **Feature:** Added a step for correction of the transcription
- **Relevance:** **Closest to voice-based editing!** Though unclear if it's voice-based.
- **Commit reference:** See line 710 in whisper-writer-forks-analysis-all-branches.md
- **Implementation approach:**
  - Examine their correction mechanism
  - Enhance with voice command detection if not already present
  - Add commands: "scratch that", "correct that", "correct [word]"

#### 3. LLM Post-Processing (from TomFrankly/whisper-writer)
- **Link:** https://github.com/TomFrankly/whisper-writer (16 stars - most popular maintained fork)
- **Features:**
  - LLM cleanup and instruction processing
  - Multiple providers (OpenAI, Anthropic, Google, Groq, local Ollama)
  - Advanced find & replace with regex
  - Clipboard cleanup hotkey
- **Relevance:** Can help with post-correction and enhancement
- **Implementation approach:**
  - Port LLM integration layer
  - Use for intelligent error correction
  - Could power voice command interpretation

### MEDIUM PRIORITY - Reliability & UX

#### 4. Press Hotkey Twice to Complete (from danshapiro/whisper-writer, thfrei/whisper-writer)
- **Links:**
  - https://github.com/danshapiro/whisper-writer (line 1008)
  - https://github.com/thfrei/whisper-writer
- **Feature:** Press the hotkey a 2nd time to complete recording before the timeout
- **Relevance:** Manual pause/resume control mechanism
- **Implementation approach:**
  - Simple toggle mechanism for pause/resume
  - Could be combined with continuous queue feature

#### 5. Clipboard & Gaming Mode Reliability (from j-goodz/whisper-writer)
- **Link:** https://github.com/j-goodz/whisper-writer
- **Features:**
  - Clipboard paste robustness (Windows API verify/restore)
  - Gaming mode detection
  - Process enumeration fixes
  - DPI scaling fixes for multi-monitor
- **Relevance:** Production-quality reliability
- **Implementation approach:**
  - Port clipboard improvements
  - May be useful if building game-like pause/resume UX

### LOW PRIORITY - Nice to Have

#### 6. Socket Control (from pshriwise/whisper-writer)
- **Link:** https://github.com/pshriwise/whisper-writer
- **Feature:** Control recording via socket
- **Relevance:** Could enable external pause/resume control (e.g., from other apps)
- **Implementation approach:** Add API for external control

#### 7. Wake/Sleep & Plugin System (from R4ND3LL/whisper-writer)
- **Link:** https://github.com/R4ND3LL/whisper-writer
- **Features:**
  - Wake/sleep functionality with state management
  - Plugin system for dynamic text processing
  - Theme management and DPI scaling
- **Relevance:** Nice architectural patterns
- **Implementation approach:** Consider for v2.0

---

## Implementation Plan - Hybrid Approach

### Phase 0: Setup ✅
1. ✅ Fork dariox1337/whisper-writer to nathantalewis/whisper-writer
2. Clone locally to your development machine
3. Create a `CREDITS.md` file documenting all sources
4. Update README with hybrid approach explanation

### Phase 1: Foundation Work
1. **Understand the base architecture** (dariox1337)
   - Read through the design doc
   - Understand AudioManager, TranscriptionManager, EventBus
   - Map out the post-processing script system

2. **Create feature branches**
   - `feature/continuous-queue` - Port danobot's queue
   - `feature/correction-step` - Port asapostolov's correction
   - `feature/llm-integration` - Port TomFrankly's LLM features
   - `feature/pause-resume` - NEW: Your pause/resume implementation
   - `feature/voice-commands` - NEW: Your voice command detection

### Phase 2: Port Existing Features
1. **Port continuous queue from danobot** (Priority 1)
   - Fetch danobot's branch: `git fetch https://github.com/danobot/whisper-writer feat/improve-continuous-recording`
   - Examine the implementation
   - Adapt to dariox's architecture
   - Test recording continuity

2. **Port correction step from asapostolov** (Priority 2)
   - Fetch: `git fetch https://github.com/asapostolov/whisper-writer main`
   - Find the correction step implementation
   - Integrate with TranscriptionManager
   - Test correction workflow

3. **Port LLM features from TomFrankly** (Priority 3)
   - Fetch: `git fetch https://github.com/TomFrankly/whisper-writer main`
   - Port LLM provider abstraction
   - Port cleanup and instruction modes
   - Port regex find/replace if not in base
   - Test with local Ollama and OpenAI

### Phase 3: Implement New Features
1. **Implement pause/resume with buffer preservation**
   - Modify AudioManager to support paused state
   - Create audio buffer that persists across pause cycles
   - Add hotkey for pause (doesn't stop recording, just marks position)
   - Add hotkey for resume (continues from mark)
   - Add hotkey for complete (sends entire buffer to transcription)
   - Ensure audio during pause is discarded, not captured

2. **Implement voice command detection**
   - Create VoiceCommandParser class
   - Add command detection layer after transcription
   - Implement commands:
     - "scratch that" - delete last phrase
     - "correct that" - re-transcribe last phrase with context
     - "correct [word]" - find and correct specific word
     - "undo" - undo last action
   - Integrate with correction step mechanism
   - Use LLM for intelligent command interpretation

### Phase 4: Testing & Polish
1. Test pause/resume with various scenarios
2. Test voice commands in real-world usage
3. Test cross-platform compatibility
4. Add documentation
5. Create demo videos

### Phase 5: Documentation
1. **Update README.md** with:
   - Hybrid approach explanation
   - Features from each fork
   - New features added
   - Installation instructions
   - Usage examples for pause/resume
   - Usage examples for voice commands

2. **Create CREDITS.md** with:
   ```markdown
   # Credits and Attribution

   This fork combines features from multiple whisper-writer forks:

   ## Base Architecture
   - **dariox1337/whisper-writer** - Full rewrite with clean architecture
     - Streaming transcription, VOSK support, post-processing scripts
     - PyQt6 migration, better error handling
     - https://github.com/dariox1337/whisper-writer

   ## Ported Features
   - **danobot/whisper-writer** - Continuous recording queue
     - Audio queuing system for uninterrupted workflow
     - https://github.com/danobot/whisper-writer

   - **asapostolov/whisper-writer** - Transcription correction step
     - Correction workflow integration
     - https://github.com/asapostolov/whisper-writer

   - **TomFrankly/whisper-writer** - LLM post-processing
     - Multi-provider LLM integration (OpenAI, Anthropic, Google, Groq, Ollama)
     - Advanced find/replace with regex
     - https://github.com/TomFrankly/whisper-writer

   ## Original Project
   - **savbell/whisper-writer** - Original whisper-writer project
     - https://github.com/savbell/whisper-writer

   ## New Features (nathantalewis)
   - Pause/resume recording with buffer preservation
   - Voice-based editing commands ("scratch that", "correct word", etc.)
   - Context-aware command parsing
   ```

---

## Features Still Missing Everywhere

These features exist in **NO fork** - you'll implement them:
1. ❌ True pause/resume with buffer preservation (danobot has queuing, but not true pause/resume)
2. ❌ Voice-based editing commands ("scratch that", "correct word")
3. ❌ Context-aware command parsing (distinguishing commands from dictation)

---

## Other Noteworthy Forks (For Future Reference)

### Recording Improvements
- **R4ND3LL/whisper-writer**: Wake/sleep functionality, plugin system for text processing
- **thfrei/whisper-writer**: Parallel processing, continuous batching

### UI/UX
- **wugui9/whisper-writer**: Compact icon-only status display
- **waLLxAck/whisper-writer**: Auto-copy and transcription result dialog

### Platform-Specific
- **Alexis-benoist/whisper-writer**: Wayland fixes
- **rkilchmn/whisper-writer**: WSL whisper.cpp integration, remote API support
- **lksmoe/whisper-writer**: whisper.cpp support

---

## Architecture Notes (dariox1337 base)

From their design doc, the key components are:

1. **AudioManager** - Handles recording with PyAudio polling
2. **TranscriptionManager** - Manages transcription backends (Faster Whisper, VOSK, OpenAI API)
3. **EventBus** - Main thread event coordination
4. **Post-processing scripts** - Extensible script system for text manipulation
5. **PyQt6 UI** - Settings window and status window

Your modifications will primarily touch:
- **AudioManager** - Add pause/resume state and buffer management
- **TranscriptionManager** - Add correction step integration
- **New: VoiceCommandParser** - Parse transcription for voice commands
- **New: LLMProvider** - Abstract LLM integration (from TomFrankly)

---

## Files Generated During Analysis

1. `whisper-writer-forks.txt` - Raw list of all 137 forks
2. `whisper-writer-forks-analysis.md` - Full analysis (main branch only, 33 forks)
3. `whisper-writer-forks-analysis-all-branches.md` - Complete analysis (all branches, 47 forks)
4. `whisper-writer-forks-summary.md` - This file

---

## Next Steps

1. Clone your fork: `git clone https://github.com/nathantalewis/whisper-writer`
2. Set up development environment (Python 3.12, PyQt6, etc.)
3. Read dariox1337's architecture docs
4. Start with Phase 1: Understanding the base
5. Create feature branches for each port
6. Begin implementation following the phases above

---

## Questions to Investigate

1. How does asapostolov's correction step work? Is it voice-based or manual?
2. Can danobot's queue be adapted to buffer audio without processing?
3. How to distinguish voice commands from dictation? (LLM? keyword detection? separate hotkey?)
4. Best way to handle "pause" vs "complete" - separate hotkeys or press twice?
5. How to handle context window for Whisper during resume?

---

## Success Criteria

Your fork will be successful when:
- ✅ You can start recording, pause (while speaking to someone), resume, and complete with full context preserved
- ✅ You can say "scratch that" and the last phrase is deleted
- ✅ You can say "correct [word]" and the word is corrected using context
- ✅ Works locally with Whisper (no required cloud services)
- ✅ Works system-wide with any application
- ✅ Proper attribution given to all source forks
