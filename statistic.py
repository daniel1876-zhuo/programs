from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QFileDialog,
    QLabel,
    QMainWindow,
    QStackedWidget,
)

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
    pass

