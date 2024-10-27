import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTextEdit,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget,QHBoxLayout
)
from PySide6.QtGui import(
    QAction,QTextDocument
)
from PySide6.QtCore import(
    Qt
)
from render import *

class EditorPage(QWidget):
    """
    Page for editing flashcard set.
    """
    def __init__(self, switch_back,refresh):
        super().__init__()
        self.currentflash = [1,False]
        self.ischanging = False

        self.Layout = QVBoxLayout()
        self.Layout2 = QVBoxLayout()
        self.realLayout = QHBoxLayout()
        self.toplabel = QLabel("Currently showing flashcard")

        self.minilayout = QHBoxLayout()
        self.prevbutton = QPushButton("Show Previous")
        self.prevbutton.clicked.connect(lambda : self.changeflash(self.currentflash[0]-1))
        self.minilayout.addWidget(self.prevbutton)
        self.flashnum = QLabel(str(self.currentflash[0]))
        self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.change = QPushButton("Show Answer")
        self.change.clicked.connect(self.showans)
        self.minilayout.addWidget(self.change)
        self.nextbutton = QPushButton("Show Next")
        self.nextbutton.clicked.connect(lambda : self.changeflash(self.currentflash[0]+1))
        self.minilayout.addWidget(self.nextbutton)
        self.Layout.addWidget(self.toplabel)
        self.Layout.addWidget(self.flashnum)

        self.Layout.addLayout(self.minilayout)
        self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1])
        self.Layout.addWidget(self.flashrender)
        self.title = QLabel("Replace this flashcard")
        self.Layout2.addWidget(self.title)
        self.replace_question_and_answer(refresh)
        self.title2 = QLabel("Add new flashcard")
        self.Layout2.addWidget(self.title2)

        self.upload_question_and_answer(refresh)

        self.rem_button = QPushButton("Remove this flashcard (doesn't work yet)")
        self.rem_button.clicked.connect(None)
        self.Layout2.addWidget(self.rem_button)

        self.title3 = QLabel("Rename this flashcard (doesn't work yet)")
        self.Layout2.addWidget(self.title3)

        self.renameinput = QTextEdit()
        self.Layout2.addWidget(self.renameinput)

        self.back_button = QPushButton("Back to Flashcards")
        self.back_button.clicked.connect(switch_back)
        self.Layout2.addWidget(self.back_button)

        self.realLayout.addLayout(self.Layout)
        self.realLayout.addLayout(self.Layout2)
        self.setLayout(self.realLayout)

    def upload_file(self):
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
    
    def replace_file(self):
        file = QFileDialog.getOpenFileName(self, "Select Multimedia Files", "",
                                           "Text(*.txt;*.doc;*.docx);;Images (*.png;*.jpg;*.jpeg);;Audio (*.mp3;*.wav);;Videos (*.mp4;*.avi)")
        if file[0]:
            print(file)
            target_directory = "./current/flashcards"
            file_suffix = file[0].split(".")[-1] #the file suffix
            if self.is_question2:
                self.question_file_path2 = f"{target_directory}/{str(self.currentflash[0])}_file.{file_suffix}"
            else:
                self.answer_file_path2 = f"{target_directory}/{str(self.currentflash[0])}_answer_file.{file_suffix}"
            try:
                if self.is_question2:
                    # Copy the file to the target location
                    shutil.copy(file[0], self.question_file_path2)
                    print(f"File copied to: {self.question_file_path2}")
                    self.is_uploaded = True
                else:
                    shutil.copy(file[0], self.answer_file_path2)
                    print(f"File copied to: {self.answer_file_path2}")
                    self.is_ans_uploaded = True
            except Exception as e:
                print(f"Error while copying the file: {e}")

    def submit(self,refresh):
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
            refresh()

    def replacesubmit(self,refresh):
        if self.is_question2:
            target_directory = "./current/flashcards"
            #create the description file
            target_path = f"{target_directory}/{self.currentflash[0]}"
            with open(f"{target_path}_des.txt","w",encoding="utf-8") as f:
                f.write(self.question_input2.toPlainText())

            self.ischanging = True
            self.is_question2 = False
            self.question_label2.setText("Replace your answer's descrption (If Any):")
            try:
                with open("./current/flashcards/"+str(self.currentflash[0])+"_answer_des.txt","r") as f:
                    self.question_input2.setPlainText("".join(f.readlines()))
            except:
                pass
        else:
            target_directory = "./current/flashcards"
            # create the description file
            target_path = f"{target_directory}/{self.currentflash[0]}"#_answer_des.txt""

            with open(f"{target_path}_answer_des.txt", "w", encoding="utf-8") as f:
                f.write(self.question_input2.toPlainText())

            # read the metadata
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                self.metatext = f.readlines()
            # adding question file
            with open("./current/metadata.txt", "w", encoding="utf-8") as f:
                filenames = self.metatext[1+self.currentflash[0]].split(":")
                if self.is_uploaded == True:
                    filenames[0] = self.question_file_path2.split('/')[-1]
                if self.is_ans_uploaded == True:
                    filenames[1] = self.answer_file_path2.split('/')[-1]
                self.metatext[1+self.currentflash[0]] = filenames[0]+':'+filenames[1]
                f.writelines(self.metatext)
            self.ischanging = False
            refresh()


    def change_from_question_to_answer(self):
        self.is_question = False
        self.question_label.setText("Enter your answer's descrption (If Any):")
        self.question_input.clear()
        # self.Layout2.update()
        # self.layout().update()

    def upload_question_and_answer(self,refresh):
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
        try:
            self.question_file_path = str(self.file_id)+"_file.txt"
            self.answer_file_path = str(self.file_id)+"_answer_file.txt"
        except: ##initialize
            pass
        self.is_question = True
        self.upload_button = QPushButton("Upload File (If Any):")
        self.upload_button.clicked.connect(lambda:self.upload_file())

        # Button to submit
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(lambda:self.submit(refresh))

        # Button to go back to Flashcards page

        self.Layout2.addWidget(self.question_label)
        self.Layout2.addWidget(self.question_input)
        self.Layout2.addWidget(self.upload_button)
        self.Layout2.addWidget(self.submit_button)
    
    def replace_question_and_answer(self,refresh):
        try:
            self.question_file_path2 = f"./current/flashcards/{str(self.currentflash[0])}_file.txt"
            self.answer_file_path2 = f"./current/flashcards/{str(self.currentflash[0])}_answer_file.txt"
        except Exception as e: #shouldn't trigger
            print(e)
        # Input for question's description
        self.question_label2 = QLabel("Replace your question's description (If Any):")
        self.question_input2 = QTextEdit()
        try:
            with open("./current/flashcards/"+str(self.currentflash[0])+"_des.txt","r") as f:
                self.question_input2.setPlainText("".join(f.readlines()))
                # self.Layout2.update()
                # self.layout().update()
        except:
            pass


        # Button to upload a file (for questions)
        self.is_uploaded = False
        self.is_ans_uploaded = False
        self.question_file_path2 = str(self.currentflash[0])+"_file.txt"
        self.answer_file_path2 = str(self.currentflash[0])+"_answer_file.txt"
        self.is_question2 = True
        self.upload_button2 = QPushButton("Replace File (If Any):")
        self.upload_button2.clicked.connect(lambda:self.replace_file())

        # Button to submit
        self.submit_button2 = QPushButton("Submit")
        self.submit_button2.clicked.connect(lambda:self.replacesubmit(refresh))

        self.Layout2.addWidget(self.question_label2)
        self.Layout2.addWidget(self.question_input2)
        self.Layout2.addWidget(self.upload_button2)
        self.Layout2.addWidget(self.submit_button2)


    def clearLayout(self, layout): ##code taken from https://stackoverflow.com/questions/9374063/remove-all-items-from-a-layout"
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
    
    def updatepage(self,switch_back,refresh): # update file fetching when flashcards loaded

        ## implementation here is a bit awkward but it works for now
        self.Layout.removeWidget(self.flashrender)
        self.Layout2.removeWidget(self.title)
        self.Layout2.removeWidget(self.question_label)
        self.Layout2.removeWidget(self.question_input)
        self.Layout2.removeWidget(self.upload_button)
        self.Layout2.removeWidget(self.submit_button)
        self.Layout2.removeWidget(self.back_button)
        self.Layout2.removeWidget(self.question_label2)
        self.Layout2.removeWidget(self.question_input2)
        self.Layout2.removeWidget(self.upload_button2)
        self.Layout2.removeWidget(self.submit_button2)
        self.Layout.removeWidget(self.toplabel)
        self.Layout.removeWidget(self.flashnum)
        self.Layout2.removeWidget(self.title2)
        self.Layout2.removeWidget(self.rem_button)
        self.Layout2.removeWidget(self.title3)
        self.Layout2.removeWidget(self.renameinput)
        self.question_label.deleteLater()
        self.question_input.deleteLater()
        self.upload_button.deleteLater()
        self.back_button.deleteLater()
        self.submit_button.deleteLater()
        self.question_label2.deleteLater()
        self.question_input2.deleteLater()
        self.upload_button2.deleteLater()
        self.submit_button2.deleteLater()
        self.toplabel.deleteLater()
        self.flashnum.deleteLater()
        '''while self.flashrender.count():
            child = self.flashrender.takeAt(0)
            if child.widget():
                child.widget().deleteLater()'''
        self.flashrender.deleteLater()
        self.title.deleteLater()
        self.title2.deleteLater()
        self.title3.deleteLater()
        self.rem_button.deleteLater()
        self.renameinput.deleteLater()

        self.ischanging = False
        self.toplabel = QLabel("Currently showing flashcard")
        self.Layout.insertWidget(0,self.toplabel)
        self.flashnum = QLabel(str(self.currentflash[0]))
        self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Layout.insertWidget(1,self.flashnum)
        self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1])
        self.Layout.addWidget(self.flashrender)
        self.title = QLabel("Replace this flashcard")
        self.Layout2.addWidget(self.title)
        self.replace_question_and_answer(refresh)
        self.title2 = QLabel("Add new flashcard")
        self.Layout2.addWidget(self.title2)
        self.upload_question_and_answer(refresh)

        self.rem_button = QPushButton("Remove this flashcard (doesn't work yet)")
        self.rem_button.clicked.connect(None)
        self.Layout2.addWidget(self.rem_button)

        self.title3 = QLabel("Rename this flashcard (doesn't work yet)")
        self.Layout2.addWidget(self.title3)

        self.renameinput = QTextEdit()
        self.Layout2.addWidget(self.renameinput)

        self.back_button = QPushButton("Back to Flashcards")
        self.back_button.clicked.connect(switch_back)
        self.Layout2.addWidget(self.back_button)

        self.Layout.update()
        self.Layout2.update()
        self.layout().update()

    def showans(self):
        if self.currentflash[1]: ##currently answer, need to show question
            self.minilayout.removeWidget(self.change)
            self.change.deleteLater()
            self.currentflash[1] = False
            self.change = QPushButton("Show Answer")
            self.change.clicked.connect(self.showans)
            self.minilayout.insertWidget(1,self.change)
            self.minilayout.update()
            '''while self.flashrender.count():
                child = self.flashrender.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()'''
            self.flashrender.deleteLater()
            self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1])
            self.Layout.insertWidget(3,self.flashrender)
            self.layout().update()
        else:  ##currently question, need to show answer
            self.minilayout.removeWidget(self.change)
            self.change.deleteLater()
            self.currentflash[1] = True
            self.change = QPushButton("Show Question")
            self.change.clicked.connect(self.showans)
            self.minilayout.insertWidget(1,self.change)
            self.minilayout.update()
            '''while self.flashrender.count():
                child = self.flashrender.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()'''
            self.flashrender.deleteLater()
            self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1])
            self.Layout.insertWidget(3,self.flashrender)
            self.layout().update()

    def changeflash(self,newflashnum):
        if not self.ischanging:
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                totalnum = int(f.readlines()[1][0:-1])
            if newflashnum == 0:
                newflashnum = totalnum
            if newflashnum == totalnum+1:
                newflashnum = 1
            self.minilayout.removeWidget(self.change)
            self.change.deleteLater()
            self.currentflash[1] = False
            self.currentflash[0] = newflashnum
            self.change = QPushButton("Show Answer")
            self.change.clicked.connect(self.showans)
            self.minilayout.insertWidget(1,self.change)

            self.Layout.removeWidget(self.flashnum)
            self.flashnum.deleteLater()
            self.flashnum = QLabel(str(self.currentflash[0]))
            self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.Layout.insertWidget(1,self.flashnum)

            '''while self.flashrender.count():
                    child = self.flashrender.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()'''
            self.flashrender.deleteLater()
            self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1])
            self.Layout.insertWidget(3,self.flashrender)
            self.minilayout.update()
            try:
                with open("./current/flashcards/"+str(self.currentflash[0])+"_des.txt","r") as f:
                    self.question_input2.setPlainText("".join(f.readlines()))
            except:
                pass
            self.layout().update()
            
            
