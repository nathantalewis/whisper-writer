# macOS Compatibility Notes

## Current Status

WhisperWriter now runs fully on macOS!

### Required macOS Permissions

The application requires **Accessibility** permissions for Terminal to function:

1. Open **System Settings**
2. Go to **Privacy & Security** → **Accessibility**
3. Enable **Terminal.app** (or click + to add it)
4. Restart the application if it was already running

Without these permissions:

- Keyboard and Mouse shortcuts (ex. Ctrl+Shift+Space) will not work for starting/stopping recording
- Text output will fail with "osascript is not allowed to send keystrokes" error

## Fixes Applied

1. **evdev dependency**: Made Linux-only in requirements.txt

   ```
   evdev==1.7.1; sys_platform == 'linux'
   ```

2. **Keyboard compatibility**: Added conditional checks for Windows/Linux-specific keys in pynput_backend.py

## Development Notes

The pynput/Qt incompatibility appears to be fundamental:

- pynput uses Quartz Event Taps which require a run loop
- Qt uses its own event loop
- These two event loops conflict, causing native code crashes

The crash manifests as exit code 133 (SIGABRT), which cannot be caught by Python exception handlers.
