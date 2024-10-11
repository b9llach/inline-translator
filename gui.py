from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit, QSplitter, QFrame, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

class TranslatorGUI(QWidget):
    toggle_signal = pyqtSignal(bool)
    language_signal = pyqtSignal(str)
    translate_signal = pyqtSignal(str, str, str) 
    capture_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
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
        ocr_lang_label = QLabel('OCR Language:')
        self.ocr_lang_combo = QComboBox()
        self.ocr_lang_combo.addItems(['english'] + [lang for lang in self.language_codes.keys()])
        ocr_layout.addWidget(ocr_lang_label)
        ocr_layout.addWidget(self.ocr_lang_combo)
        layout.addLayout(ocr_layout)

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
        target_lang = self.lang_combo.currentText().lower()
        source_lang = self.ocr_lang_combo.currentText().lower()
        self.translate_signal.emit(source_text, target_lang, source_lang)

    def update_output(self, translated_text):
        self.output_text.setPlainText(translated_text)

    def filter_languages(self, text):
        self.lang_combo.clear()
        filtered_languages = [lang for lang in self.all_languages if text.lower() in lang.lower()]
        self.lang_combo.addItems(filtered_languages)

    def capture_screen(self):
        ocr_lang = self.ocr_lang_combo.currentText().lower()
        self.capture_signal.emit(ocr_lang)