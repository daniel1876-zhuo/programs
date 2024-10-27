import os.path
import sys
from zipfile import ZipFile,ZIP_DEFLATED
import pathlib
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
from menu import *
from flashcardmenu import *
from statistic import *
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
            self.show_statistics_page
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

        self.statistics_page = StatisticsPage(self.show_menu_page)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.flashcards_page)
        self.stacked_widget.addWidget(self.add_flashcard_page)
        self.stacked_widget.addWidget(self.revision_page)
        self.stacked_widget.addWidget(self.statistics_page)
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

    def saveall(self): #save to ./stored
        if(os.path.isdir("./stored") == False):
            os.mkdir("./stored")
        try:
            with open("./current/metadata.txt","r",encoding="utf-8") as f:
                target_name = f.readlines()[0][0:-1]
        except:
            target_name = "unnamed_folder"
        target_path = "./stored/"
        target_path_id = 1

        if(os.path.exists(f"{target_path}{target_name}.zip") == True):
            while True:
                if os.path.exists(f"./stored/{target_name}_{target_path_id}.zip") == True:
                    target_path_id += 1
                else:
                    break
            target_name = f"{target_name}_{target_path_id}.zip"
        else:
            target_name = f"{target_name}.zip"

        target_path = f"{target_path}{target_name}"
        print(target_path,"is the location the zip stores")
        print("is file already existed:",os.path.exists(target_path))
        if os.path.isdir("./current"):
            folder = pathlib.Path("./current")
            with ZipFile(target_path,"w",ZIP_DEFLATED) as zip:
                for file in folder.rglob('*'):
                    print(file.name,"is being zipped as a part of the zip file")
                    zip.write(file,file.relative_to(folder.parent))

    def show_menu_page(self):
        """Switch to the menu page."""
        self.saveall()
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

    def show_statistics_page(self):
        """Switch to the statistics page."""
        self.stacked_widget.setCurrentWidget(self.statistics_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
