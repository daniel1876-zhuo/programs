import os.path
import shutil
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QFrame, QScrollArea, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget
)

class StatisticsPage(QWidget):
    """
    Page for displaying statistics of answered questions.
    This page should be moved after flashcardmenu (the main menu should only be open,create,tutorial, and after
    a flashcard is loaded the statistics page is given as an option along edit and start revision.

    The stats of loaded flashcards will be stored in a newly created folder ./current/stats.txt
    stats.txt stores statistics for each flashcard in the loaded set in rows, one in each row
    each row consists of four numbers separated by spaces: number of times flashcard has been seen,
    number of correct answers, how many flashcards ago has this flashcard been seen, and whether the user submitted
    a correct answer the last time they answered.
    """

    def __init__(self, switch_back_to_menu):
        super().__init__()

        self.Layout = QVBoxLayout()

        # Title label
        self.title = QLabel("Statistics")
        self.Layout.addWidget(self.title)

        # List widget to display accuracy of each question
        self.frame = QFrame()
        #accuracy_list is embedded in self.scroll_area, so no need to self.Layout.addWidget(self.accuracy_list)
        self.accuracy_list = QVBoxLayout(self.frame)
        # Sample data (to be replaced with actual data)
        #the format of self.stats: each question consists of onw row and two colomns. First column contains its id
        #and the question description Second row contains the accuracy, number of flashcards ago of its last time seen,
        #and the total number of this flashcard seen
        self.stats = self.obtain_stats()
        self.reset_accuracy_list()

        #make the accuracy list to be scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.wrap_accuracy_list = QWidget()
        self.wrap_accuracy_list.setLayout(self.accuracy_list)
        self.scroll_area.setWidget(self.wrap_accuracy_list)

        #provide three ways to sort it
        sort_by_accuracy = QPushButton("Sort By Accuracy")
        sort_by_accuracy.clicked.connect(self.sort_by_accuracy)
        sort_by_last_time_seen = QPushButton("Sort By Last Time Seen")
        sort_by_last_time_seen.clicked.connect(self.sort_by_last_time_seen)
        sort_by_number_of_time_seen = QPushButton("Sort By Total Time Seen")
        sort_by_number_of_time_seen.clicked.connect(self.sort_by_number_of_time_seen)

        # Button to go back to Menu page
        back_menu_button = QPushButton("Back to Menu")
        back_menu_button.clicked.connect(switch_back_to_menu)
        #create a horizontal box layout
        self.sort_buttons = QHBoxLayout()
        self.sort_buttons.addWidget(sort_by_accuracy)
        self.sort_buttons.addWidget(sort_by_number_of_time_seen)
        self.sort_buttons.addWidget(sort_by_last_time_seen)
        self.wrap_sort_buttons = QWidget()
        self.wrap_sort_buttons.setLayout(self.sort_buttons)
        # Add widgets to layout
        self.Layout.addWidget(back_menu_button)
        self.Layout.addWidget(self.scroll_area)
        self.Layout.addWidget(self.wrap_sort_buttons)
        self.setLayout(self.Layout)
    #sort the stats list by these three options
    def sort_by_accuracy(self):
        self.stats = sorted(self.stats,key=lambda x:float( x[1].split(':')[1].split('%')[0][1:] ))
        self.reset_accuracy_list()

    def sort_by_last_time_seen(self):
        self.stats = sorted(self.stats,key=lambda x:float( x[1].split(':')[2].split('f')[0]), reverse = True)
        self.reset_accuracy_list()

    def sort_by_number_of_time_seen(self):
        self.stats = sorted(self.stats,key = lambda x:float( x[1].split(':')[-1][1:-2]))
        self.reset_accuracy_list()

    def obtain_stats(self): #obtain data from stats.txt, returns the list
        li = []
        if(os.path.isdir("./current") == False):
            shutil.copytree("./New flashcards","./current")
        with open("./current/stats.txt","r",encoding="utf-8") as f:
            stats = f.readlines()
        for i in range(1,len(stats)+1):
            subli = []
            try:
                with open(f"./current/flashcards/{i}_des.txt","r",encoding="utf-8") as f:
                    subli.append(f"Question {i}: {f.read()}")
            except:
                subli.append(f"Question {i}: Unknown: No such question exists.")
            try:
                accuracy = round(100*(float(stats[i-1].split(' ')[1])) / (float(stats[i-1].split(' ')[0])),2)
            except: ##division by zero
                accuracy = 0
            try:
                last_time_seen = stats[i-1].split(' ')[2]
                number_of_time_seen = stats[i-1].split(' ')[0]
            except:
                last_time_seen = 0
                number_of_time_seen = 0
            subli.append(f"Accuracy: {accuracy}%.  Last Time Seen: {last_time_seen} flashcards ago.  Number Of Time: {number_of_time_seen}.\n")
            li.append(subli)
        return li

    def reset_accuracy_list(self):
    #first remove all the widgets in accuracy_list, then add them again (since there are sorting functions)
        while self.accuracy_list.count():
            content = self.accuracy_list.takeAt(0)
            widget = content.widget()
            if widget:
                widget.deleteLater()
            self.accuracy_list.removeItem(content)

        for content in self.stats:
            content_label = QLabel(content[0])
            self.accuracy_list.addWidget(content_label)
            content_label = QLabel(content[1])
            self.accuracy_list.addWidget(content_label)

    def refreshpage(self,switch):
        while self.layout().count():
            content = self.layout().takeAt(0)
            widget = content.widget()
            if widget:
                widget.deleteLater()
            self.layout().removeItem(content)

         # Title label
        self.title = QLabel("Statistics")
        self.Layout.addWidget(self.title)

        # List widget to display accuracy of each question
        self.frame = QFrame()
        #accuracy_list is embedded in self.scroll_area, so no need to self.Layout.addWidget(self.accuracy_list)
        self.accuracy_list = QVBoxLayout(self.frame)
        # Sample data (to be replaced with actual data)
        #the format of self.stats: each question consists of onw row and two colomns. First column contains its id
        #and the question description Second row contains the accuracy, number of flashcards ago of its last time seen,
        #and the total number of this flashcard seen
        self.stats = self.obtain_stats()
        self.reset_accuracy_list()

        #make the accuracy list to be scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.wrap_accuracy_list = QWidget()
        self.wrap_accuracy_list.setLayout(self.accuracy_list)
        self.scroll_area.setWidget(self.wrap_accuracy_list)

        #provide three ways to sort it
        sort_by_accuracy = QPushButton("Sort By Accuracy")
        sort_by_accuracy.clicked.connect(self.sort_by_accuracy)
        sort_by_last_time_seen = QPushButton("Sort By Last Time Seen")
        sort_by_last_time_seen.clicked.connect(self.sort_by_last_time_seen)
        sort_by_number_of_time_seen = QPushButton("Sort By Total Time Seen")
        sort_by_number_of_time_seen.clicked.connect(self.sort_by_number_of_time_seen)

        # Button to go back to Menu page
        back_menu_button = QPushButton("Back to Menu")
        back_menu_button.clicked.connect(switch)
        #create a horizontal box layout
        self.sort_buttons = QHBoxLayout()
        self.sort_buttons.addWidget(sort_by_accuracy)
        self.sort_buttons.addWidget(sort_by_number_of_time_seen)
        self.sort_buttons.addWidget(sort_by_last_time_seen)
        self.wrap_sort_buttons = QWidget()
        self.wrap_sort_buttons.setLayout(self.sort_buttons)
        # Add widgets to layout
        self.Layout.addWidget(back_menu_button)
        self.Layout.addWidget(self.scroll_area)
        self.Layout.addWidget(self.wrap_sort_buttons)

        self.layout().update()
        
'''
class statistics(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Statistics")

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(QLabel("Statistics"))

    def use_store_accuracy(self):
        return store_accuracy(self)

    def use_next_question(self):
        return next_question(self)

def next_question(list,accuracy):
    pass

def store_accuracy(id,is_correct):
    pass'''

