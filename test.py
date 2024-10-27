import sys,os,shutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

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

        # Placeholder for the current flashcard question
        self.flashcard_label = QLabel("Flashcard Question Here")

        # Buttons for answering the flashcard
        self.know_button = QPushButton("I Know the Answer")
        self.dont_know_button = QPushButton("I Don't Know the Answer")

        # Connect buttons to their respective functions

        self.know_button.clicked.connect(lambda:self.know_answer)
        self.dont_know_button.clicked.connect(lambda:self.dont_know_answer)

        # Button to go back to Flashcards page
        back_flashcards_button = QPushButton("Back to Flashcards")
        back_flashcards_button.clicked.connect(lambda:switch_back_to_flashcards)

        # Button to show next question (placeholder functionality)
        next_question_button = QPushButton("Next Question")
        next_question_button.clicked.connect(lambda:self.next_question)

        # Add widgets to layout
        self.layout.addWidget(self.flashcard_label)
        self.layout.addWidget(self.know_button)
        self.layout.addWidget(self.dont_know_button)
        self.layout.addWidget(back_flashcards_button)
        self.layout.addWidget(next_question_button)
        self.setLayout(self.layout)
        self.question_id = 0
    
    def updatestats(self):
        with open("./current/stats.txt","r",encoding="utf-8") as f:
            self.stats = f.readlines()


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
        question_id = self.decide_next_question(self.stats)
        """Placeholder for showing the next question."""

        directory = "./current/flashcards"
        metadata = []
        with open("./current/metadata.txt","r",encoding="utf-8") as f:
            metadata = f.readlines()

        #the locations of the four files
        question_description_text = f"{directory}/{metadata[question_id * 2].split(':')[0]}"
        question_file = f"{directory}/{metadata[question_id * 2 + 1].split(':')[0]}"
        answer_description_text = f"{directory}/{metadata[question_id * 2].split(':')[1][:-1]}"
        answer_file = f"{directory}/{metadata[question_id * 2 + 1].split(':')[1][:-1]}"
        
    """You may want to use string.endswith(suffix) that returns a boolean value indicating 
    whether the string ends with this suffix, in order to decide which function is used to render the flashcard"""

        #QMessageBox.information(self, "Next Question", "Here would be the next question.")

    def decide_next_question(self,stats): #return the id of next_question

        pass
