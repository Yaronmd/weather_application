import asyncio
from api.weater_api import fetch_weather
from config.config import countries
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QComboBox, QWidget, QLabel, QStackedWidget
from PyQt5.QtCore import Qt



import asyncio

class Page1(QWidget):
    def __init__(self, stack, main_window):
        super().__init__()
        self.stack = stack  # Store reference to the stacked widget
        self.main_window = main_window  # Store reference to the main window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Add dropdown to page 1
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(countries.keys())
        layout.addWidget(self.dropdown)

        # Add Next button to page 1
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setStyleSheet(
            "background-color: green; color: white; border-radius: 10px; padding: 5px;"
        )
        layout.addWidget(self.next_button)

        # Add Exit button to page 1
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.exit_app)
        self.exit_button.setStyleSheet(
            "background-color: red; color: white; border-radius: 10px; padding: 5px;"
        )
        layout.addWidget(self.exit_button)

    def next_page(self):
        selected_option = self.dropdown.currentText()  # Get the selected option
        lat = countries[selected_option]["latitude"]
        lon = countries[selected_option]["longitude"]

        # Fetch weather data asynchronously
        loop = asyncio.get_event_loop()
        weather_data = loop.run_until_complete(fetch_weather(lat, lon))

        if weather_data:
            self.main_window.page2.set_main_label(weather_data)
            self.main_window.page2.set_weather_data(weather_data)  # Pass weather data to page2
        else:
            self.main_window.page2.set_weather_data(None)

        self.stack.setCurrentWidget(self.main_window.page2)

    def exit_app(self):
        QApplication.quit()






