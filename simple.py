import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Weather Map Viewer")

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create QWebEngineView for the weather map
        self.weather_map_view = QWebEngineView()
        layout.addWidget(self.weather_map_view)

        # Load the URL
        url = "https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat=44.04449796443341&lon=-122.94003653926616&zoom=10&appid=5551bd31cc4373c66959543972ff9c67"
        self.weather_map_view.setUrl(QUrl(url))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
