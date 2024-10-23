import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class EditorPage(QWidget):
    """Unfinished and not integrated: Page for editing flashcard set."""

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
