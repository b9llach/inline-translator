import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from translator import Translator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon("./imgs/icon.png")
    app.setWindowIcon(app_icon)
    translator = Translator()
    sys.exit(app.exec())