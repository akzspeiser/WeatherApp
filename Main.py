########################################################################
## IMPORTS
########################################################################
import sys
import threading
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_interface2 import Ui_MainWindow
from Custom_Widgets.Widgets import loadJsonStyle

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        loadJsonStyle(self, self.ui)
        ########################################################################

        self.show()

        # Connect menu buttons to functions
        self.ui.settingsButton.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpButton.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.closeCenterMenuButton.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())
        self.ui.moreMenuButton.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profileMenuButton.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.closeRightMenuButton.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())
        self.ui.closeNotificationButton.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())

        # Line edit for zipcode input
        self.ui.zipcodeInput = self.ui.lineEdit

        # Set a default value for the zipcode input
        self.ui.zipcodeInput.setText("97478")

        # Connect weather functions to buttons
        self.ui.dailyButton.clicked.connect(lambda: self.get_today_weather(self.ui.zipcodeInput.text()))
        self.ui.weeklyButton.clicked.connect(lambda: self.get_weekly_forecast(self.ui.zipcodeInput.text()))
        self.ui.weatherMapButton.clicked.connect(self.display_local_weather_map)  # Connect the weather map button
        self.ui.profileMenuButton.clicked.connect(self.show_profile)
        self.ui.notificationButton.clicked.connect(lambda: self.get_weather_alerts(self.ui.zipcodeInput.text()))

        # Fetch and display weather data in the background
        threading.Thread(target=self.get_weather_data).start()

        # Connect the line edit's returnPressed signal to update weather data
        self.ui.zipcodeInput.returnPressed.connect(self.update_weather_data)

    def moveWindow(self, event):
        # Dummy method to handle the moveWindow attribute error
        pass

    def get_weather_data(self):
        zipcode = self.ui.zipcodeInput.text()
        self.get_current_weather(zipcode)
        self.get_today_weather(zipcode)
        self.get_weekly_forecast(zipcode)

    def update_weather_data(self):
        # Fetch and display weather data based on new ZIP code
        threading.Thread(target=self.get_weather_data).start()

    def get_current_weather(self, zipcode):
        try:
            response = requests.get(f'http://localhost:5003/get_current_weather/{zipcode}')
            if response.status_code == 200:
                data = response.json()
                self.ui.label_27.setText(f"Current Weather ({zipcode}):\nTemperature: {data['current_temperature']}°F\nDescription: {data['current_weather']}")
            else:
                self.ui.label_27.setText(f"Failed to retrieve current weather for {zipcode}")
        except requests.exceptions.RequestException as e:
            self.ui.label_27.setText(f"Error: {e}")

    def get_today_weather(self, zipcode):
        try:
            response = requests.get(f'http://localhost:5003/get_today_weather/{zipcode}')
            if response.status_code == 200:
                data = response.json()
                today_weather = data['today_weather']
                self.ui.label_10.setText(f"Temperature: {today_weather['temperature']}°F\nDescription: {today_weather['shortForecast']}")
            else:
                self.ui.label_10.setText(f"Failed to retrieve today's weather for {zipcode}")
        except requests.exceptions.RequestException as e:
            self.ui.label_10.setText(f"Error: {e}")

    def get_weekly_forecast(self, zipcode):
        try:
            response = requests.get(f'http://localhost:5003/get_weekly_forecast/{zipcode}')
            if response.status_code == 200:
                data = response.json()
                forecast = '\n'.join([f"{period['name']}: {period['temperature']}°F, {period['shortForecast']}" for period in data['weekly_forecast']])
                self.ui.label_11.setText(forecast)
            else:
                self.ui.label_11.setText(f"Failed to retrieve weekly forecast for {zipcode}")
        except requests.exceptions.RequestException as e:
            self.ui.label_11.setText(f"Error: {e}")

    def get_weather_alerts(self, zipcode):
        try:
            response = requests.get(f'http://localhost:5003/get_weather_alerts/{zipcode}')
            if response.status_code == 200:
                data = response.json()
                alerts = '\n\n'.join([f"Alert: {alert['Alert']}\nWhere: {alert['Where']}\nWhen: {alert['When']}\nImpacts: {alert['Impacts']}" for alert in data['alerts']])
                self.ui.label_13.setText(alerts if alerts else "No active weather alerts")
            else:
                self.ui.label_13.setText(f"Failed to retrieve weather alerts for {zipcode}")
        except requests.exceptions.RequestException as e:
            self.ui.label_13.setText(f"Error: {e}")

    def display_local_weather_map(self):
        try:
            # Load the local image and set it to the QLabel
            pixmap = QPixmap("weathermap2.png")
            self.ui.label_9.setPixmap(pixmap)
            self.ui.label_9.setScaledContents(True)
        except Exception as e:
            self.ui.label_9.setText(f"Error: {e}")
            print(f"Error displaying local map: {e}")  # Debug: Print error

    def show_profile(self):
        # Define what happens when the profile button is clicked
        self.ui.rightMenuContainer.expandMenu()
        self.ui.rightMenuPages.setCurrentIndex(0)  # Assuming the profile page is the first page in rightMenuPages
        self.ui.label_7.setText("Profile Information Updated")  # Update profile information for demo purposes

    def show_more_menu(self):
        # Define what happens when the more menu button is clicked
        self.ui.rightMenuContainer.expandMenu()
        self.ui.rightMenuPages.setCurrentIndex(1)  # Assuming the more menu page is the second page in rightMenuPages


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################
