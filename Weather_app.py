import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton,
                             QLineEdit, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import requests


class weather_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 150, 400, 400)
        self.setWindowTitle("Weather app")
        self.setWindowIcon(QIcon("OIP.webp"))
        self.city_label = QLabel("Enter the city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Submit", self)
        self.temp_label = QLabel("30°C", self)
        self.label_emoji = QLabel("☀️", self)
        self.description_label = QLabel("Sunny", self)
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.label_emoji)
        vbox.addWidget(self.description_label)

        central = QWidget()
        central.setLayout(vbox)
        self.setCentralWidget(central)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.label_emoji.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.label_emoji.setObjectName("label_emoji")
        self.description_label.setObjectName("discription_label")

        self.setStyleSheet("""
QLabel, QPushButton, QLineEdit { font-size: 18px; font-family: Arial; }
QLabel#city_label { font-size: 22px; font-weight: bold; font-style: italic; }
QLabel#label_emoji { font-size: 55px; font-family: "Segoe UI Emoji"; }
QLineEdit#city_input { font-size: 18px; padding: 6px; }
QPushButton#get_weather_button { font-size: 18px; padding: 6px; border: 2px solid #444; }
QLabel#temp_label { font-size: 32px; font-weight: bold; }
""")

        self.get_weather_button.clicked.connect(self.get_weather)
        # Hide weather output until user clicks Submit
        self.temp_label.hide()
        self.label_emoji.hide()
        self.description_label.hide()
    def get_weather(self):
        api_key = "77932878049c494044c5e9581490066a"
        # Show output widgets when user clicks Submit
        self.temp_label.show()
        self.label_emoji.show()
        self.description_label.show()
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name.")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['cod'] == 200:
                self.display_weather(data)
            

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("failed to retrive data\nPlease check your input")
                case 401:
                    self.display_errornt("failed to retrive data\nPlease check your input")
                case 402:
                    self.display_error("unautorized\n invalid API key")        
                case 403:
                    self.display_error("forbidden\naccess denied")
                case 404:
                    self.display_error("city not found\nPlease enter correct cty name")
                case 500:
                    self.display_error("internal server error\nPlease try again later")
                case 502:
                    self.display_error("bad gateway\ninvalid response from the server")
                case 503:
                    self.display_error("Server unavailable\nserver is down")
                case 504:
                    self.display_error("timeout\nno response from the user")
                case _:
                    self.display_error(f"HTTP Error occured\nfailed to get {http_error}")
        except requests.exceptions.ConnectionError:   
            self.display_error("Connection Error\n please check your internet")
        except requests.exceptions.Timeout:
            self.display_error("timeout error \n try again")
        except requests.exceptions.TooManyRedirects:
            self.display_error("too many redirects\n check your URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"request error \n {req_error} ")
    
    def display_error(self, message):
        self.temp_label.setText(message)
        self.temp_label.show()

    def display_weather(self, data):
        temperature_C = data["main"]["temp"]
        self.temp_label.setText(f"{temperature_C}°C")
        weather_description = data["weather"][0]["description"]
        # ensure output widgets are visible when weather is displayed
        self.temp_label.show()
        self.label_emoji.show()
        self.description_label.show()
        
        
        weather_id = data["weather"][0]["id"]
        self.label_emoji.setText(self.display_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
    def display_weather_emoji(self, weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = weather_app()
    window.show()
    sys.exit(app.exec_())