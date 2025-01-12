from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel,QSizePolicy,QStackedWidget,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QFont,QRegion, QPainterPath,QMovie,QPainter
import sys
import requests
from io import BytesIO

class WeaterPage(QWidget):
    def __init__(self, stack, main_window):
        super().__init__()
        self.stack = stack  # Store reference to the stacked widget
        self.main_window = main_window  # Store reference to the main window
        
        layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 20)
        # layout.setAlignment(Qt.AlignTop)
     

        # layout.setAlignment(Qt.AlignCenter)
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(10, 10, 10, 10)  # Margins for spacing
        self.button_layout.setSpacing(20)


        # Add Back button to page 2
        back_button = QPushButton("<", self)
        back_button.clicked.connect(self.previous_page)
        back_button.setStyleSheet(
                """
                background-color: black;
                color: white;
                border-radius: 12px; /* Half of the width/height for a perfect circle */
                min-width: 24px;     /* Set width and height to the same value */
                min-height: 24px;
                max-width: 24px;     /* Prevent resizing */
                max-height: 24px;
                font-size: 12px;     /* Adjust font size for smaller buttons */
                """
                )
        self.button_layout.addWidget(back_button,alignment=Qt.AlignLeft)
        # layout.addWidget(back_button)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        # self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_layout.addWidget(self.image_label)
        # Add label to display selected option on page 2
        self.selected_option_label = QLabel("", self)
        self.selected_option_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.selected_option_label)

        # Add Exit button to page 2
        exit_button = QPushButton("x", self)
        exit_button.clicked.connect(self.exit_app)
        exit_button.setStyleSheet(
                """
                background-color: red;
                color: white;
                border-radius: 12px; /* Half of the width/height for a perfect circle */
                min-width: 24px;     /* Set width and height to the same value */
                min-height: 24px;
                max-width: 24px;     /* Prevent resizing */
                max-height: 24px;
                font-size: 12px;     /* Adjust font size for smaller buttons */
                """
                )
        self.button_layout.addWidget(exit_button,alignment=Qt.AlignRight)

        layout.addLayout(self.button_layout)

        
        
        # Add weather information label to page 2
        self.weather_label = QLabel("", self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weather_label)
    

    # def set_stylesheet(self,weather_condition):
    #     self.movie = QMovie("assets/rain.gif")
    #     self.movie.frameChanged.connect(self.repaint)
    #     self.movie.start()
    def set_weather_data(self, weather_data):
        if weather_data:
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            font = QFont()
            font.setBold(True)
            font.setPointSize(20)  # Adjust the size as needed
            self.weather_label.setFont(font)
            self.weather_label.setText(f"{int(temperature)}°C\n\n{description}")
            # self.set_stylesheet(weather_condition=weather_data)
        else:
            self.weather_label.setText("Failed to fetch weather data.")

    def get_contry_data(self,weather_data):
         if weather_data:
             return weather_data["sys"]["country"].lower()

    def set_contry_flag_label(self,weather_data):
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

                    # # Create a circular region mask for the QLabel
                    # path = QPainterPath()
                    # radius = min(scaled_pixmap.width(), scaled_pixmap.height()) // 2
                    # path.addEllipse(0, 0, radius * 2, radius * 2)
                    # region = QRegion(path.toFillPolygon().toPolygon())
                    # Set scaled pixmap to label
                    self.image_label.setPixmap(scaled_pixmap)
                    # Resize label to fit pixmap
                    self.image_label.setFixedSize(scaled_pixmap.size())
                    # self.image_label.setMask(region)
            

                else:
                    self.image_label.setText("Failed to load image")
            else:
                self.image_label.setText(f"Failed to download image: {response.status_code}")


    def previous_page(self):
        self.stack.setCurrentWidget(self.main_window.page1)

    def exit_app(self):
        QApplication.quit()
    # def paintEvent(self, event):
    #     currentFrame = self.movie.currentPixmap()
    #     frameRect = currentFrame.rect()
    #     frameRect.moveCenter(self.rect().center())
    #     if frameRect.intersects(event.rect()):
    #         painter = QPainter(self)
    #         painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)
