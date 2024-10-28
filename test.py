#import packages
import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)
from render import *
class RevisionPage(QWidget):
    """
    Page for revising flashcards.
    A weight should be calculated for each flashcard. This weight determines how often the flashcard comes up,
    and should be calculated using user statistics (correct rate, time since last seen, etc.) stored in
    the flashcard statistics file ./current/stats.txt

    The file format for stats.txt is: one row for each flashcard, each row has 4 numbers separated by spaces.
    4 numbers are: Number of times shown, Number of correct answers, flashcards since last seen, and whether
    the last answer was correct or not.

    A random flashcard (determined by weight) should be repeatedly rendered, and the user can click to see the answer.
    The answer would be shown, and the user can select if they are correct or not. Relevant statistics should be updated
    in stats.txt .

    The user can click a button to exit back to the flashcardmenu.
    """

    def __init__(self, switch_back_to_flashcards, switch_back_to_menu):
        super().__init__()

        #set up the layout of the page
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Revision Page"))

        #update statistics and decide next question
        self.updatestats()
        self.question_id = self.decide_next_question(self.stats)
        self.flashcard_label = QLabel("Question:")
        self.flashcontent = MediaPlayer(self.question_id)

        #buttons in the page
        self.show_answer_button = QPushButton("Show Answer")
        self.show_answer_button.clicked.connect(self.show_answer)
        self.is_showing_answer = False
        back_flashcards_button = QPushButton("Back to Flashcards")
        back_flashcards_button.clicked.connect(switch_back_to_flashcards)

        #add widgets to the layout
        self.layout.addWidget(self.flashcard_label)
        self.layout.addWidget(self.flashcontent)
        self.layout.addWidget(self.show_answer_button)
        self.layout.addWidget(back_flashcards_button)

        self.setLayout(self.layout)


    def updatestats(self):
        #load statistics
        try:
            with open("./current/stats.txt","r",encoding="utf-8") as f:
                self.stats = f.readlines()
        except:
            self.stats = []

    def update_content_shown(self,des_file,file_content,is_answer):
        #display current flashcard
        with open(des_file,"r",encoding="utf-8") as f:
            self.layout.removeWidget(self.flashcontent)
            self.flashcontent.deleteLater()
            self.flashcard_label.setText(f"Quesntion {self.question_id}: {f.read()}")
            self.flashcontent = MediaPlayer(self.question_id,is_answer)
            self.layout.insertWidget(2,self.flashcontent)

    def show_answer(self):
        #show the answer
        self.layout.removeWidget(self.show_answer_button)
        self.layout.removeWidget(self.flashcontent)
        self.show_answer_button.deleteLater()
        self.flashcontent.deleteLater()

        #let the user indicate whether they know the answer of not
        self.know_button = QPushButton("I Know the Answer")
        self.dont_know_button = QPushButton("I Don't Know the Answer")
        self.know_button.clicked.connect(self.know_answer)
        self.dont_know_button.clicked.connect(self.dont_know_answer)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.know_button)
        self.buttons.addWidget(self.dont_know_button)
        self.is_showing_answer = True
        self.flashcontent = MediaPlayer(self.question_id,self.is_showing_answer)
        self.layout.insertWidget(2,self.flashcontent)
        self.layout.insertLayout(3,self.buttons)
        self.layout.update()

    def know_answer(self):
        #case when the user knows the answer, update statistics and load next question
        QMessageBox.information(self, "Correct!", "Great job! You knew the answer!")
        tem = self.stats[self.question_id-1].split(' ')
        self.stats[self.question_id-1] = f"{int(tem[0])+1} {int(tem[1])+1} {0} {True}\n"
        with open("./current/stats.txt","w",encoding="utf-8") as f:
            f.writelines(self.stats)
        self.next_question()

    def dont_know_answer(self):
        #case when the user doesn't know the answer, update statistics and load next question
        QMessageBox.information(self, "Keep Trying!", "No worries! Keep practicing.")
        tem = self.stats[self.question_id - 1].split(' ')
        self.stats[self.question_id - 1] = f"{int(tem[0]) + 1} {int(tem[1])} {0} {False}\n"
        with open("./current/stats.txt", "w", encoding="utf-8") as f:
            f.writelines(self.stats)
        self.next_question()

    def next_question(self):
        #update statistics and select next question
        self.updatestats()
        self.is_showing_answer = False
        self.question_id = self.decide_next_question(self.stats)
        
        #update the buttons
        while self.buttons.count():
            child = self.buttons.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.show_answer_button = QPushButton("Show Answer")
        self.show_answer_button.clicked.connect(self.show_answer)

        #update the display
        self.layout.removeWidget(self.flashcontent)
        self.flashcontent.deleteLater()
        self.flashcontent = MediaPlayer(self.question_id,self.is_showing_answer)
        self.layout.insertWidget(3,self.show_answer_button)
        self.layout.insertWidget(2,self.flashcontent)
        self.layout.update()

        directory = "./current/flashcards"
        metadata = []

    def decide_next_question(self,stats): 
        #decide the next question using weighting, considering forgetting curve
        weight_seen = -0.3  
        weight_correct = -0.5  
        weight_interval = 0.6  
        weight_last_correct = 1.0  
        max_priority = float('-inf')
        next_card_id = -1

        #calculate priority score of flashcards
        for i in range(len(stats)):
            line = stats[i][0:-1].split(' ')
            seen_count = float(line[0])
            correct_count = float(line[1])
            interval = float(line[2])
            if(line[3] == "True"):
                last_correct = 1
            else:
                last_correct = 0
            priority_score = (weight_seen * seen_count + weight_correct * correct_count +
            weight_interval * interval + weight_last_correct * (1 - last_correct))

            #decide next flashcard to be the flashcard with highest priority score
            if priority_score > max_priority:
                max_priority = priority_score
                next_card_id = i + 1 
        return next_card_id
