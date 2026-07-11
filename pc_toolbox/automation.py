import time
import threading
from pynput import keyboard, mouse
import pyautogui
import pyperclip

class GlobalHotkeyTracker:
    """
    Highly advanced dynamically rebindable always-on global hotkey system.
    Dynamically maps hotkey strings to action triggers.
    """
    def __init__(self, coord_cb, clicker_cb, macro_cb):
        self.coord_cb = coord_cb
        self.clicker_cb = clicker_cb
        self.macro_cb = macro_cb

        # Default rebindable hotkeys
        self.key_coord = "F9"
        self.key_clicker = "F10"
        self.key_macro = "F11"

        self.listener = None

    def update_keybinds(self, key_coord, key_clicker, key_macro):
        self.key_coord = key_coord.strip().upper()
        self.key_clicker = key_clicker.strip().upper()
        self.key_macro = key_macro.strip().upper()

    def _get_key_str(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                return key.char.upper()
            else:
                return str(key).replace("Key.", "").upper()
        except Exception:
            return ""

    def _on_press(self, key):
        try:
            key_str = self._get_key_str(key)
            if key_str == self.key_coord:
                m_controller = mouse.Controller()
                pos = m_controller.position
                self.coord_cb(pos[0], pos[1])
            elif key_str == self.key_clicker:
                self.clicker_cb()
            elif key_str == self.key_macro:
                self.macro_cb()
        except Exception:
            pass

    def start(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.daemon = True
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()


class AutoClicker:
    """
    Custom Auto-Clicker supporting custom click intervals,
    left/right clicks, and target coordinates.
    """
    def __init__(self):
        self.interval = 1.0
        self.button = "left"
        self.running = False
        self.thread = None

    def start(self, interval, button, coords=None):
        self.interval = interval
        self.button = button
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_clicker, args=(coords,), daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def _run_clicker(self, coords):
        while self.running:
            try:
                if coords:
                    pyautogui.click(x=coords[0], y=coords[1], button=self.button)
                else:
                    pyautogui.click(button=self.button)
            except Exception:
                pass
            time.sleep(self.interval)


class MacroRecorder:
    """
    Sequence recorder for mouse and keyboard actions.
    Uses pynput mouse/keyboard listeners to build macro sequence.
    """
    def __init__(self):
        self.sequence = []
        self.recording = False
        self.start_time = 0
        self._mouse_listener = None
        self._keyboard_listener = None

    def start_recording(self):
        self.sequence = []
        self.recording = True
        self.start_time = time.time()

        # Start pynput listeners
        self._mouse_listener = mouse.Listener(on_click=self._on_click)
        self._keyboard_listener = keyboard.Listener(on_press=self._on_press)

        self._mouse_listener.daemon = True
        self._keyboard_listener.daemon = True

        self._mouse_listener.start()
        self._keyboard_listener.start()

    def stop_recording(self):
        self.recording = False
        if self._mouse_listener:
            self._mouse_listener.stop()
        if self._keyboard_listener:
            self._keyboard_listener.stop()

    def clear(self):
        self.sequence = []

    def _on_click(self, x, y, button, pressed):
        if pressed and self.recording:
            elapsed = time.time() - self.start_time
            self.sequence.append({
                "type": "click",
                "x": x,
                "y": y,
                "button": button.name,
                "time": elapsed
            })

    def _on_press(self, key):
        if self.recording:
            elapsed = time.time() - self.start_time
            try:
                char = key.char
            except AttributeError:
                char = str(key)
            self.sequence.append({
                "type": "key",
                "key": char,
                "time": elapsed
            })

    def play(self):
        if not self.sequence:
            return

        # Play sequence in background thread
        thread = threading.Thread(target=self._run_playback, daemon=True)
        thread.start()

    def _run_playback(self):
        current_time = 0
        # Sort sequence by timestamp
        sorted_seq = sorted(self.sequence, key=lambda x: x["time"])
        for event in sorted_seq:
            delay = event["time"] - current_time
            if delay > 0:
                time.sleep(delay)
            current_time = event["time"]

            try:
                if event["type"] == "click":
                    pyautogui.click(x=event["x"], y=event["y"], button=event["button"])
                elif event["type"] == "key":
                    pyautogui.press(event["key"])
            except Exception:
                pass


class SmartClipboard:
    """
    Tracks and maintains a log of clipboard copying operations.
    """
    def __init__(self):
        self.history = []
        self._last_item = ""
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def _monitor(self):
        while self.running:
            try:
                current = pyperclip.paste()
                if current and current != self._last_item:
                    self._last_item = current
                    if current not in self.history:
                        self.history.append(current)
            except Exception:
                pass
            time.sleep(0.5)

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []
        self._last_item = ""

    def copy_item(self, text):
        try:
            pyperclip.copy(text)
            self._last_item = text
        except Exception:
            pass
