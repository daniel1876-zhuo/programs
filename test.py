import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class RevisionPage(QWidget):
    """Unfinished and unintegrated: Page for revising flashcards."""

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
