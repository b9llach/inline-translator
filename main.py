import sys
from PyQt6.QtWidgets import QApplication
from translator import Translator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = Translator()
    sys.exit(app.exec())