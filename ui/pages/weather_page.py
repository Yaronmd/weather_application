from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel,QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QFont
import sys
import requests
from io import BytesIO

class WeaterPage(QWidget):
    def __init__(self, stack, main_window):
        super().__init__()
        self.stack = stack  # Store reference to the stacked widget
        self.main_window = main_window  # Store reference to the main window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)

        layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.image_label)

        # Add label to display selected option on page 2
        self.selected_option_label = QLabel("", self)
        self.selected_option_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.selected_option_label)

        # Add weather information label to page 2
        self.weather_label = QLabel("", self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weather_label)

        # Add Back button to page 2
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.previous_page)
        back_button.setStyleSheet(
            "background-color: red; color: white; border-radius: 10px; padding: 5px;"
        )
        layout.addWidget(back_button)

        # Add Exit button to page 2
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.exit_app)
        exit_button.setStyleSheet(
            "background-color: red; color: white; border-radius: 10px; padding: 5px;"
        )
        layout.addWidget(exit_button)
    
    def set_weather_data(self, weather_data):
        if weather_data:
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            font = QFont()
            font.setBold(True)
            font.setPointSize(20)  # Adjust the size as needed
            self.weather_label.setFont(font)
            self.weather_label.setText(f"{temperature}°C\n\n{description}")
        else:
            self.weather_label.setText("Failed to fetch weather data.")

    def get_contry_data(self,weather_data):
         if weather_data:
             return weather_data["sys"]["country"].lower()

    def set_main_label(self,weather_data):
        if weather_data:
                # Download the image from the URL
            url = f'https://flagicons.lipis.dev/flags/1x1/{self.get_contry_data(weather_data)}.svg'
            response = requests.get(url)
            if response.status_code == 200:
                # Load image into QPixmap
                image_data = BytesIO(response.content)
                pixmap = QPixmap()
                if pixmap.loadFromData(image_data.read()):
                    # Scale pixmap to 16x16 pixels
                    scaled_pixmap = pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    # Set scaled pixmap to label
                    self.image_label.setPixmap(scaled_pixmap)
                    # Resize label to fit pixmap
                    self.image_label.setFixedSize(scaled_pixmap.size())
                else:
                    self.image_label.setText("Failed to load image")
            else:
                self.image_label.setText(f"Failed to download image: {response.status_code}")


    def previous_page(self):
        self.stack.setCurrentWidget(self.main_window.page1)

    def exit_app(self):
        QApplication.quit()