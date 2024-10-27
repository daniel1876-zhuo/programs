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

    def __init__(self, createflash, importflash):
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

        # not implemented yet
        tutorial_button = QPushButton("Quick start")
        layout.addWidget(tutorial_button)

        self.setLayout(layout)


