########################################################################
## IMPORTS
########################################################################
import sys

from PyQt5.QtWidgets import QApplication
from PySide2 import *

########################################################################
# IMPORT GUI FILE
from ui_interface2 import *
########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *


########################################################################


########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        loadJsonStyle(self, self.ui)
        ########################################################################

        ########################################################################

        self.show()

        self.ui.settingsButton.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpButton.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())

        self.ui.closeCenterMenuButton.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())

        self.ui.moreMenuButton.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profileMenuButton.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())

        self.ui.closeRightMenuButton.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())

        self.ui.closeNotificationButton.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())


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
