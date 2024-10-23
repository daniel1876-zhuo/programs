import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
## abcdef
class FlashcardsPage(QWidget):
    """Flashcards page with options to add new flashcards or start revision."""

    def __init__(self, switch_to_add_flashcard, switch_to_revision, switch_back_to_menu):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        layout.addWidget(QLabel("Flashcards"))

        # Button to add new flashcards
        add_flashcard_button = QPushButton("Add New Flashcards")
        add_flashcard_button.clicked.connect(switch_to_add_flashcard)
        layout.addWidget(add_flashcard_button)

        # Button to start revision
        start_revision_button = QPushButton("Start Revision")
        start_revision_button.clicked.connect(switch_to_revision)
        layout.addWidget(start_revision_button)

        # Button to go back to Menu page
        back_to_menu_button = QPushButton("Back to Menu")
        back_to_menu_button.clicked.connect(switch_back_to_menu)
        layout.addWidget(back_to_menu_button)

        self.setLayout(layout)

class AddFlashcardPage(QWidget):
    """Page for adding new flashcards."""

    def __init__(self, switch_back):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        layout.addWidget(QLabel("Add New Flashcard"))

        # Input for question
        self.question_input = QLabel("Enter your question:")

        # Button to upload a file (for questions)
        upload_button = QPushButton("Upload File")
        upload_button.clicked.connect(self.upload_file)

        # Button to go back to Flashcards page
        back_button = QPushButton("Back to Flashcards")
        back_button.clicked.connect(switch_back)

        layout.addWidget(self.question_input)
        layout.addWidget(upload_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def upload_file(self):
        """Open file dialog to upload a file containing questions."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload File", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)

        if file_name:
            QMessageBox.information(self, "File Uploaded", f"File {file_name} uploaded successfully!")


class RevisionPage(QWidget):
    """Page for revising flashcards."""

    def __init__(self, switch_back_to_flashcards, switch_back_to_menu):
        super().__init__()

        self.layout = QVBoxLayout()

        # Title label
        self.layout.addWidget(QLabel("Revision Page"))

        # Placeholder for the current flashcard question
        self.flashcard_label = QLabel("Flashcard Question Here")

        # Buttons for answering the flashcard
        self.know_button = QPushButton("I Know the Answer")
        self.dont_know_button = QPushButton("I Don't Know the Answer")

        # Connect buttons to their respective functions

        self.know_button.clicked.connect(self.know_answer)
        self.dont_know_button.clicked.connect(self.dont_know_answer)

        # Button to go back to Flashcards page
        back_flashcards_button = QPushButton("Back to Flashcards")
        back_flashcards_button.clicked.connect(switch_back_to_flashcards)

        # Button to show next question (placeholder functionality)
        next_question_button = QPushButton("Next Question")
        next_question_button.clicked.connect(self.next_question)

        # Add widgets to layout
        self.layout.addWidget(self.flashcard_label)
        self.layout.addWidget(self.know_button)
        self.layout.addWidget(self.dont_know_button)
        self.layout.addWidget(back_flashcards_button)
        self.layout.addWidget(next_question_button)

        self.setLayout(self.layout)


    def know_answer(self):
        """Handle the case when the user knows the answer."""
        QMessageBox.information(self, "Correct!", "Great job! You knew the answer!")


    def dont_know_answer(self):
        """Handle the case when the user doesn't know the answer."""
        QMessageBox.information(self, "Keep Trying!", "No worries! Keep practicing.")


    def next_question(self):
        """Placeholder for showing the next question."""
        QMessageBox.information(self, "Next Question", "Here would be the next question.")

'''
from menu import *

class add_flashcards(QWidget):
    def __init__(self):
        super().__init__()
        super().hide()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add New Flashcards")
        layout = QVBoxLayout()

        self.upload_button = QPushButton('Upload File')
        self.upload_button.clicked.connect(self.upload_file)

        layout.addWidget(self.upload_button)
        self.setLayout(layout)

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

class flashcards(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Flashcards")

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.HomePage = Home()
        self.AddFlashcards = add_flashcards()

        self.stacked_widget = QStackedWidget()

        self.stacked_widget.addWidget(self.HomePage)
        self.stacked_widget.addWidget(self.AddFlashcards)

        home_button = QPushButton("Go to Home")
        add_button = QPushButton("Add Flashcards")
        next_button = QPushButton("Next Flashcards")

        home_button.clicked.connect(self.show_home)
        add_button.clicked.connect(self.make_card)
        next_button.clicked.connect(self.show_card)

        layout.addWidget(QLabel("Flashcards"))
        layout.addWidget(add_button)
        layout.addWidget(next_button)
        #encapsulate stacked_widget in the central widget
        layout.addWidget(self.stacked_widget)

    def make_card(self):
        self.stacked_widget.setCurrentWidget(self.AddFlashcards)

    def show_card(self):
        pass

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.HomePage)

def answering():
    pass'''
