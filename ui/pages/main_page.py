import asyncio
from api import google_api
from api.weater_api import fetch_weather
from config.config import countries
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QComboBox, QWidget, QLabel, QStackedWidget,QCompleter,QLineEdit
from PyQt5.QtCore import Qt,QStringListModel



import asyncio

class Page1(QWidget):
    def __init__(self, stack, main_window):
        super().__init__()
        self.stack = stack  # Store reference to the stacked widget
        self.main_window = main_window  # Store reference to the main window

       # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)  # Set the layout for the QWidget

        # Input box
        self.location_input = QLineEdit(self)
        self.location_input.setPlaceholderText("Enter location...")
        self.layout.addWidget(self.location_input)

        # Label for displaying selected location details
        self.location_details = QLabel(self)
        self.layout.addWidget(self.location_details)

        # Connect text changes to fetch suggestions
        self.location_input.textChanged.connect(self.update_suggestions)

        # Completer setup
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(False)
        self.completer.setFilterMode(Qt.MatchContains)
        self.location_input.setCompleter(self.completer)


        # Add Next button to page 1
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_page)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet(
            "background-color: gray; color: white; border-radius: 10px; padding: 5px;"
        )
       
        self.layout.addWidget(self.next_button)

        # Add Exit button to page 1
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.exit_app)
        self.exit_button.setStyleSheet(
            "background-color: red; color: white; border-radius: 10px; padding: 5px;"
        )
        self.layout.addWidget(self.exit_button)

    def next_page(self):
        # selected_option = self.dropdown.currentText()  # Get the selected option
        # lat = countries[selected_option]["latitude"]
        # lon = countries[selected_option]["longitude"]

        # Fetch weather data asynchronously
        if self.lat and self.lon:
            loop = asyncio.get_event_loop()
            weather_data = loop.run_until_complete(fetch_weather(self.lat, self.lon))

            if weather_data:
                self.main_window.page2.set_contry_flag_label(weather_data)
                self.main_window.page2.set_weather_data(weather_data)  # Pass weather data to page2
            else:
                self.main_window.page2.set_weather_data(None)

            self.stack.setCurrentWidget(self.main_window.page2)
   

    def exit_app(self):
        QApplication.quit()
    def update_suggestions(self, text):
        if len(text) < 3:  # Avoid unnecessary API calls for short text
            return

        # Fetch suggestions using API utility
        suggestions = google_api.fetch_location_suggestions(text)
        
        # Update completer model
        self.completer.setModel(QStringListModel(suggestions))
        self.completer.popup().show()

        # Set completer activated signal to fetch lat/lon
        self.completer.activated.connect(self.fetch_lat_lon)

    def fetch_lat_lon(self, location):
        # Fetch lat/lon using API utility
        result = google_api.fetch_lat_lon(location)
        if result:
            self.lat,  self.lon = result
            self.next_button.setEnabled(True)
            self.next_button.setStyleSheet(
            "background-color: green; color: white; border-radius: 10px; padding: 5px;"
        )
        else:
            self.location_details.setText("Failed to fetch location details")






