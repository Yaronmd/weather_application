from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QComboBox, QWidget, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QRegion, QPainterPath
from ui.pages.main_page import Page1
from ui.pages.weather_page import WeaterPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 200, 200)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # Create a stacked widget for managing pages
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Create instances of the pages and pass the stack reference and the main window
        self.page1 = Page1(self.stack, self)
        self.page2 = WeaterPage(self.stack, self)

        # Add pages to the stack
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)




if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()