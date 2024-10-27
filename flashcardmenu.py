import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class FlashcardsPage(QWidget):
    """Flashcards menu after import where you can edit, test, or save&close"""

    def __init__(self, switch_to_add_flashcard, switch_to_revision, switch_back_to_menu,switch_to_statistics):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        layout.addWidget(QLabel("Flashcards"))

        #Text that will be updated to show loaded flashcard set
        self.label = QLabel("Loaded: None")
        layout.addWidget(self.label)

        # Button to open editor
        add_flashcard_button = QPushButton("Edit flashcards")
        add_flashcard_button.clicked.connect(switch_to_add_flashcard)
        layout.addWidget(add_flashcard_button)

        # Button to open test
        start_revision_button = QPushButton("Start Revision")
        start_revision_button.clicked.connect(switch_to_revision)
        layout.addWidget(start_revision_button)

        statistics_button = QPushButton("Show statistics")
        statistics_button.clicked.connect(switch_to_statistics)
        layout.addWidget(statistics_button)

        # Button to go back to Menu page
        back_to_menu_button = QPushButton("Save to program-mains/stored folder")
        back_to_menu_button.clicked.connect(switch_back_to_menu)
        layout.addWidget(back_to_menu_button)

        self.setLayout(layout)

    def updatetext(self):
        f = open("./current/metadata.txt","r")
        name = f.readline()
        f.close()
        self.layout().removeWidget(self.label)
        self.label.deleteLater()
        self.label = QLabel("Loaded: "+name)
        self.layout().insertWidget(1,self.label)
        self.layout().update()
