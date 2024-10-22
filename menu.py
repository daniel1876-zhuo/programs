import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QStackedWidget,
    QMainWindow,
    QToolBar,
    QStatusBar,
)
from PySide6.QtGui import QAction, QIcon
from flashcard import *
from statistic import *

class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(QLabel("Home"))


class App(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setWindowTitle('Flashcards app')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.initMenus()

    def initMenus(self):
        # Create the stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages and add them to the stacked widget
        self.FlashcardPage = flashcards()
        self.StatisticPage = statistics()
        self.HomePage = Home()

        self.stacked_widget.addWidget(self.FlashcardPage)
        self.stacked_widget.addWidget(self.StatisticPage)
        self.stacked_widget.addWidget(self.HomePage)

        menu = self.menuBar().addMenu("File") #create menu bar
        # Create actions for the menu
        go_to_flashcard = QAction("Flashcards", self)
        go_to_statistics = QAction("Statistics", self)
        go_to_home = QAction("Home", self)

        go_to_flashcard.triggered.connect(self.show_flashcards)
        go_to_statistics.triggered.connect(self.show_statistics)
        go_to_home.triggered.connect(self.show_home)

        # Add actions to the File menu
        menu.addAction(go_to_flashcard)
        menu.addAction(go_to_statistics)
        menu.addAction(go_to_home)
        #menubar
#------------------------------------------------------------------------------------------------------------------------------------
        #toolbar
        toolbar = QToolBar("Menus")
        self.addToolBar(toolbar)
        go_to_flashcard_toolbar = QAction("Flashcards",self)
        go_to_flashcard_toolbar.setStatusTip("Go to Flashcards")

        go_to_statistics_toolbar = QAction("Statistics", self)
        go_to_statistics_toolbar.setStatusTip("Go to Statistics")

        go_to_home_toolbar = QAction("Home",self)
        go_to_home_toolbar.setStatusTip("Go to Home")

        go_to_flashcard_toolbar.triggered.connect(self.show_flashcards)
        go_to_statistics_toolbar.triggered.connect(self.show_statistics)
        go_to_home_toolbar.triggered.connect(self.show_home)

        toolbar.addAction(go_to_statistics_toolbar)
        toolbar.addAction(go_to_flashcard_toolbar)
        toolbar.addAction(go_to_home_toolbar)

        self.setStatusBar(QStatusBar(self))

    def show_flashcards(self):
        self.stacked_widget.setCurrentWidget(self.FlashcardPage)

    def show_statistics(self):
        self.stacked_widget.setCurrentWidget(self.StatisticPage)

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.HomePage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.initUI()
    window.show()
    app.exec()
