import time
import threading
from PyQt6.QtCore import QObject, QTimer
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
        self.gui.ocr_languages_changed_signal.connect(self.update_ocr_languages)
        self.gui.show()

        self.ocr_source_lang = 'english'
        self.ocr_target_lang = 'english'

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
            'abkhazian': 'ab', 'acehnese': 'ace', 'acoli': 'ach', 'afar': 'aa', 'afrikaans': 'af',
            'akan': 'ak', 'albanian': 'sq', 'alur': 'alz', 'amharic': 'am', 'arabic': 'ar',
            'armenian': 'hy', 'assamese': 'as', 'avaric': 'av', 'awadhi': 'awa', 'aymara': 'ay',
            'azerbaijani': 'az', 'balinese': 'ban', 'baluchi': 'bal', 'bambara': 'bm', 'bangla': 'bn',
            'baoulé': 'bci', 'bashkir': 'ba', 'basque': 'eu', 'batak karo': 'btx', 'batak simalungun': 'bts',
            'batak toba': 'bbc', 'belarusian': 'be', 'bemba': 'bem', 'betawi': 'bew', 'bhojpuri': 'bho',
            'bikol': 'bik', 'bosnian': 'bs', 'breton': 'br', 'bulgarian': 'bg', 'buriat': 'bua',
            'burmese': 'my', 'cantonese': 'yue', 'catalan': 'ca', 'cebuano': 'ceb', 'central kurdish': 'ckb',
            'chamorro': 'ch', 'chechen': 'ce', 'chiga': 'cgg', 'chinese (simplified)': 'zh-CN',
            'chinese (traditional)': 'zh-TW', 'chuukese': 'chk', 'chuvash': 'cv', 'corsican': 'co',
            'crimean tatar': 'crh', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dari': 'prs',
            'dinka': 'din', 'divehi': 'dv', 'dogri': 'doi', 'dombe': 'dov', 'dutch': 'nl', 'dyula': 'dyu',
            'dzongkha': 'dz', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee',
            'faroese': 'fo', 'fijian': 'fj', 'filipino': 'fil', 'finnish': 'fi', 'fon': 'fon',
            'french': 'fr', 'friulian': 'fur', 'fulani': 'ff', 'ga': 'gaa', 'galician': 'gl',
            'ganda': 'lg', 'georgian': 'ka', 'german': 'de', 'goan konkani': 'gom', 'greek': 'el',
            'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hakha chin': 'cnh', 'hausa': 'ha',
            'hawaiian': 'haw', 'hebrew': 'he', 'hiligaynon': 'hil', 'hindi': 'hi', 'hmong': 'hmn',
            'hungarian': 'hu', 'hunsrik': 'hrx', 'iban': 'iba', 'icelandic': 'is', 'igbo': 'ig',
            'iloko': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'jamaican patois': 'jam',
            'japanese': 'ja', 'javanese': 'jv', 'jingpo': 'kac', 'kalaallisut': 'kl', 'kannada': 'kn',
            'kanuri': 'kr', 'kazakh': 'kk', 'khasi': 'kha', 'khmer': 'km', 'kinyarwanda': 'rw',
            'kituba': 'ktu', 'kokborok': 'trp', 'komi': 'kv', 'kongo': 'kg', 'korean': 'ko', 'krio': 'kri',
            'kurdish': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latgalian': 'ltg', 'latin': 'la', 'latvian': 'lv',
            'ligurian': 'lij', 'limburgish': 'li', 'lingala': 'ln', 'lithuanian': 'lt', 'lombard': 'lmo',
            'luo': 'luo', 'luxembourgish': 'lb', 'macedonian': 'mk', 'madurese': 'mad', 'maithili': 'mai',
            'makasar': 'mak', 'malagasy': 'mg', 'malay': 'ms', 'malay (arabic)': 'ms-arab', 'malayalam': 'ml',
            'maltese': 'mt', 'mam': 'mam', 'manipuri (meitei mayek)': 'mni', 'manx': 'gv', 'māori': 'mi',
            'marathi': 'mr', 'marshallese': 'mh', 'marwari': 'mwr', 'meadow mari': 'mhr', 'minangkabau': 'min',
            'mizo': 'lus', 'mongolian': 'mn', 'morisyen': 'mfe', 'nahuatl (eastern huasteca)': 'nhe',
            'ndau': 'ndc', 'nepalbhasa (newari)': 'new', 'nepali': 'ne', 'nko': 'nqo', 'northern sami': 'se',
            'northern sotho': 'nso', 'norwegian': 'no', 'nuer': 'nus', 'nyanja': 'ny', 'occitan': 'oc',
            'odia': 'or', 'oromo': 'om', 'ossetic': 'os', 'pampanga': 'pam', 'pangasinan': 'pag',
            'papiamento': 'pap', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt',
            'portuguese (portugal)': 'pt-PT', 'punjabi': 'pa', 'punjabi (arabic)': 'pa-arab', 'q\'eqchi\'': 'kek',
            'quechua': 'qu', 'romanian': 'ro', 'romany': 'rom', 'rundi': 'rn', 'russian': 'ru', 'samoan': 'sm',
            'sango': 'sg', 'sanskrit': 'sa', 'santali (latin)': 'sat', 'scottish gaelic': 'gd', 'serbian': 'sr',
            'seselwa creole french': 'crs', 'shan': 'shn', 'shona': 'sn', 'sicilian': 'scn', 'silesian': 'szl',
            'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so',
            'south ndebele': 'nr', 'southern sotho': 'st', 'spanish': 'es', 'sundanese': 'su', 'susu': 'sus',
            'swahili': 'sw', 'swati': 'ss', 'swedish': 'sv', 'tahitian': 'ty', 'tajik': 'tg', 'tamazight': 'ber',
            'tamazight (tifinagh)': 'ber-tfng', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'tetum': 'tet',
            'thai': 'th', 'tibetan': 'bo', 'tigrinya': 'ti', 'tiv': 'tiv', 'tok pisin': 'tpi', 'tongan': 'to',
            'tsonga': 'ts', 'tswana': 'tn', 'tulu': 'tcy', 'tumbuka': 'tum', 'turkish': 'tr', 'turkmen': 'tk',
            'tuvinian': 'tyv', 'udmurt': 'udm', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz',
            'venda': 've', 'venetian': 'vec', 'vietnamese': 'vi', 'waray': 'war', 'welsh': 'cy',
            'western frisian': 'fy', 'wolof': 'wo', 'xhosa': 'xh', 'yakut': 'sah', 'yiddish': 'yi',
            'yoruba': 'yo', 'yucatec maya': 'yua', 'zapotec': 'zap', 'zulu': 'zu'
        }

        self.ocr_language_codes = {
            'arabic': 'ara',
            'bulgarian': 'bul',
            'chinese (simplified)': 'chs',
            'chinese (traditional)': 'cht',
            'croatian': 'hrv',
            'czech': 'cze',
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
            translator = GoogleTranslator(source='auto', target=target_lang)
            translated = translator.translate(source_text)
            return translated
        except Exception as e:
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
    
    def capture_and_translate(self):
        try:
            if not self.screen_capture_widget:
                self.screen_capture_widget = ScreenCaptureWidget()
                self.screen_capture_widget.area_selected.connect(self.process_selected_area)

            primary_screen = QApplication.primaryScreen()
            screen_geometry = primary_screen.geometry()

            self.screen_capture_widget.setGeometry(screen_geometry)
            self.screen_capture_widget.showFullScreen()
            self.screen_capture_widget.activateWindow()
        except Exception as e:
            self.gui.update_output(f"Error: {str(e)}\n\n")

    def process_selected_area(self, selected_rect):
        x, y, width, height = selected_rect.getRect()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        
        api_key = os.getenv('KEY')
        url = 'https://api.ocr.space/parse/image'

        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        ocr_lang_code = self.ocr_language_codes.get(self.ocr_source_lang.lower(), 'eng')
        
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
            translated = self.translate_text(text, self.ocr_target_lang, self.ocr_source_lang)
            output = f"{translated}\n\n"
            self.gui.update_output(output)
        else:
            output = "No text could be extracted from the screen.\n\n"
            self.gui.update_output(output)

    def update_ocr_languages(self, source_lang, target_lang):
        self.ocr_source_lang = source_lang
        self.ocr_target_lang = target_lang

    def __del__(self):
        if os.path.exists(self.on_file):
            os.remove(self.on_file)
        if os.path.exists(self.off_file):
            os.remove(self.off_file)
        os.rmdir(self.temp_dir)