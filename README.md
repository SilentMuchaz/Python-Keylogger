# Python Keylogger — Keyboard Event Monitoring Lab

A Python lab exploring **keyboard event listeners, event handling, text buffering, and local file output** with the `pynput` library. I implemented a listener that processes character and special-key events, accumulates typed text, and appends the buffered text to a local file when Enter is pressed.

## Project at a glance

| Area | Implementation |
| --- | --- |
| Language and library | Python, `pynput.keyboard` |
| Input handling | `Listener` callbacks for key press and release events |
| Text processing | Accumulates character input and spaces in a buffer |
| File output | Appends a buffered line to `test_file.txt` when Enter is pressed |
| Stop condition | Releases Esc to stop the listener |
| Verification | 10 isolated handler-level tests using simulated events; no live keyboard monitoring during tests |

## Implementation and results

**Keyboard event processing.** The `on_press()` callback prints the received key event and adds ordinary characters to the `lines` buffer. Space is handled separately. Other special keys, including Backspace, are not represented in the saved text.

**Buffered local output.** Pressing Enter calls `write_file()`, which appends the current buffer and a newline to `test_file.txt`, then clears the buffer. The script does not continuously save every keystroke.

**Controlled exit.** The `on_release()` callback returns `False` when Esc is released, ending the listener.

```python
# Selected lines from Keylogger.py
if key == Key.enter:
    write_file(lines)
    lines = ""
elif hasattr(key, 'char'):
    lines += key.char
elif key == Key.space:
    lines += " "
```

### Verification evidence

I tested the **event-handling functions** using simulated key events, without activating the operating-system keyboard listener.

```text
Ran 10 tests

OK
```

The tests cover character input, spaces, Enter-triggered output, buffer reset, Esc termination, ignored special keys, append-mode file writing, console printing, and the existing `None`-character edge case.

- [Handler-level test suite](tests/test_keylogger_logic.py)
- [Recorded test results](evidence/handler-test-results.txt)
- [Technical case study](Keyboard-Event-Monitoring-Case-Study.md)
- [PDF case study](reports/01-keyboard-event-monitoring-case-study.pdf)

## Technical observations

| Input or event | Behavior in the current script |
| --- | --- |
| Character key | Added to the in-memory buffer |
| Space | Adds a space |
| Enter | Writes the buffer to `test_file.txt` and clears it |
| Esc released | Stops the listener |
| Backspace | Not reflected in the buffer |
| Character event with `char=None` | Can raise a `TypeError` |
| Esc before Enter | Unwritten buffered text is not saved |

## Scope and safe use

This is a **local, educational keyboard-event monitoring experiment**, not a production security tool. The original script has no network transmission or persistence mechanism, and its file output is unencrypted. It can capture sensitive information if used carelessly. Run it only on a system you own or are explicitly authorized to test, using non-sensitive test text.


