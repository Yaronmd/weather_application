import asyncio
import aiohttp
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QComboBox, QWidget, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("API_KEY")

countries = {
    "Israel": {"latitude": 31.0461, "longitude": 34.8516},
    "United States": {"latitude": 37.0902, "longitude": -95.7129},
    "Canada": {"latitude": 56.1304, "longitude": -106.3468},
    "United Kingdom": {"latitude": 55.3781, "longitude": -3.4360},
    "Germany": {"latitude": 51.1657, "longitude": 10.4515},
    "France": {"latitude": 46.6034, "longitude": 1.8883},
    "China": {"latitude": 35.8617, "longitude": 104.1954},
    "Japan": {"latitude": 36.2048, "longitude": 138.2529},
    "India": {"latitude": 20.5937, "longitude": 78.9629},
    "Australia": {"latitude": -25.2744, "longitude": 133.7751},
    "Brazil": {"latitude": -14.2350, "longitude": -51.9253},
    "South Africa": {"latitude": -30.5595, "longitude": 22.9375},
    "Russia": {"latitude": 61.5240, "longitude": 105.3188},
    "Mexico": {"latitude": 23.6345, "longitude": -102.5528},
    "Italy": {"latitude": 41.8719, "longitude": 12.5674},
    "Argentina": {"latitude": -38.4161, "longitude": -63.6167},
    "Egypt": {"latitude": 26.8206, "longitude": 30.8025},
    "Saudi Arabia": {"latitude": 23.8859, "longitude": 45.0792},
    "South Korea": {"latitude": 35.9078, "longitude": 127.7669},
    "Turkey": {"latitude": 38.9637, "longitude": 35.2433},
}

API_URL = "http://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(lat, lon):
    url = f"{API_URL}?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None


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
        api_key = "your_api_key_here"  # Replace with your actual API key

        # Fetch weather data asynchronously
        loop = asyncio.get_event_loop()
        weather_data = loop.run_until_complete(fetch_weather(lat, lon))

        if weather_data:
            self.main_window.page2.set_weather_data(weather_data)  # Pass weather data to page2
        else:
            self.main_window.page2.set_weather_data(None)

        self.stack.setCurrentWidget(self.main_window.page2)

    def exit_app(self):
        QApplication.quit()

class Page2(QWidget):
    def __init__(self, stack, main_window):
        super().__init__()
        self.stack = stack  # Store reference to the stacked widget
        self.main_window = main_window  # Store reference to the main window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Add label to page 2
        label = QLabel("This is the next page!", self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

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
            self.weather_label.setText(f"Temperature: {temperature}°C\nDescription: {description}")
        else:
            self.weather_label.setText("Failed to fetch weather data.")

    def previous_page(self):
        self.stack.setCurrentWidget(self.main_window.page1)

    def exit_app(self):
        QApplication.quit()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Next Page Example")
        self.setGeometry(100, 100, 400, 300)

        # Create a stacked widget for managing pages
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Create instances of the pages and pass the stack reference and the main window
        self.page1 = Page1(self.stack, self)
        self.page2 = Page2(self.stack, self)

        # Add pages to the stack
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
