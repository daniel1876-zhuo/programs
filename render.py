import sys,pygame
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,QHBoxLayout,QSlider,
    QPushButton, QLabel, QStackedWidget, QFileDialog, QMessageBox, QListWidget, QScrollArea
)
from PySide6.QtGui import (
    QImage,QPixmap
)
from PySide6.QtCore import (
    QSize,Qt,QUrl,QTimer
)
from moviepy.editor import VideoFileClip,AudioFileClip
from PySide6.QtMultimedia import (
    QMediaFormat,QMediaPlayer,
)
from PySide6.QtMultimediaWidgets import (
    QVideoWidget
)
# f = QMediaFormat()
# print(QMediaFormat.supportedFileFormats(f,QMediaFormat.Decode))
#plan: after done, change to video part into a new class, leave the original video part with a button instead
# which shows pop-out window of playing the video.
class MediaPlayer(QWidget):
    def __init__(self,flashnum,answer=False):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.renderflashcard(flashnum,answer)
    def renderfile(self,flashnum,answer=False):
        """
        Takes in flashcard number (starting from 1)
        Choose to render question(False) or answer(True)
        Returns a QVBoxLayout that contains the flashcard question and true/false indicating media
        """
        with open("./current/metadata.txt", "r", encoding="utf-8") as f:
            try:
                if answer:
                    self.fileloc = "./current/flashcards/"+f.readlines()[flashnum+1][0:-1].split(":")[1][:-1]
                else:
                    self.fileloc = "./current/flashcards/"+f.readlines()[flashnum+1][0:-1].split(":")[0]
            except:
                self.label = QLabel(" ") ## doesn't exist?
                self.scroll = QScrollArea()
                self.scroll.setFixedHeight(300)
                self.scroll.setWidget(self.label)

                return self.scroll
        try:
            extension = self.fileloc[-4:].lower()
            if extension == ".txt":
                with open(self.fileloc,"r") as f:
                    text = "".join(f.readlines())
                print("Rendering text!")
                self.label = QLabel(text)
                self.scroll = QScrollArea()
                self.scroll.setFixedHeight(300)
                self.scroll.setWidget(self.label)
                return self.scroll
            elif extension in (".gif,.jpg,.jpeg,.png"):
                self.label = QLabel()
                pixmap = QPixmap(self.fileloc)
                self.size = QSize()
                self.size.setHeight(300)
                self.size.setWidth(500)
                pixmap = pixmap.scaled(self.size,Qt.KeepAspectRatio)
                self.label.setPixmap(pixmap)
                print("rendering image!")
                return self.label
            elif extension in (".mp4,.avi,.mov"): ##video
                self.playing = QPushButton("Play The Video")
                self.playing.clicked.connect(self.playvideo)
                return self.playing
            elif extension in (".mp3, .wav"):
                self.playing = QPushButton("Play The Audio")
                self.playing.clicked.connect(self.playaudio)
                return self.playing
            else: ##unknown type
                self.label = QLabel(" ")
                self.scroll = QScrollArea()
                self.scroll.setFixedHeight(300)
                self.scroll.setWidget(self.label)
                return self.scroll
        except Exception as e:
            print(e)
            self.label = QLabel(" ")
            self.scroll = QScrollArea()
            self.scroll.setFixedHeight(300)
            self.scroll.setWidget(self.label)
            return self.scroll ## no file exists?

    def renderflashcard(self,flashnum,answer=False):
        try:
            f = open("./current/metadata.txt", "r", encoding="utf-8")
        except:
            print("Metadata doesn't exist yet! renderquestion() will need to be run again when flashcards are properly loaded.")
            self.layout.addWidget(QLabel("No existing flashcard yet!"))
            return self.layout
        if flashnum > int(f.readlines()[1]):
            self.layout.addWidget(QLabel("No existing flashcard yet!"))
            return self.layout

        if answer:
            try:
                desc = open("./current/flashcards/"+str(flashnum)+"_answer_des.txt")
                text = "".join(desc.readlines())
                self.layout.addWidget(QLabel(text))
            except: ## no desc
                pass
            output = self.renderfile(flashnum,True)
            self.layout.addWidget(output)
            return self.layout
        else:
            try:
                desc = open("./current/flashcards/"+str(flashnum)+"_des.txt")
                text = "".join(desc.readlines())
                self.layout.addWidget(QLabel(text))
            except: ## no desc
                pass
            output = self.renderfile(flashnum)
            #print(output)
            try:
            #print("variable 'output' has a datatype of:",type(output))
                self.layout.addWidget(output)
            except Exception as e:
                print(e)
                for components in output:
                    self.layout.addWidget(components)

    def playvideo(self):
        #print("button is clicked!")
        pygame.init()
        video = VideoFileClip(self.fileloc)
        video.preview()
        pygame.quit()

    def playaudio(self):
        pygame.init()
        audio = AudioFileClip(self.fileloc)
        audio.preview()
        pygame.quit()
