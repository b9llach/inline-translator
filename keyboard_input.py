from PyQt6.QtCore import pyqtSignal, QObject
from pynput import keyboard

class KeyboardListener(QObject):
    key_pressed = pyqtSignal(str)
    toggle_pressed = pyqtSignal()
    capture_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        if key == keyboard.Key.f9:
            self.toggle_pressed.emit()
            return
        if key == keyboard.Key.f10:
            self.capture_pressed.emit()
            return
        try:
            self.key_pressed.emit(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.key_pressed.emit(' ')
            elif key == keyboard.Key.backspace:
                self.key_pressed.emit('backspace')