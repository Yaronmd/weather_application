from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtCore import Qt

class ResizableRoundWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set initial size and properties
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("Round Window with Dropdown and Exit Button")

        # Remove the title bar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        # Set initial background color
        self.setStyleSheet("background-color: lightblue;")

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add dropdown (combo box)
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])
        self.dropdown.currentIndexChanged.connect(self.on_dropdown_change)
        layout.addWidget(self.dropdown)

        # Add Exit button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close_window)
        self.exit_button.setStyleSheet(
            "background-color: red; color: white; border-radius: 10px; padding: 5px;"
        )
        layout.addWidget(self.exit_button)

        # Apply initial round shape
        self.setRoundShape()

    def setRoundShape(self):
        # Create a round shape based on the current size
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        # Reapply the round shape when the window is resized
        self.setRoundShape()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        # Enable dragging of the frameless window
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # Update position during drag
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def on_dropdown_change(self, index):
        # Handle dropdown selection change
        print(f"Selected: {self.dropdown.itemText(index)}")

    def close_window(self):
        # Close the application
        print("Exiting application...")
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = ResizableRoundWindow()
    window.show()
    app.exec()
