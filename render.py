import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget, QScrollArea
)
from PySide6.QtGui import (
    QImage,QPixmap
)
from PySide6.QtCore import (
    QSize,Qt,QUrl
)
from PySide6.QtMultimedia import (
    QMediaFormat,QMediaPlayer
)
from PySide6.QtMultimediaWidgets import (
    QVideoWidget
)
# f = QMediaFormat()
# print(QMediaFormat.supportedFileFormats(f,QMediaFormat.Decode))

def renderfile(flashnum,answer=False):
    global video
    """
    Takes in flashcard number (starting from 1)
    Choose to render question(False) or answer(True)
    Returns a QVBoxLayout that contains the flashcard question and true/false indicating media
    """
    with open("./current/metadata.txt", "r", encoding="utf-8") as f:
        try:
            if answer:
                fileloc = "./current/flashcards/"+f.readlines()[flashnum+1][0:-1].split(":")[1]
            else:
                fileloc = "./current/flashcards/"+f.readlines()[flashnum+1][0:-1].split(":")[0]
        except:
            label = QLabel(" ") ## doesn't exist?
            scroll = QScrollArea()
            scroll.setFixedHeight(300)
            scroll.setWidget(label)
            return scroll
    try:
        extension = fileloc[-4:].lower()
        if extension == ".txt":
            with open(fileloc,"r") as f:
                text = "".join(f.readlines())
            print("Rendering text!")
            label = QLabel(text)
            scroll = QScrollArea()
            scroll.setFixedHeight(300)
            scroll.setWidget(label)
            return scroll
        elif extension in (".gif,.jpg,jpeg,.png"):
            label = QLabel()
            pixmap = QPixmap.fromImage(QImage(fileloc))
            size = QSize()
            size.setHeight(300)
            size.setWidth(500)
            pixmap = pixmap.scaled(size,Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            print("rendering image!")
            return label
        else: ##no audio or video support
            label = QLabel(" ")
            scroll = QScrollArea()
            scroll.setFixedHeight(300)
            scroll.setWidget(label)
            return scroll
    except Exception as e:
        print(e)
        label = QLabel(" ")
        scroll = QScrollArea()
        scroll.setFixedHeight(300)
        scroll.setWidget(label)
        return scroll ## no file exists?

def renderflashcard(flashnum,answer=False):
    layout = QVBoxLayout()
    try:
        f = open("./current/metadata.txt", "r", encoding="utf-8")
    except:
        print("Metadata doesn't exist yet! renderquestion() will need to be run again when flashcards are properly loaded.")
        layout.addWidget(QLabel("No existing flashcard yet!"))
        return layout
    if flashnum > int(f.readlines()[1]):
        layout.addWidget(QLabel("No existing flashcard yet!"))
        return layout
    if answer:
        try:
            desc = open("./current/flashcards/"+str(flashnum)+"_answer_des.txt")
            text = "".join(desc.readlines())
            layout.addWidget(QLabel(text))
        except: ## no desc
            pass
        output = renderfile(flashnum,True)
        layout.addWidget(output)
        return layout
    else:
        layout = QVBoxLayout()
        try:
            desc = open("./current/flashcards/"+str(flashnum)+"_des.txt")
            text = "".join(desc.readlines())
            layout.addWidget(QLabel(text))
        except: ## no desc
            pass
        output = renderfile(flashnum)
        layout.addWidget(output)
        return layout

def playmedia(play):
    print("button press")
    play.setPosition(0)
    play.play()