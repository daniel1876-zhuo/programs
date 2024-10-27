import sys
from zipfile import ZipFile
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
from menu import *
from flashcardmenu import *
# from statistic import *
from editor import *
from test import *

class MainWindow(QMainWindow):
    """Main window of the application that manages different pages."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard Application")

        # Create a stacked widget for page navigation
        self.stacked_widget = QStackedWidget()

        # Create instances of pages
        self.menu_page = MenuPage(
            self.create_flashcards,
            self.import_flashcards,
            None
            # self.show_statistics_page
        )
        self.flashcards_page = FlashcardsPage(
            self.show_add_flashcard_page,
            self.show_revision_page,
            self.show_menu_page,
        )
        self.add_flashcard_page = EditorPage(self.show_flashcards_page,self.refresheditor)
        
        self.revision_page = RevisionPage(
            self.show_flashcards_page,
            self.show_menu_page,
        )

        # self.statistics_page = StatisticsPage(self.show_menu_page)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.flashcards_page)
        self.stacked_widget.addWidget(self.add_flashcard_page)
        self.stacked_widget.addWidget(self.revision_page)
        # self.stacked_widget.addWidget(self.statistics_page)

        # Set the stacked widget as central widget
        self.setCentralWidget(self.stacked_widget)

    def create_flashcards(self):
        """copies empty template to ./current folder, then switches to flashcard menu"""
        path = "./current"
        try:
            shutil.rmtree(path)
        except:
            pass
        shutil.copytree("./New flashcards",path)
        self.stacked_widget.setCurrentWidget(self.flashcards_page)
        self.flashcards_page.updatetext()
        self.revision_page.updatestats()

    def import_flashcards(self):
        """User can upload flashcard and flashcards will be loaded to ./current"""
        try:
            file_name = QFileDialog.getOpenFileName(self, "Upload File", "", "Zip Files (*.zip);;All Files (*)")[0]
            try:
                shutil.rmtree("./unzip")
            except:
                pass
            os.mkdir("./unzip")
            with ZipFile(file_name, 'r') as zObject:
                zObject.extractall("./unzip")
            zipname = file_name[file_name.rfind("/")+1:-4]
            try:
                shutil.rmtree("./current")
            except:
                pass
            shutil.copytree("./unzip/"+zipname,"./current")
            self.stacked_widget.setCurrentWidget(self.flashcards_page)
            self.flashcards_page.updatetext()
            self.revision_page.updatestats()
            QMessageBox.information(self,"","Flashcards loaded!")
        except Exception as e:
            print(e)
            QMessageBox.information(self,"","Flashcards failed to load")

    def show_menu_page(self):
        """Switch to the menu page."""
        self.stacked_widget.setCurrentWidget(self.menu_page)

    def show_flashcards_page(self):
        """Switch to the flashcards page."""
        self.stacked_widget.setCurrentWidget(self.flashcards_page)

    def refresheditor(self):
        self.stacked_widget.setCurrentWidget(self.flashcards_page)
        self.add_flashcard_page.updatepage(self.show_flashcards_page,self.refresheditor)
        self.stacked_widget.setCurrentWidget(self.add_flashcard_page)

    def show_add_flashcard_page(self):
        self.add_flashcard_page.updatepage(self.show_flashcards_page,self.refresheditor)
        """Switch to the add flashcard page."""
        self.stacked_widget.setCurrentWidget(self.add_flashcard_page)


    def show_revision_page(self):
        """Switch to the revision page."""
        self.stacked_widget.setCurrentWidget(self.revision_page)


    # def show_statistics_page(self):
    #     """Switch to the statistics page."""
    #     self.stacked_widget.setCurrentWidget(self.statistics_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
