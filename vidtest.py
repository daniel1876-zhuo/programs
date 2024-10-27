import sys
from PySide6.QtMultimedia import (
    QMediaPlayer,QAudioOutput
)
from PySide6.QtCore import (
    QUrl
)
from PySide6.QtMultimediaWidgets import (
    QVideoWidget
)
from PySide6.QtWidgets import (
    QWidget,QApplication,QLayout,QVBoxLayout,QMainWindow,QLabel
)

import time

class window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.player.setSource(QUrl.fromLocalFile("/Users/mickeywong/Documents/programs-main/current/flashcards/1_file.wav"))
        ao = QAudioOutput()
    
        ao.setMuted(False)
        ao.setVolume(100)
        self.player.setAudioOutput(ao)
        container = QWidget()
        lay = QVBoxLayout()
        lay.addWidget(QLabel("abc"))
        container.setLayout(lay)
        self.setCentralWidget(container)
        # self.player.mediaStatusChanged.connect(lambda status : print(status))
        self.player.mediaStatusChanged.connect(self.handle)

    def handle(self):
        print(self.player.error(),self.player.mediaStatus(),self.player.errorString())
        if self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.play()
            print("trying to play")
            print(self.player.isPlaying())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    play = window()
    play.show()
    sys.exit(app.exec())