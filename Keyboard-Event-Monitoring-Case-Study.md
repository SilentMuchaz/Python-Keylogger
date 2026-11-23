# Keyboard Event Monitoring — Technical Case Study

## Project objective

I built a Python keyboard-event monitoring experiment to practice event-driven programming, keyboard listener callbacks, text buffering, and local file I/O. The project uses `pynput.keyboard.Listener` to process key press and release events.

## Implementation

**Listener setup:** The program registers `on_press` and `on_release` callbacks with `Listener` and waits for the listener to exit.

**Event processing:** `on_press` prints each key event to the console. Ordinary character keys are appended to a global `lines` buffer; a space event adds a literal space.

**File output:** When Enter is pressed, `write_file` opens `test_file.txt` in append mode, writes the buffered text plus a newline, and clears the buffer. The file is only written when Enter is received.

**Termination:** When Esc is released, `on_release` returns `False`, which stops the listener.

## Implementation evidence

| Source element | Demonstrated behavior |
| --- | --- |
| `Listener(on_press=..., on_release=...)` | Registers keyboard event callbacks |
| `lines += key.char` | Buffers ordinary character input |
| `lines += " "` | Handles the space key |
| `write_file(lines)` | Writes buffered text at Enter |
| `open("test_file.txt", "a")` | Uses append-mode local file output |
| `if key == Key.esc: return False` | Stops on Esc release |

## Handler-level verification

To test the event-processing logic without collecting live keyboard input, I extracted the existing function definitions from `Keylogger.py` and exercised them using simulated key events. The tests do **not** start `pynput.Listener`.

**Result:** 10 handler-level tests passed. The suite verifies ordinary characters, spaces, Enter-triggered writes and reset, Esc behavior, handling of unsupported special keys, local file append mode, console printing, and the known `char=None` edge case.

Supporting artifacts:
- [`tests/test_keylogger_logic.py`](test_keylogger_logic.py)
- [`evidence/handler-test-results.txt`](evidence/handler-test-results.txt)

## Findings and implementation limits

- The script records buffered lines only after Enter, not every key event to disk.
- Backspace and other editing keys are not applied to the buffer, so saved text may not match what was typed after corrections.
- Some character events with `char=None` can raise a `TypeError`.
- Text not followed by Enter is not flushed when Esc ends the session.
- Key events are printed to the console; the script is not silent.
- Local text output is not encrypted. The source contains no network exfiltration or startup persistence.

## Outcome

The project demonstrates basic Python event-driven programming and file handling through a working implementation of keyboard callbacks. Isolated function-level tests confirm the documented handler logic. Live listener behavior and operating-system permissions were not evaluated in this test run.

## Responsible-use boundary

This project is for consent-based learning in a controlled environment. Do not use it to monitor other people's input or record passwords, personal messages, or other sensitive information.
