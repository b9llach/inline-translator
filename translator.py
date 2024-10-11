import time
import threading
from PyQt6.QtCore import QObject, QTimer, QRect, Qt
from PyQt6.QtWidgets import QApplication
from deep_translator import GoogleTranslator
import pyautogui
import pyperclip
from gtts import gTTS
import os
from playsound import playsound
import tempfile
import win32gui
import ctypes
from ctypes import wintypes
from PIL import Image
from keyboard_input import KeyboardListener
from gui import TranslatorGUI
import requests
from PIL import ImageGrab
from screen_capture import ScreenCaptureWidget
import io
from dotenv import load_dotenv
load_dotenv()

is_typing = False
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3)
    ]

class Translator(QObject):
    def __init__(self):
        super().__init__()
        self.buffer = ""
        self.last_translated = ""
        self.translating = False
        self.is_typing_translation = False
        self.target_language = 'it' 
        self.translator = GoogleTranslator(source='auto', target=self.target_language)
        self.gui = TranslatorGUI()
        self.gui.toggle_signal.connect(self.set_translating)
        self.gui.language_signal.connect(self.set_language)
        self.gui.translate_signal.connect(self.translate_text)
        self.gui.capture_signal.connect(self.capture_and_translate)
        self.gui.show()

        self.keyboard_listener = KeyboardListener()
        self.keyboard_listener.key_pressed.connect(self.on_key_event)
        self.keyboard_listener.toggle_pressed.connect(self.toggle_translation)
        self.keyboard_listener.capture_pressed.connect(self.capture_and_translate)

        self.translation_timer = QTimer(self)
        self.translation_timer.timeout.connect(self.delayed_translate)
        self.translation_timer.setSingleShot(True)

        self.last_key_time = time.time()

        self.temp_dir = tempfile.mkdtemp()
        self.on_file = os.path.join(self.temp_dir, "on.mp3")
        self.off_file = os.path.join(self.temp_dir, "off.mp3")

        gTTS("Translation on").save(self.on_file)
        gTTS("Translation off").save(self.off_file)

        self.screen_capture_widget = None
        
        self.language_codes = {
            'arabic': 'ar',
            'bulgarian': 'bg',
            'chinese (simplified)': 'zh-CN',
            'chinese (traditional)': 'zh-TW',
            'croatian': 'hr',
            'danish': 'da',
            'dutch': 'nl',
            'english': 'en',
            'finnish': 'fi',
            'french': 'fr',
            'german': 'de',
            'greek': 'el',
            'hungarian': 'hu',
            'italian': 'it',
            'japanese': 'ja',
            'korean': 'ko',
            'norwegian': 'no',
            'polish': 'pl',
            'portuguese': 'pt',
            'russian': 'ru',
            'spanish': 'es',
            'slovenian': 'sl',
            'swedish': 'sv',
            'turkish': 'tr'
        }

        self.ocr_language_codes = {
            'arabic': 'ara',
            'bulgarian': 'bul',
            'chinese (simplified)': 'chs',
            'chinese (traditional)': 'cht',
            'croatian': 'hrv',
            'danish': 'dan',
            'dutch': 'dut',
            'english': 'eng',
            'finnish': 'fin',
            'french': 'fre',
            'german': 'ger',
            'greek': 'gre',
            'hungarian': 'hun',
            'italian': 'ita',
            'japanese': 'jpn',
            'korean': 'kor',
            'norwegian': 'nor',
            'polish': 'pol',
            'portuguese': 'por',
            'russian': 'rus',
            'spanish': 'spa',
            'slovenian': 'slv',
            'swedish': 'swe',
            'turkish': 'tur'
        }

    def set_translating(self, state):
        self.translating = state

    def set_language(self, language_code):
        self.target_language = language_code
        self.translator = GoogleTranslator(source='auto', target=self.target_language)

    def on_key_event(self, key):
        global is_typing
        if not self.translating or self.is_typing_translation:
            return

        current_time = time.time()
        if current_time - self.last_key_time > 2:
            self.buffer = ""  
        self.last_key_time = current_time

        if key == 'backspace':
            if self.buffer and not is_typing:
                self.buffer = self.buffer[:-1]
        elif key == ' ':
            if not is_typing:
                self.buffer += ' '
        elif len(key) == 1: 
            if not is_typing:
                self.buffer += key

        self.translation_timer.stop()
        self.translation_timer.start(1250) 

    def delayed_translate(self):
        if self.buffer.strip() and self.buffer.strip() != self.last_translated:
            self.translate_buffer()

    def translate_buffer(self):
        global is_typing
        if not self.buffer.strip():
            return

        try:
            original_text = self.buffer.strip()
            translated = self.translator.translate(original_text)

            if original_text.isupper():
                translated = translated.upper()
            elif not original_text[0].isupper():
                translated = translated[0].lower() + translated[1:]
            
            if translated != self.last_translated:
                self.is_typing_translation = True

                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                time.sleep(0.05)

                is_typing = True
                pyperclip.copy(translated)
                time.sleep(0.05)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)
                is_typing = False
                
                self.is_typing_translation = False
                self.last_translated = translated
            
            self.buffer = ""
        except Exception as e:
            pass
        finally:
            is_typing = False
            self.is_typing_translation = False
            self.buffer = ""

    def translate_text(self, source_text, target_lang, source_lang):
        try:
            translator = GoogleTranslator(source=self.language_codes.get(source_lang, 'auto'), target=self.language_codes.get(target_lang, 'en'))
            translated = translator.translate(source_text)
            self.gui.update_output(translated)
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            self.gui.update_output(f"Translation error: {e}")
            return "N/A"

    def toggle_translation(self):
        self.translating = not self.translating
        self.gui.toggle_button.setText('Turn Off' if self.translating else 'Turn On')
        self.speak_status()
        
    def speak_status(self):
        audio_file = self.on_file if self.translating else self.off_file
        threading.Thread(target=playsound, args=(audio_file,), daemon=True).start()

    def capture_screen(self):
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32

        hwnd = win32gui.GetForegroundWindow()
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bot - top

        hwndDC = user32.GetWindowDC(hwnd)
        mfcDC = gdi32.CreateCompatibleDC(hwndDC)
        saveBitMap = gdi32.CreateCompatibleBitmap(hwndDC, width, height)
        gdi32.SelectObject(mfcDC, saveBitMap)

        result = ctypes.windll.user32.PrintWindow(hwnd, mfcDC, 0)

        bmpinfo = BITMAPINFO()
        bmpinfo.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmpinfo.bmiHeader.biWidth = width
        bmpinfo.bmiHeader.biHeight = -height
        bmpinfo.bmiHeader.biPlanes = 1
        bmpinfo.bmiHeader.biBitCount = 32
        bmpinfo.bmiHeader.biCompression = 0 
        
        buffer = ctypes.create_string_buffer(width * height * 4)
        gdi32.GetDIBits(mfcDC, saveBitMap, 0, height, buffer, ctypes.byref(bmpinfo), 0)

        gdi32.DeleteObject(saveBitMap)
        gdi32.DeleteDC(mfcDC)
        user32.ReleaseDC(hwnd, hwndDC)

        return Image.frombuffer('RGBA', (width, height), buffer, 'raw', 'BGRA', 0, 1)
    
    def capture_and_translate(self, ocr_lang):
        try:
            if not self.screen_capture_widget:
                self.screen_capture_widget = ScreenCaptureWidget()
                self.screen_capture_widget.area_selected.connect(lambda rect: self.process_selected_area(rect, ocr_lang))

            primary_screen = QApplication.primaryScreen()
            screen_geometry = primary_screen.geometry()

            self.screen_capture_widget.setGeometry(screen_geometry)
            self.screen_capture_widget.showFullScreen()
            self.screen_capture_widget.activateWindow()

        except Exception as e:
            error_message = f"An error occurred during capture and translation:\n{str(e)}"
            print(error_message)
            self.gui.update_output(error_message)

    def process_selected_area(self, selected_rect, ocr_lang):
        x, y, width, height = selected_rect.getRect()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        
        api_key = os.getenv('KEY')
        url = 'https://api.ocr.space/parse/image'

        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        ocr_lang_code = self.ocr_language_codes.get(ocr_lang.lower(), 'eng')
        
        response = requests.post(
            url,
            files={'screenshot.png': img_byte_arr},
            data={
                'apikey': api_key,
                'language': ocr_lang_code,
                'isOverlayRequired': False
            }
        )

        result = response.json()
        if result.get('IsErroredOnProcessing'):
            raise Exception(result.get('ErrorMessage', ['Unknown error'])[0])
        
        text = result['ParsedResults'][0]['ParsedText']

        if text.strip():
            translated = self.translate_text(text, 'english', 'auto')
            output = f"{translated}\n\n"
            self.gui.update_output(output)
        else:
            output = "No text could be extracted from the screen.\n\n"
            self.gui.update_output(output)

    def capture_and_translate(self):
        ocr_lang = self.gui.ocr_lang_combo.currentText()
        try:
            if not self.screen_capture_widget:
                self.screen_capture_widget = ScreenCaptureWidget()
                self.screen_capture_widget.area_selected.connect(lambda rect: self.process_selected_area(rect, ocr_lang))

            primary_screen = QApplication.primaryScreen()
            screen_geometry = primary_screen.geometry()

            self.screen_capture_widget.setGeometry(screen_geometry)
            self.screen_capture_widget.showFullScreen()
            self.screen_capture_widget.activateWindow()
        except Exception as e:
            self.gui.update_output(f"Error: {str(e)}\n\n")

    def __del__(self):
        if os.path.exists(self.on_file):
            os.remove(self.on_file)
        if os.path.exists(self.off_file):
            os.remove(self.off_file)
        os.rmdir(self.temp_dir)