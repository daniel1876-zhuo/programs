from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QFileDialog,
    QLabel,
    QMainWindow,
    QStackedWidget,
)
import os,shutil
from menu import *

class add_flashcards(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.upload_button = QPushButton('Upload File')
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

class flashcards(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Flashcards")

    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.HomePage = Home()
        self.AddFlash
        self.stacked_widget.addWidget(self.HomePage)

        home_button = QPushButton("Go to Home")
        add_button = QPushButton("Add Flashcards")
        next_button = QPushButton("Next Flashcards")

        home_button.clicked.connect(self.show_home)
        add_button.clicked.connect(self.make_card)
        next_button.clicked.connect(self.show_card)

        self.layout.addWidget(QLabel("Flashcards"))
        self.layout.addWidget(add_button)
        self.layout.addWidget(next_button)

    def upload_file(self):
        file = QFileDialog.getOpenFileName(self,"Select Multimedia Files", "","Text(*.txt;*.doc;*.docx);;Images (*.png;*.jpg;*.jpeg);;Audio (*.mp3;*.wav);;Videos (*.mp4;*.avi)")
        if file:
            target_directory = "./questions"
            file_name_only = file[0].split("/")[-1]
            target_path = f"{target_directory}/{file_name_only}"
            if os.path.isdir(target_directory) == False:
                os.mkdir(target_directory)
            try:
                # Copy the file to the target location
                shutil.copy(file[0], target_path)
                print(f"File copied to: {target_path}")
            except Exception as e:
                print(f"Error while copying the file: {e}")

    def make_card(self):
        self.stacked_widget.setCurrentWidget(self.)


    def show_card(self):
        pass

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.HomePage)

def answering():
    pass