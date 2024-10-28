import os,shutil #used for file handling
from PySide6.QtWidgets import ( #import widget classes
    QVBoxLayout, QWidget, QTextEdit,
    QPushButton, QLabel, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import( #import qt classes for widget alignment
    Qt
)
from render import * #render.py handles rendering flashcards

class EditorPage(QWidget):
    """
    Page for editing flashcard set.
    """

    def __init__(self, switch_back,refresh): #initialize page
        super().__init__()
        self.currentflash = [1,False] #currently viewing flashcard, and viewing answer(true) or question(false)
        self.ischanging = False #store that we are not replacing the answer file/description
                                #so the previous/next buttons can be enabled

        self.Layout = QVBoxLayout() #left layout
        self.Layout2 = QVBoxLayout() #right layout
        self.realLayout = QHBoxLayout() #outer layout
        self.toplabel = QLabel("Currently showing flashcard")

        self.minilayout = QHBoxLayout() #layout for switching currently viewing flashcard
        self.prevbutton = QPushButton("Show Previous")
        self.prevbutton.clicked.connect(lambda : self.changeflash(self.currentflash[0]-1))
        self.minilayout.addWidget(self.prevbutton)
        self.flashnum = QLabel(str(self.currentflash[0])) #shows current flashcard number
        self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.change = QPushButton("Show Answer")
        self.change.clicked.connect(self.showans)
        self.minilayout.addWidget(self.change)
        self.nextbutton = QPushButton("Show Next")
        self.nextbutton.clicked.connect(lambda : self.changeflash(self.currentflash[0]+1))
        self.minilayout.addWidget(self.nextbutton)

        #add relevant widgets to the left layout
        self.Layout.addWidget(self.toplabel)
        self.Layout.addWidget(self.flashnum)
        self.Layout.addLayout(self.minilayout)

        self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1]) #returns rendered flashcard widget
        self.Layout.addWidget(self.flashrender)
        self.title = QLabel("Replace this flashcard")

        #add relevant widgets to the right layout
        self.Layout2.addWidget(self.title)
        self.replace_question_and_answer(refresh) #add flashcard editing widgets into layout
        self.title2 = QLabel("Add new flashcard")
        self.Layout2.addWidget(self.title2)

        self.upload_question_and_answer(refresh) #add flashcard adding widgets into layout

        self.rem_button = QPushButton("Remove this flashcard") #remove flashcards button
        self.rem_button.clicked.connect(lambda:self.removeflash(refresh))
        self.Layout2.addWidget(self.rem_button)

        self.title3 = QLabel("Rename this flashcard set (press back to flashcards to save changes)")
        self.Layout2.addWidget(self.title3)

        self.renameinput = QTextEdit() #text box for renaming flashcard
        try: #try statement so that initial run won't error because metadata.txt doesn't exist yet
            with open("./current/metadata.txt") as f:
                self.renameinput.setPlainText(f.readline()[0:-1]) #fill textbox with current flashcard name
        except:
            pass
        self.Layout2.addWidget(self.renameinput)

        self.back_button = QPushButton("Back to Flashcards") #back to flashcard menu button
        self.back_button.clicked.connect(lambda:self.savename(switch_back))
        self.Layout2.addWidget(self.back_button)

        self.realLayout.addLayout(self.Layout)
        self.realLayout.addLayout(self.Layout2)
        self.setLayout(self.realLayout)

    def upload_file(self): #Upload new file add to flashcards
        file = QFileDialog.getOpenFileName(self, "Select Multimedia Files", "",
                                           "Text(*.txt;*.doc;*.docx);;Images (*.png;*.jpg;*.jpeg);;Audio (*.mp3;*.wav);;Videos (*.mp4;*.avi)")
        if file[0]:
            target_directory = "./current/flashcards"
            file_suffix = file[0].split(".")[-1] #the file suffix
            if self.is_question: #whether we're replacing the question or answer file
                #set target path
                self.question_file_path = f"{target_directory}/{str(self.file_id)}_file.{file_suffix}"
            else:
                self.answer_file_path = f"{target_directory}/{str(self.file_id)}_answer_file.{file_suffix}"
            try:
                if self.is_question: #whether we're replacing the question or answer file
                    #copy the file to the target location
                    shutil.copy(file[0], self.question_file_path)
                    print(f"File copied to: {self.question_file_path}")
                else:
                    shutil.copy(file[0], self.answer_file_path)
                    print(f"File copied to: {self.answer_file_path}")
            except Exception as e:
                print(f"Error while copying the file: {e}")
    
    def replace_file(self):#upload file to replace in existing flashcards
        file = QFileDialog.getOpenFileName(self, "Select Multimedia Files", "",
                                           "Text(*.txt;*.doc;*.docx);;Images (*.png;*.jpg;*.jpeg);;Audio (*.mp3;*.wav);;Videos (*.mp4;*.avi)")
        if file[0]:
            target_directory = "./current/flashcards"
            file_suffix = file[0].split(".")[-1] #the file suffix
            if self.is_question2: #Whether we're replacing the question or answer
                #set target path
                self.question_file_path2 = f"{target_directory}/{str(self.currentflash[0])}_file.{file_suffix}"
            else:
                self.answer_file_path2 = f"{target_directory}/{str(self.currentflash[0])}_answer_file.{file_suffix}"
            try:
                if self.is_question2:
                    #copy the file to the target location
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
        #controls what should happen when we press submit to add flashcard
        if self.is_question: #if we are editing question or answer
            target_directory = "./current/flashcards"
            #create the description file
            target_path = f"{target_directory}/{self.file_id}"
            with open(f"{target_path}_des.txt","w",encoding="utf-8") as f:
                f.write(self.question_input.toPlainText())
            
            self.change_from_question_to_answer()#changes text to accept an answer description and/or file
        else:
            target_directory = "./current/flashcards"
            #create the description file
            target_path = f"{target_directory}/{self.file_id}"

            with open(f"{target_path}_answer_des.txt", "w", encoding="utf-8") as f:
                f.write(self.question_input.toPlainText())

            # read the metadata
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                self.metatext = f.readlines() #storing contents to self.metatext

            # adding question file
            with open("./current/metadata.txt", "w", encoding="utf-8") as f:
                self.metatext[1] = str(self.file_id)+"\n" #changing second row of metadata: number of flashcards
                #adding new row to metadata containing flashcard question and answer file names
                self.metatext.append(f"{self.question_file_path.split('/')[-1]}:{self.answer_file_path.split('/')[-1]}\n") 
                f.writelines(self.metatext)

            #update stats.txt, adding a new flashcard's data into it
            with open("./current/stats.txt","a",encoding="utf-8") as f:
                f.write(f"0 0 -1 {False}\n")
            self.file_id += 1  #increment number of flashcards by 1
            refresh() #refreshes entire page to reset everything
            #this refresh() is passed here from main.py and runs self.updatepage()

    def replacesubmit(self,refresh): 
        #same as submit except we are submitting to replace a flashcard
        if self.is_question2: #if we are editing question or answer
            target_directory = "./current/flashcards"
            #create the description file
            target_path = f"{target_directory}/{self.currentflash[0]}"
            with open(f"{target_path}_des.txt","w",encoding="utf-8") as f:
                f.write(self.question_input2.toPlainText())

            #changes text to accept an answer description and/or file
            self.ischanging = True #disable next and previous buttons
            self.is_question2 = False #store that we are now editing the answer
            self.question_label2.setText("Replace your answer's description (If Any):")
            try:
                with open("./current/flashcards/"+str(self.currentflash[0])+"_answer_des.txt","r") as f:
                    self.question_input2.setPlainText("".join(f.readlines())) #fill description textbox with existing description
            except:
                pass
        else:
            target_directory = "./current/flashcards"
            # create the description file
            target_path = f"{target_directory}/{self.currentflash[0]}"

            with open(f"{target_path}_answer_des.txt", "w", encoding="utf-8") as f:
                f.write(self.question_input2.toPlainText())

            # read the metadata
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                self.metatext = f.readlines()
            # adding question file
            with open("./current/metadata.txt", "w", encoding="utf-8") as f:
                filenames = self.metatext[1+self.currentflash[0]].split(":") #extracting current filenames
                if self.is_uploaded == True: #whether we need to change question filename or not
                    filenames[0] = self.question_file_path2.split('/')[-1]
                if self.is_ans_uploaded == True: #whether we need to change answer filename or not
                    filenames[1] = self.answer_file_path2.split('/')[-1]
                self.metatext[1+self.currentflash[0]] = filenames[0]+':'+filenames[1]+'\n'
                f.writelines(self.metatext)
            self.ischanging = False #not actually necessary because the same line is in updatetext()
                                    #but its here just in case
            refresh() #refreshes entire page to reset everything
            #this refresh() is passed here from main.py and runs self.updatepage()


    def change_from_question_to_answer(self):
        #changes text to accept an answer description & file
        self.is_question = False #store that we are now editing the answer
        self.question_label.setText("Enter your answer's description (If Any):")
        self.question_input.clear() #clears the input textbox

    def upload_question_and_answer(self,refresh):
        # add widgets for adding new flashcards
        try:
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                self.file_id = int(f.readlines()[1][0:-1])#the index of the latest file added
            self.file_id += 1
            self.question_file_path = f"./current/flashcards/{str(self.file_id)}_file.txt"
            self.answer_file_path = f"./current/flashcards/{str(self.file_id)}_answer_file.txt"
        except Exception as e: #metadata or other files likely doesn't exist yet
                               #this will be repeated in updatepage() and by then we will have valid files
            print(e)
        #input for question's description
        self.question_label = QLabel("Enter your question's description (If Any):")
        self.question_input = QTextEdit()#input textbox

        try: #determine file paths
            self.question_file_path = str(self.file_id)+"_file.txt"
            self.answer_file_path = str(self.file_id)+"_answer_file.txt"
        except: #files don't exist yet, likely the first run of the program
            pass
        self.is_question = True #store that we are editing the question
        self.upload_button = QPushButton("Upload File (If Any):") #upload file button
        self.upload_button.clicked.connect(lambda:self.upload_file())

        self.submit_button = QPushButton("Submit") #submit button
        self.submit_button.clicked.connect(lambda:self.submit(refresh))

        #add widgets to the right layout
        self.Layout2.addWidget(self.question_label)
        self.Layout2.addWidget(self.question_input)
        self.Layout2.addWidget(self.upload_button)
        self.Layout2.addWidget(self.submit_button)
    
    def replace_question_and_answer(self,refresh):
        #same as upload except the inputs will be used to replace a flashcard
        try:
            self.question_file_path2 = f"./current/flashcards/{str(self.currentflash[0])}_file.txt"
            self.answer_file_path2 = f"./current/flashcards/{str(self.currentflash[0])}_answer_file.txt"
        except Exception as e: #metadata or other files likely doesn't exist yet
                               #this will be repeated in updatepage() and by then we will have valid files
            print(e)
        #input for question's description
        self.question_label2 = QLabel("Replace your question's description (If Any):")
        self.question_input2 = QTextEdit() #input textbox
        try:
            with open("./current/flashcards/"+str(self.currentflash[0])+"_des.txt","r") as f:
                self.question_input2.setPlainText("".join(f.readlines())) #fill textbox with current description
        except:
            pass


        self.is_uploaded = False #store that we have not uploaded any question file yet
        self.is_ans_uploaded = False #store that we have not uploaded any answer file yet
        #determine file paths
        self.question_file_path2 = str(self.currentflash[0])+"_file.txt"
        self.answer_file_path2 = str(self.currentflash[0])+"_answer_file.txt"
        self.is_question2 = True #store that we are editing the question file/description
        self.upload_button2 = QPushButton("Replace File (If Any):")
        self.upload_button2.clicked.connect(lambda:self.replace_file())#button to upload replacement file

        #utton to submit
        self.submit_button2 = QPushButton("Submit")
        self.submit_button2.clicked.connect(lambda:self.replacesubmit(refresh))

        #add widgets to right layout
        self.Layout2.addWidget(self.question_label2)
        self.Layout2.addWidget(self.question_input2)
        self.Layout2.addWidget(self.upload_button2)
        self.Layout2.addWidget(self.submit_button2)
    
    def updatepage(self,switch_back,refresh): 
        # update the page, including the fetched files, flashcard viewer, etc.

        # implementation here is awkward but it works
        # I'd rather not use a loop here so as to avoid unwanted side effects

        # remove every widget from its respective layout
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
        self.question_label.deleteLater()#delete the removed widgets
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
        try:
            self.flashrender.deleteLater()
        except:
            pass
        self.title.deleteLater()
        self.title2.deleteLater()
        self.title3.deleteLater()
        self.rem_button.deleteLater()
        self.renameinput.deleteLater()

        self.ischanging = False #store that we are not replacing the answer file/description
                                #so the previous/next buttons can be enabled

        #build the page back up again as in init()
        self.toplabel = QLabel("Currently showing flashcard")
        self.Layout.insertWidget(0,self.toplabel)
        self.flashnum = QLabel(str(self.currentflash[0])) #shows current flashcard number
        self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Layout.insertWidget(1,self.flashnum)
        self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1]) #returns rendered flashcard widget
        self.Layout.addWidget(self.flashrender)
        self.title = QLabel("Replace this flashcard")
        self.Layout2.addWidget(self.title)
        self.replace_question_and_answer(refresh) #add flashcard editing widgets to layout
        self.title2 = QLabel("Add new flashcard")
        self.Layout2.addWidget(self.title2)
        self.upload_question_and_answer(refresh) #add flashcard adding widgets to layout

        self.rem_button = QPushButton("Remove this flashcard") #flashcard removing button
        self.rem_button.clicked.connect(lambda:self.removeflash(refresh))
        self.Layout2.addWidget(self.rem_button)

        self.title3 = QLabel("Rename this flashcard set (press back to flashcards to save changes)")
        self.Layout2.addWidget(self.title3)

        self.renameinput = QTextEdit()#flashcard renaming textbox
        try:
            with open("./current/metadata.txt") as f:
                self.renameinput.setPlainText(f.readline()[0:-1]) #fill textbox with current flashcard name
        except:
            pass
        self.Layout2.addWidget(self.renameinput)

        self.back_button = QPushButton("Back to Flashcards")
        self.back_button.clicked.connect(lambda:self.savename(switch_back))
        self.Layout2.addWidget(self.back_button)

        #update layouts to show changes visually
        self.Layout.update()
        self.Layout2.update()
        self.layout().update()

    def showans(self):
        # change the displayed flashcard between question and answer
        if self.currentflash[1]: # currently showing answer, this will change it to showing question
            self.minilayout.removeWidget(self.change)
            self.change.deleteLater() #removing the "show question" button
            self.currentflash[1] = False #store that we are now showing the question
            self.change = QPushButton("Show Answer")
            self.change.clicked.connect(self.showans)
            self.minilayout.insertWidget(1,self.change) #replacing it with "show answer" button
            self.minilayout.update() #update flashcard changing layout to reflect changes

            try:
                self.flashrender.deleteLater() #delete currently displayed flashcard
            except:
                pass
            self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1]) #render a new flashcard from render.py
            self.Layout.insertWidget(3,self.flashrender)
            self.layout().update() #update layout to show rendered flashcard

        else:  # currently showing question, this will change it to showing answer
            self.minilayout.removeWidget(self.change)
            self.change.deleteLater()#removing the "show answer" button
            self.currentflash[1] = True #store that we are now showing the question
            self.change = QPushButton("Show Question")
            self.change.clicked.connect(self.showans)
            self.minilayout.insertWidget(1,self.change) #replacing it with "show question" button
            self.minilayout.update()

            try:
                self.flashrender.deleteLater() #delete currently displayed flashcard
            except:
                pass
            self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1]) #render a new flashcard from render.py
            self.Layout.insertWidget(3,self.flashrender)
            self.layout().update() #update layout to show rendered flashcard

    def changeflash(self,newflashnum):
        # display a new flashcard
        if not self.ischanging: #skip if prev/next button is disabled
            with open("./current/metadata.txt", "r", encoding="utf-8") as f:
                totalnum = int(f.readlines()[1][0:-1]) #fetch total flashcard number
            
            #ensures newflashnum is within range
            if newflashnum == 0:
                newflashnum = totalnum
            if newflashnum == totalnum+1:
                newflashnum = 1

            self.minilayout.removeWidget(self.change) #removing the "show question/answer" button to be replaced
            self.change.deleteLater()
            self.currentflash[1] = False #store that we are showing question
            self.currentflash[0] = newflashnum #store taht we are showing the new flashcard
            self.change = QPushButton("Show Answer") #replacing button
            self.change.clicked.connect(self.showans)
            self.minilayout.insertWidget(1,self.change)

            self.Layout.removeWidget(self.flashnum)
            self.flashnum.deleteLater() #removing flashcard number
            self.flashnum = QLabel(str(self.currentflash[0])) #replace with new flashcard number
            self.flashnum.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.Layout.insertWidget(1,self.flashnum)#insert changes into layout

            try:
                self.flashrender.deleteLater() #delete currently showing flashcard
            except:
                pass
            self.flashrender = MediaPlayer(self.currentflash[0],self.currentflash[1]) #render new flashcard from render.py to show
            self.Layout.insertWidget(3,self.flashrender)
            self.minilayout.update() #update layouts to show changes
            try:
                with open("./current/flashcards/"+str(self.currentflash[0])+"_des.txt","r") as f:
                    self.question_input2.setPlainText("".join(f.readlines())) #change "edit question description" text box
            except:
                pass
            self.layout().update()
            
    def removeflash(self,refresh):
        # deletes the currently shown flashcard
        f = open("./current/metadata.txt","r")
        text = f.readlines()
        if text[1] == "1\n": #there is only 1 flashcard
            f.close()
            QMessageBox.information(self,"Cannot remove","Please add another flashcard before removing this one!")
        else:
            text[1] = str(int(text[1])-1) #subtract 1 from the number of flashcards stored in metadata
            text.pop(self.currentflash[0]+1) #remove the filenames of said flashcard

            #adjust filenames in metadata.txt
            for i in range(self.currentflash[0]+1,int(text[1])+2):
                text[i] = text[i].replace(str(i),str(i-1))
            f.close()
            text[1] = text[1] + "\n"

            with open("./current/metadata.txt","w") as f:
                f.writelines(text)# write the metadata file back in
            with open("./current/stats.txt","r") as f:
                text2 = f.readlines()
                text2.pop(self.currentflash[0]-1)#remove statistics
            with open("./current/stats.txt","w") as f:
                f.writelines(text2)
            

            for f in os.listdir("./current/flashcards"): #delete relevant flashcard files
                if f.startswith(str(self.currentflash[0])):
                    os.remove(os.path.join("./current/flashcards",f))
            for f in os.listdir("./current/flashcards"): #adjust names of existing files
                flashnum = int(f[0])
                if flashnum > self.currentflash[0]:
                    print(f)
                    print("renamed to",str(flashnum-1)+f[1:])
                    os.rename(os.path.join("./current/flashcards",f),"./current/flashcards/"+str(flashnum-1)+f[1:])
            print('refresh!')
            self.currentflash = [1,False] #display the first flashcard again
            refresh() #refreshes entire page to reset everything
                      #this refresh() is passed here from main.py and runs self.updatepage()
    
    def savename(self,switch_back):
        # Saves the changed flashcard name under metadata
        with open("./current/metadata.txt","r") as f:
            text = f.readlines()
            text[0] = self.renameinput.toPlainText()+"\n"
        with open("./current/metadata.txt","w") as f:
            f.writelines(text)
        switch_back()
