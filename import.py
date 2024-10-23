import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class ImportFlashcard(QWidget):
    """Import flashcards"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        

