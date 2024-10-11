import sys
from PyQt6.QtWidgets import QApplication
import os
from translator import Translator

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = Translator()
    sys.exit(app.exec())