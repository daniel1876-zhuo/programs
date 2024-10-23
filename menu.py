import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
from flashcard import *
from statistic import *
from Functions import *
class MenuPage(QWidget):
    """Menu page with options to navigate to Flashcards or Statistics."""

    def __init__(self, switch_to_flashcards, switch_to_statistics):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        layout.addWidget(QLabel("Welcome to the Flashcard App"))

        # Button to go to Flashcards
        flashcards_button = QPushButton("Flashcards")
        flashcards_button.clicked.connect(switch_to_flashcards)
        layout.addWidget(flashcards_button)

        # Button for Statistics
        statistics_button = QPushButton("Statistics")
        statistics_button.clicked.connect(switch_to_statistics)
        layout.addWidget(statistics_button)

        self.setLayout(layout)
        self.initMenus()

    def initMenus(self):#you can temporarily disable this function 
        # Create the stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        self.layout().addWidget(self.stacked_widget)

        # Create pages and add them to the stacked widget
        self.FlashcardPage = FlashcardsPage(show_add_flashcard_page,show_revision_page,show_menu_page)
        self.StatisticPage = StatisticsPage(show_menu_page)

        self.stacked_widget.addWidget(self.FlashcardPage)
        self.stacked_widget.addWidget(self.StatisticPage)

        Menu = QMainWindow.menuBar()
        menu = Menu.addMenu("File")  # create menu bar
        # Create actions for the menu
        go_to_flashcard = QMainWindow.QAction("Flashcards", self)
        go_to_statistics = QMainWindow.QAction("Statistics", self)

        go_to_flashcard.triggered.connect(self.show_flashcards)
        go_to_statistics.triggered.connect(self.show_statistics)

        # Add actions to the File menu
        menu.addAction(go_to_flashcard)
        menu.addAction(go_to_statistics)


