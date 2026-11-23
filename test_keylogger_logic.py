"""Handler-level tests for Keylogger.py. No OS keyboard listener is started."""
import ast
import contextlib
import io
import os
from pathlib import Path
import tempfile
import types
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "Keylogger.py"

class FakeKey:
    enter = object()
    space = object()
    esc = object()
    backspace = object()


def make_handlers():
    # Extract only function definitions: do not execute the script's Listener.
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    funcs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    module = ast.fix_missing_locations(ast.Module(body=funcs, type_ignores=[]))
    namespace = {"Key": FakeKey, "lines": ""}
    exec(compile(module, str(SOURCE), "exec"), namespace)
    return namespace


class KeyloggerHandlerTests(unittest.TestCase):
    def setUp(self):
        self.ns = make_handlers()
        self.saved = []
        self.ns["write_file"] = self.saved.append
        self.console = io.StringIO()

    def press(self, key):
        with contextlib.redirect_stdout(self.console):
            self.ns["on_press"](key)

    def test_character_buffering(self):
        self.press(types.SimpleNamespace(char="H"))
        self.press(types.SimpleNamespace(char="i"))
        self.assertEqual(self.ns["lines"], "Hi")

    def test_space_buffering(self):
        self.press(types.SimpleNamespace(char="A"))
        self.press(FakeKey.space)
        self.press(types.SimpleNamespace(char="B"))
        self.assertEqual(self.ns["lines"], "A B")

    def test_enter_writes_and_resets_buffer(self):
        self.press(types.SimpleNamespace(char="x"))
        self.press(FakeKey.enter)
        self.assertEqual(self.saved, ["x"])
        self.assertEqual(self.ns["lines"], "")

    def test_no_file_write_before_enter(self):
        self.press(types.SimpleNamespace(char="x"))
        self.assertEqual(self.saved, [])

    def test_escape_release_stops_listener(self):
        self.assertIs(self.ns["on_release"](FakeKey.esc), False)

    def test_other_key_release_does_not_stop(self):
        self.assertIsNone(self.ns["on_release"](FakeKey.space))

    def test_backspace_is_not_applied_to_buffer(self):
        self.press(types.SimpleNamespace(char="x"))
        self.press(FakeKey.backspace)
        self.assertEqual(self.ns["lines"], "x")

    def test_console_prints_key_event(self):
        self.press(types.SimpleNamespace(char="z"))
        self.assertIn("char='z'", self.console.getvalue())

    def test_none_character_raises_typeerror(self):
        with self.assertRaises(TypeError):
            self.press(types.SimpleNamespace(char=None))


class FileOutputTests(unittest.TestCase):
    def test_write_file_appends_lines(self):
        ns = make_handlers()
        with tempfile.TemporaryDirectory() as tmp:
            old = os.getcwd()
            try:
                os.chdir(tmp)
                ns["write_file"]("alpha")
                ns["write_file"]("beta")
                self.assertEqual(Path("test_file.txt").read_text(), "alpha\nbeta\n")
            finally:
                os.chdir(old)

if __name__ == "__main__":
    unittest.main()
