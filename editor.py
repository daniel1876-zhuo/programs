import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTextEdit,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
from PySide6.QtGui import(
    QAction,
)
from PySide6.QtCore import(
    Qt
)
from render import renderflashcard

class EditorPage(QWidget):
    """
    Page for editing flashcard set.
    On entry, the first flashcard question and answer in the loaded set should be rendered.
    Each flashcard can be either text, image, or video.
    The file name of the flashcard is stored in a created folder ./current/metadata.txt
    File format as follows:
    Row 1: name of flashcard set
    row 2: number of flashcards already exists
    Subsequent rows :
        row1:question description and answer description, separated by a colon ':'
        row2:question file name and answer file name, separated by a colon ':'
    e.g.
        string_question:string_answer
        q1.txt:a1.txt
    The actual flashcard files (text/image/video) is stored in ./current/flashcards/
    The user can switch between different flashcards.
    The user can upload a file to replace an original flashcard question or answer, or directly change it if it is a text file.
    The user can choose to close the editor, leading back to flashcardmenu.
    Any changes made by the user should be in the loaded flashcard set in ./current
    """

    def __init__(self, switch_back):
        super().__init__()
        self.Layout = QVBoxLayout()
        self.toplabel = QLabel("Currently showing flashcard")
        self.Layout.addWidget(self.toplabel)
        self.flashnum = QLabel("1")
        self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Layout.addWidget(self.flashnum)
        self.flashrender = renderflashcard(1)
        self.Layout.addLayout(self.flashrender)
        self.title = QLabel("Add New Flashcard")
        self.Layout.addWidget(self.title)

        self.upload_question_and_answer(switch_back)
        self.setLayout(self.Layout)

    def upload_file(self,switch_back):
        file = QFileDialog.getOpenFileName(self, "Select Multimedia Files", "",
                                           "Text(*.txt;*.doc;*.docx);;Images (*.png;*.jpg;*.jpeg);;Audio (*.mp3;*.wav);;Videos (*.mp4;*.avi)")
        if file[0]:
            print(file)
            target_directory = "./current/flashcards"
            file_suffix = file[0].split(".")[-1] #the file suffix
            if self.is_question:
                self.question_file_path = f"{target_directory}/{str(self.file_id)}_file.{file_suffix}"
            else:
                self.answer_file_path = f"{target_directory}/{str(self.file_id)}_answer_file.{file_suffix}"
            try:
                if self.is_question:
                    # Copy the file to the target location
                    shutil.copy(file[0], self.question_file_path)
                    print(f"File copied to: {self.question_file_path}")
                else:
                    shutil.copy(file[0], self.answer_file_path)
                    print(f"File copied to: {self.answer_file_path}")
            except Exception as e:
                print(f"Error while copying the file: {e}")

    def submit(self,switch_back):
        if self.is_question:
            target_directory = "./current/flashcards"
            #create the description file
            target_path = f"{target_directory}/{self.file_id}"
            with open(f"{target_path}_des.txt","w",encoding="utf-8") as f:
                f.write(self.question_input.toPlainText())

            self.change_from_question_to_answer()
        else:
            target_directory = "./current/flashcards"
            # create the description file
            target_path = f"{target_directory}/{self.file_id}"#_answer_des.txt""

            with open(f"{target_path}_answer_des.txt", "w", encoding="utf-8") as f:
                f.write(self.question_input.toPlainText())

            # read the metadata
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                self.metatext = f.readlines()
            # adding description file and question file
            with open("./current/metadata.txt", "w", encoding="utf-8") as f:
                self.metatext[1] = str(self.file_id)+"\n"
                self.metatext.append(f"{self.question_file_path.split('/')[-1]}:{self.answer_file_path.split('/')[-1]}\n")
                f.writelines(self.metatext)

            # update stats.txt, adding a new flashcard's data into it
            with open("./current/stats.txt","a",encoding="utf-8") as f:
                f.write(f"0 0 -1 {False}\n")
            self.file_id += 1  # increment number of flashcards by 1
            switch_back()


    def change_from_question_to_answer(self):
        self.is_question = False
        self.question_label.setText("Enter your answer's descrption (If Any):")
        self.question_input.clear()

    def upload_question_and_answer(self,switch_back):
        try:
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                self.file_id = int(f.readlines()[1][0:-1])#the index of the latest file added
            self.file_id += 1
            self.question_file_path = f"./current/flashcards/{str(self.file_id)}_file.txt"
            self.answer_file_path = f"./current/flashcards/{str(self.file_id)}_answer_file.txt"
        except Exception as e: #metadata likely doesn't exist yet, will repeat detection in updatepage()
            print(e)
        # Input for question's description
        self.question_label = QLabel("Enter your question's description (If Any):")
        self.question_input = QTextEdit()

        # Button to upload a file (for questions)
        self.is_question = True
        self.upload_button = QPushButton("Upload File (If Any):")
        self.upload_button.clicked.connect(self.upload_file)

        # Button to submit
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(lambda:self.submit(switch_back))

        # Button to go back to Flashcards page
        self.back_button = QPushButton("Back to Flashcards")
        self.back_button.clicked.connect(switch_back)

        self.Layout.addWidget(self.question_label)
        self.Layout.addWidget(self.question_input)
        self.Layout.addWidget(self.upload_button)
        self.Layout.addWidget(self.submit_button)
        self.Layout.addWidget(self.back_button)
    
    def updatepage(self, switch_back): # update file fetching when flashcards loaded

        ## implementation here is a bit awkward but it works for now
        self.layout().removeItem(self.flashrender)
        self.layout().removeWidget(self.title)
        self.Layout.removeWidget(self.question_label)
        self.Layout.removeWidget(self.question_input)
        self.Layout.removeWidget(self.upload_button)
        self.Layout.removeWidget(self.submit_button)
        self.Layout.removeWidget(self.back_button)
        self.Layout.removeWidget(self.toplabel)
        self.Layout.removeWidget(self.flashnum)
        self.question_label.deleteLater()
        self.question_input.deleteLater()
        self.upload_button.deleteLater()
        self.back_button.deleteLater()
        self.submit_button.deleteLater()
        self.toplabel.deleteLater()
        self.flashnum.deleteLater()
        while self.flashrender.count():
            child = self.flashrender.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.title.deleteLater()


        self.toplabel = QLabel("Currently showing flashcard")
        self.Layout.addWidget(self.toplabel)
        self.flashnum = QLabel("1")
        self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flashnum.setStyleSheet("background-color: rgb(50,50,50);")
        self.Layout.addWidget(self.flashnum)
        self.flashrender = renderflashcard(1)
        self.Layout.addLayout(self.flashrender)
        self.title = QLabel("Add New Flashcard")
        self.Layout.addWidget(self.title)
        self.upload_question_and_answer(switch_back)
        self.layout().update()


