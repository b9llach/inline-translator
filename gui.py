from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit, QSplitter, QFrame, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from deep_translator import GoogleTranslator

class TranslatorGUI(QWidget):
    toggle_signal = pyqtSignal(bool)
    language_signal = pyqtSignal(str)
    translate_signal = pyqtSignal(str, str, str) 
    capture_signal = pyqtSignal(str, str)
    ocr_languages_changed_signal = pyqtSignal(str, str) 
    
    def __init__(self):
        super().__init__()
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
        
        self.all_languages_dict = {
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
        self.google_languages = GoogleTranslator().get_supported_languages(as_dict=True)
        self.language_names = {v: k for k, v in self.google_languages.items()}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Translator Control')
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()

        control_layout = QHBoxLayout()
        self.toggle_button = QPushButton('Turn On', self)
        self.toggle_button.clicked.connect(self.toggle_translation)
        control_layout.addWidget(self.toggle_button)

        self.camera_button = QPushButton('📷', self)
        self.camera_button.setToolTip('Capture Screen Area')
        self.camera_button.clicked.connect(self.capture_screen)
        control_layout.addWidget(self.camera_button)

        lang_label = QLabel('Target Language:')
        self.lang_combo = QComboBox()

        self.lang_combo.clear()
        self.lang_combo.addItems(sorted(self.language_names.values()))
        self.lang_combo.setCurrentText('Italian')  # Set default to Italian
        self.lang_combo.currentTextChanged.connect(self.change_language)

        lang_layout = QVBoxLayout()
        lang_layout.addWidget(self.lang_combo)
        
        control_layout.addWidget(lang_label)
        control_layout.addLayout(lang_layout)

        layout.addLayout(control_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        ocr_layout = QHBoxLayout()
        ocr_source_lang_label = QLabel('OCR Source Language:')
        self.ocr_source_lang_combo = QComboBox()
        self.ocr_target_lang_combo = QComboBox() 
        
        self.ocr_source_lang_combo.clear()
        self.ocr_target_lang_combo.clear()
        ocr_languages = ['english'] + list(self.ocr_language_codes.keys())
        self.ocr_source_lang_combo.addItems(ocr_languages)
        self.ocr_target_lang_combo.addItems(ocr_languages)
        
        ocr_layout.addWidget(ocr_source_lang_label)
        ocr_layout.addWidget(self.ocr_source_lang_combo)

        ocr_target_lang_label = QLabel('OCR Target Language:')
        ocr_layout.addWidget(ocr_target_lang_label)
        ocr_layout.addWidget(self.ocr_target_lang_combo)

        layout.addLayout(ocr_layout)

        self.ocr_source_lang_combo.currentTextChanged.connect(self.update_ocr_languages)
        self.ocr_target_lang_combo.currentTextChanged.connect(self.update_ocr_languages)

        translation_layout = QHBoxLayout()
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text in any language to translate")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Translation will appear here")

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.input_text)
        splitter.addWidget(self.output_text)
        splitter.setSizes([400, 400])

        translation_layout.addWidget(splitter)
        layout.addLayout(translation_layout)

        self.translate_button = QPushButton('Translate', self)
        self.translate_button.clicked.connect(self.translate_text)
        layout.addWidget(self.translate_button)

        self.setLayout(layout)

    def update_ocr_languages(self):
        ocr_source_lang = self.ocr_source_lang_combo.currentText().lower()
        ocr_target_lang = self.ocr_target_lang_combo.currentText().lower()
        self.ocr_languages_changed_signal.emit(ocr_source_lang, ocr_target_lang)

    def capture_screen(self):
        ocr_source_lang = self.ocr_source_lang_combo.currentText().lower()
        ocr_target_lang = self.ocr_target_lang_combo.currentText().lower()
        self.capture_signal.emit(ocr_source_lang, ocr_target_lang)

    def toggle_translation(self):
        if self.toggle_button.text() == 'Turn On':
            self.toggle_button.setText('Turn Off')
            self.toggle_signal.emit(True)
        else:
            self.toggle_button.setText('Turn On')
            self.toggle_signal.emit(False)

    def change_language(self, language):
        self.language_signal.emit(language)

    def translate_text(self):
        source_text = self.input_text.toPlainText()
        target_lang = self.lang_combo.currentText().lower()
        source_lang = 'auto' 
        self.translate_signal.emit(source_text, target_lang, source_lang)

    def update_output(self, translated_text):
        self.output_text.setPlainText(translated_text)

    def filter_languages(self, text):
        self.lang_combo.clear()
        filtered_languages = [lang for lang in self.all_languages_dict.keys() if text.lower() in lang.lower()]
        self.lang_combo.addItems(filtered_languages)