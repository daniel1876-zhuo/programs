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
    QMediaFormat,QMediaPlayer,QAudioOutput,QSoundEffect
)
#plan: after done, change to video part into a new class, leave the original video part with a button instead
#which shows pop-out window of playing the video.

#a class that renders a file, given the question_id (so that the file location can be found by using metadata.txt)
class MediaPlayer(QWidget):
    #initialize the class, "answer" parameter means is finding question file or answer file
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
                #self.fileloc is the file location found by reading metadata
                if answer:
                    self.fileloc = "./current/flashcards/"+f.readlines()[flashnum+1][0:-1].split(":")[1]
                else:
                    self.fileloc = "./current/flashcards/"+f.readlines()[flashnum+1][0:-1].split(":")[0]
            except:
                self.label = QLabel(" ") ## doesn't exist?
                self.scroll = QScrollArea()
                self.scroll.setFixedHeight(300)
                self.scroll.setWidget(self.label)

                return self.scroll
        try:
            #extension is the file suffix (e.g. .png, .mp4, etc)
            extension = self.fileloc[-4:].lower()
            print("moved on",extension,self.fileloc)
            if extension == ".txt":
                with open(self.fileloc,"r") as f:
                    text = "".join(f.readlines())
                print("rendering text:", text)
                self.label = QLabel(text)
                self.scroll = QScrollArea()
                self.scroll.setFixedHeight(300)
                self.scroll.setWidget(self.label)
                return self.scroll
            #the file is an iamge, use Pixmap to render the file
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
            #the file is a video, use pygame to show it
            elif extension in (".mp4,.avi,.mov"): ##video
                #create a "play video" button, when it is clicked it pops out a window that shows the video.
                self.playing = QPushButton("Play The Video")
                self.playing.setMinimumHeight(300)
                self.playing.clicked.connect(self.playvideo)
                return self.playing
            #the file is an audio, use QMediaPlayer to display it
            elif extension in (".mp3, .wav"):
                #create two buttons to play and stop the audio.
                self.playing = QPushButton("Play The Audio")
                self.playing.setMinimumHeight(270)
                self.playing.clicked.connect(self.playaudio)
                self.stop_playing = QPushButton("Stop Playing")
                self.stop_playing.clicked.connect(self.stopplay)
                return self.playing,self.stop_playing
            else: ##unknown type (some unknwon errors may occur, if this happen then set a spare content)
                self.label = QLabel(" ")
                self.scroll = QScrollArea()
                self.scroll.setFixedHeight(300)
                self.scroll.setWidget(self.label)
                return self.scroll
        #no file exists or other unknown errors occur, set a spare content.
        except Exception as e:
            print(e)
            self.label = QLabel(" ")
            self.scroll = QScrollArea()
            self.scroll.setFixedHeight(300)
            self.scroll.setWidget(self.label)
            return self.scroll ## no file exists?

    #the function used to organize the flashcard, including adding the question description, and the file rendering
    #flashnum is the question_id.
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
        try:
            f.close()
        except:
            pass
        #if is to show answer flashcard
        if answer:
            try:
                desc = open("./current/flashcards/"+str(flashnum)+"_answer_des.txt")
                text = "".join(desc.readlines())
                self.layout.addWidget(QLabel(text))
                desc.close()
            except: ## no desc
                pass
            #call the renderfile() to render the content of the file

            output = self.renderfile(flashnum,True)
            try:
                self.layout.addWidget(output)
            except Exception as e:
                print(e)
                print(output)
                for components in output:
                    self.layout.addWidget(components)
            return self.layout
        #if is to show question flashcard
        else:
            try:
                desc = open("./current/flashcards/"+str(flashnum)+"_des.txt")
                text = "".join(desc.readlines())
                self.layout.addWidget(QLabel(text))
                desc.close()
            except: ## no desc
                pass
            # call the renderfile() to render the content of the file
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
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setSource(QUrl.fromLocalFile(self.fileloc))
        self.audio.setVolume(50)
        self.player.play()

    def stopplay(self):
            self.player.stop()

