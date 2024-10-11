from PyQt6.QtWidgets import QWidget, QRubberBand
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QRect, pyqtSignal

class ScreenCaptureWidget(QWidget):
    area_selected = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.rubberband = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.origin = None
        self.current = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(QRect(self.origin, self.origin))
        self.rubberband.show()

    def mouseMoveEvent(self, event):
        self.current = event.pos()
        self.rubberband.setGeometry(QRect(self.origin, self.current).normalized())

    def mouseReleaseEvent(self, event):
        self.current = event.pos()
        self.hide()
        if self.origin and self.current:
            selected_area = QRect(self.origin, self.current).normalized()
            self.area_selected.emit(selected_area)

    def showFullScreen(self):
        super().showFullScreen()
        self.setCursor(Qt.CursorShape.CrossCursor)