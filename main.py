import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
from menu import *
from flashcard import *
from statistic import *


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
