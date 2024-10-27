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

        self.layout = QVBoxLayout()

        # Title label
        self.layout.addWidget(QLabel("Revision Page"))
        self.updatestats()
        self.question_id = self.decide_next_question(self.stats)
        #self.question_id = 1
        # Placeholder for the current flashcard question
        self.flashcard_label = QLabel("Question:")
        self.flashcontent = MediaPlayer(self.question_id)

        self.show_answer_button = QPushButton("Show Answer")
        self.show_answer_button.clicked.connect(self.show_answer)
        self.is_showing_answer = False
        # Button to go back to Flashcards page
        back_flashcards_button = QPushButton("Back to Flashcards")
        back_flashcards_button.clicked.connect(switch_back_to_flashcards)

        # Add widgets to layout
        self.layout.addWidget(self.flashcard_label)
        self.layout.addWidget(self.flashcontent)
        self.layout.addWidget(self.show_answer_button)
        self.layout.addWidget(back_flashcards_button)

        self.setLayout(self.layout)

    
    def updatestats(self):
        try:
            with open("./current/stats.txt","r",encoding="utf-8") as f:
                self.stats = f.readlines()
        except:
            self.stats = []

    def update_content_shown(self,des_file,file_content,is_answer):
        with open(des_file,"r",encoding="utf-8") as f:
            self.layout.removeWidget(self.flashcontent)
            self.flashcontent.deleteLater()
            self.flashcard_label.setText(f"Quesntion {self.question_id}: {f.read()}")
            self.flashcontent = MediaPlayer(self.question_id,is_answer)
            self.layout.insertWidget(2,self.flashcontent)

    def show_answer(self):
        # Buttons for answering the flashcard,
        self.layout.removeWidget(self.show_answer_button)
        self.layout.removeWidget(self.flashcontent)
        self.show_answer_button.deleteLater()
        self.flashcontent.deleteLater()

        self.know_button = QPushButton("I Know the Answer")
        self.dont_know_button = QPushButton("I Don't Know the Answer")
        # Connect buttons to their respective functions
        self.know_button.clicked.connect(self.know_answer)
        self.dont_know_button.clicked.connect(self.dont_know_answer)
        # Button to show next question (placeholder functionality)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.know_button)
        self.buttons.addWidget(self.dont_know_button)
        self.is_showing_answer = True
        self.flashcontent = MediaPlayer(self.question_id,self.is_showing_answer)

        self.layout.insertWidget(2,self.flashcontent)
        self.layout.insertLayout(3,self.buttons)
        self.layout.update()

    def know_answer(self):
        """Handle the case when the user knows the answer."""
        QMessageBox.information(self, "Correct!", "Great job! You knew the answer!")
        #update stats.txt
        tem = self.stats[self.question_id-1].split(' ')
        self.stats[self.question_id-1] = f"{int(tem[0])+1} {int(tem[1])+1} {0} {True}\n"
        with open("./current/stats.txt","w",encoding="utf-8") as f:
            f.writelines(self.stats)
        #next question
        self.next_question()

    def dont_know_answer(self):
        """Handle the case when the user doesn't know the answer."""
        QMessageBox.information(self, "Keep Trying!", "No worries! Keep practicing.")
        # update stats.txt
        tem = self.stats[self.question_id - 1].split(' ')
        self.stats[self.question_id - 1] = f"{int(tem[0]) + 1} {int(tem[1])} {0} {False}\n"
        with open("./current/stats.txt", "w", encoding="utf-8") as f:
            f.writelines(self.stats)
        #next question
        self.next_question()

    def next_question(self):
        self.updatestats()
        self.is_showing_answer = False
        self.question_id = self.decide_next_question(self.stats)
        """Placeholder for showing the next question."""
        #know and don't know buttons deleted, show answer button appears
        #self.layout.removeItem(self.buttons)
        #self.buttons.deleteLater()
        while self.buttons.count():
            child = self.buttons.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.show_answer_button = QPushButton("Show Answer")
        self.show_answer_button.clicked.connect(self.show_answer)
        #update flashcontent
        self.layout.removeWidget(self.flashcontent)
        self.flashcontent.deleteLater()
        self.flashcontent = MediaPlayer(self.question_id,self.is_showing_answer)
        self.layout.insertWidget(3,self.show_answer_button)
        self.layout.insertWidget(2,self.flashcontent)
        self.layout.update()

        directory = "./current/flashcards"
        metadata = []
        '''with open("./current/metadata.txt","r",encoding="utf-8") as f:
            metadata = f.readlines()

        #the locations of the four files
        question_description_text = f"{directory}/{metadata[self.question_id * 2].split(':')[0]}"
        question_file = f"{directory}/{metadata[self.question_id * 2 + 1].split(':')[0]}"
        answer_description_text = f"{directory}/{metadata[self.question_id * 2].split(':')[1][:-1]}"
        answer_file = f"{directory}/{metadata[self.question_id * 2 + 1].split(':')[1][:-1]}"'''

        #QMessageBox.information(self, "Next Question", "Here would be the next question.")

    def decide_next_question(self,stats): #return the id of next_question
        # Define weights for priority calculation
        weight_seen = -0.3  # Weight for times seen, more seen -> lower priority
        weight_correct = -0.5  # Weight for correct answers, more correct -> lower priority
        weight_interval = 0.6  # Weight for interval since last seen, longer interval -> higher priority
        weight_last_correct = 1.0  # Weight for last answer correctness, incorrect last time -> higher priority

        max_priority = float('-inf')
        next_card_id = -1

        # Iterate through each flashcard
        for i in range(len(stats)):
            line = stats[i][0:-1].split(' ')
            seen_count = float(line[0])
            correct_count = float(line[1])
            interval = float(line[2])

            if(line[3] == "True"):#if last time is correct
                last_correct = 1
            else:
                last_correct = 0

            # Calculate priority score
            priority_score = (weight_seen * seen_count + weight_correct * correct_count +
            weight_interval * interval + weight_last_correct * (1 - last_correct))

            # Select the flashcard with the highest priority score
            if priority_score > max_priority:
                max_priority = priority_score
                next_card_id = i + 1  # Flashcard ID starts from 1, so add 1

        return next_card_id
        #return 2 