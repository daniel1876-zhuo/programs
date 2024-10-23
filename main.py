import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class MenuPage(QWidget):
    """Menu page with options to navigate to Flashcards or Statistics."""

    def __init__(self, switch_to_flashcards, switch_to_statistics):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        layout.addWidget(QLabel("Welcome to the Flashcard App"))

        # Button to go to Flashcards
        flashcards_button = QPushButton("Flashcards")
        flashcards_button.clicked.connect(switch_to_flashcards)
        layout.addWidget(flashcards_button)

        # Button for Statistics
        statistics_button = QPushButton("Statistics")
        statistics_button.clicked.connect(switch_to_statistics)
        layout.addWidget(statistics_button)

        self.setLayout(layout)


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


class MainWindow(QMainWindow):
    """Main window of the application that manages different pages."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard Application")

        # Create a stacked widget for page navigation
        self.stacked_widget = QStackedWidget()

        # Create instances of pages
        self.menu_page = MenuPage(self.show_flashcards_page, self.show_statistics_page)
        self.flashcards_page = FlashcardsPage(
            self.show_add_flashcard_page,
            self.show_revision_page,
            self.show_menu_page,
        )
        self.add_flashcard_page = AddFlashcardPage(self.show_flashcards_page)
        self.revision_page = RevisionPage(
            self.show_flashcards_page,
            self.show_menu_page,
        )

        self.statistics_page = StatisticsPage(self.show_menu_page)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.flashcards_page)
        self.stacked_widget.addWidget(self.add_flashcard_page)
        self.stacked_widget.addWidget(self.revision_page)
        self.stacked_widget.addWidget(self.statistics_page)

        # Set the stacked widget as central widget
        self.setCentralWidget(self.stacked_widget)


    def show_menu_page(self):
        """Switch to the menu page."""
        self.stacked_widget.setCurrentWidget(self.menu_page)


    def show_flashcards_page(self):
        """Switch to the flashcards page."""
        self.stacked_widget.setCurrentWidget(self.flashcards_page)


    def show_add_flashcard_page(self):
        """Switch to the add flashcard page."""
        self.stacked_widget.setCurrentWidget(self.add_flashcard_page)


    def show_revision_page(self):
        """Switch to the revision page."""
        self.stacked_widget.setCurrentWidget(self.revision_page)


    def show_statistics_page(self):
        """Switch to the statistics page."""
        self.stacked_widget.setCurrentWidget(self.statistics_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
