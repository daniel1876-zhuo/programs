import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class StatisticsPage(QWidget):
    """Page for displaying statistics of answered questions."""

    def __init__(self, switch_back_to_menu):
        super().__init__()

        self.layout = QVBoxLayout()

        # Title label
        self.layout.addWidget(QLabel("Statistics"))

        # List widget to display accuracy of each question
        self.accuracy_list = QListWidget()

        # Sample data (to be replaced with actual data)
        sample_data = ["Question 1: 80%", "Question 2: 100%", "Question 3: 50%"]
        self.accuracy_list.addItems(sample_data)

        # Button to go back to Menu page
        back_menu_button = QPushButton("Back to Menu")
        back_menu_button.clicked.connect(switch_back_to_menu)

        # Add widgets to layout
        self.layout.addWidget(self.accuracy_list)
        self.layout.addWidget(back_menu_button)

        self.setLayout(self.layout)

'''
class statistics(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Statistics")

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(QLabel("Statistics"))

    def use_store_accuracy(self):
        return store_accuracy(self)

    def use_next_question(self):
        return next_question(self)

def next_question(list,accuracy):
    pass

def store_accuracy(id,is_correct):
    pass'''

