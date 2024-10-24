import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class EditorPage(QWidget):
    """
    Page for editing flashcard set.
    On entry, the first flashcard in the loaded set should be rendered.
    Each flashcard can be either text, image, or video.
    The file name of the flashcard is stored in a created folder ./current/metadata.txt
    with the first row being the name of the set, and the next rows being the names of flashcard files (e.g. q1.txt).
    The actual flashcard files (text/image/video) is stored in ./current/flashcards/
    The user can switch between different flashcards.
    The user can upload a file to replace an original flashcard file, or directly change it if it is a text file.
    The user can choose to close the editor, leading back to flashcardmenu.
    Any changes made by the usershould be in the loaded flashcard set in ./current
    """

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
