import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
from flashcardmenu import *
from statistic import *
# from Functions import *
class MenuPage(QWidget):
    """Menu page with options to Open flashcards, create flashcards or view statistics."""

    def __init__(self, createflash, importflash, switch_to_statistics):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        layout.addWidget(QLabel("Welcome to the Flashcard App"))

        # Button to import flashcards
        import_button = QPushButton("Open flashcards")
        import_button.clicked.connect(importflash)
        layout.addWidget(import_button)

        # Button to create flashcards
        create_button = QPushButton("Create flashcards")
        create_button.clicked.connect(createflash)
        layout.addWidget(create_button)

        # Button for Statistics
        statistics_button = QPushButton("Statistics")
        statistics_button.clicked.connect(switch_to_statistics)
        layout.addWidget(statistics_button)

        self.setLayout(layout)

    ## removed menubar related things because it is not working
    ## and we likely won't need it either
    ## so ¯\_(ツ)_/¯

