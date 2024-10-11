from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit, QSplitter, QFrame, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

class TranslatorGUI(QWidget):
    toggle_signal = pyqtSignal(bool)
    language_signal = pyqtSignal(str)
    translate_signal = pyqtSignal(str, str)
    capture_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.language_codes = {
            'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy',
            'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu',
            'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg',
            'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN',
            'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs',
            'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en',
            'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi',
            'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de',
            'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha',
            'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu',
            'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga',
            'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk',
            'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri',
            'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo',
            'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg',
            'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg',
            'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr',
            'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my',
            'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps',
            'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu',
            'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd',
            'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd',
            'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es',
            'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta',
            'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts',
            'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur',
            'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh',
            'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
        }
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

        self.all_languages = ['italian'] + [lang for lang in self.language_codes.keys()]
        
        self.lang_combo.addItems(self.all_languages)
        self.lang_combo.currentTextChanged.connect(self.change_language)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search languages...")
        self.search_bar.textChanged.connect(self.filter_languages)

        lang_layout = QVBoxLayout()
        lang_layout.addWidget(self.search_bar)
        lang_layout.addWidget(self.lang_combo)
        
        control_layout.addWidget(lang_label)
        control_layout.addLayout(lang_layout)

        layout.addLayout(control_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

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

    def toggle_translation(self):
        if self.toggle_button.text() == 'Turn On':
            self.toggle_button.setText('Turn Off')
            self.toggle_signal.emit(True)
        else:
            self.toggle_button.setText('Turn On')
            self.toggle_signal.emit(False)

    def change_language(self, language):
        code = self.language_codes.get(language, 'en') 
        self.language_signal.emit(code)

    def translate_text(self):
        source_text = self.input_text.toPlainText()
        self.translate_signal.emit(source_text, self.lang_combo.currentText().lower())

    def update_output(self, translated_text):
        self.output_text.setPlainText(translated_text)

    def filter_languages(self, text):
        self.lang_combo.clear()
        filtered_languages = [lang for lang in self.all_languages if text.lower() in lang.lower()]
        self.lang_combo.addItems(filtered_languages)

    def capture_screen(self):
        self.capture_signal.emit()