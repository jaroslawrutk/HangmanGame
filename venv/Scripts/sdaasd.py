# client
import socket
import ssl
import pickle
import _thread
from tkinter import *

hangman = (
    """







                    ___                 
        """,
    """

       |/        
           |              
             |                
              |                 
            |               
                |                   
                   |___                 
        """,
    """
       _________
       |/        
           |              
             |                
              |                 
            |               
                |                   
                 |___               
        """,
    """
       _________
           |/       |     
           |              
             |                
              |                 
            |               
                |                   
                     |___                   
        """,
    """
       _________
           |/       |     
           |       (_)   
             |                
              |                 
            |               
                |                   
                           |___                         
        """,
    """
       _________
           |/       |     
           |       (_)   
                |       /|          
              |                 
            |               
                |                   
                        |___                     
        """,
    """
    ________
        |/   |     
        |   (_)    
               |   /|\           
        |           
       |          
            |               
                                |___                              
        """,
    """
    ________
        |/   |     
        |   (_)    
               |   /|\           
           |     |        
       |          
            |               
                               |___                             
        """,
    """
      ________
        |/   |     
        |   (_)    
               |   /|\           
          |    |        
         |   /        
           |               
                                  |___                                 
    """,
    """
       ________
        |/   |     
        |   (_)    
               |   /|\           
          |    |        
            |   / \        
            |               
             |___           
    """)
odkryte_litery = []  # to na serwerze ma być
result = ''  # to też
typeOfplayer = 0  # tutaj sobie zmieniaj kim chcesz być
isNameSent = False
firstMessage = False
firstSend = False
sendingPhrase=''
ArootA = Tk()
f1 = Frame(width=200, height=200, background="#FFFFFF")
f2 = Frame(ArootA, width=400, height=200)
f3 = Frame(ArootA, width=550, height=450)
f4 = Frame(ArootA, width=550, height=450)
TypingLabel = Label(f3, text='')
UsernNameLabel = Label(f3, text='')
TypingInputForWord = Entry(f3, width=50)
TypingButton = Button(f3, text='', command=NONE)
UserLabel = Label(f3, text='W grze: ')
listOfplayers = Listbox(f3, activestyle=DOTBOX,selectmode=SINGLE, height=20 )
InformationLabel = Label(f3, text='')
WisielecLabel = Label(f3, text='')
LettersLabel = Label(f3, text='')
TypingPassLabel = Label(f3, text='')
WinningLabel=Label(f3, text='')

class MakeTkInter:

    def __init__(self, resolution, nameofgame):

        ArootA.geometry(resolution)
        ArootA.title(nameofgame)
        f2.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
        f3.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
        f4.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)

    def LogIntoGame(self):  # tworzenie ekranu logowania
        global AnameEL
        global ErrorLabel
        global ArootA
        AnameL = Label(f2, text='Username: ')
        AnameL.grid(row=1, sticky=W)

        ErrorLabel = Label(f2, text='')
        ErrorLabel.grid(columnspan=2, sticky=W)

        AnameEL = Entry(f2)
        AnameEL.grid(row=1, column=1)

        AloginB = Button(f2, text='Start Game', command=self.JoinGame)
        AloginB.grid(columnspan=2, sticky=W)

    def JoinGame(self):
        global UserName
        if AnameEL.get() != "":
            UserName = AnameEL.get()
            f2.destroy()
            CreateView()
        else:
            ErrorLabel['fg'] = "red"
            ErrorLabel['text'] = "Put your name!!!"
def CreateView():
    global TypingInputForWord
    global TypingButton
    global InformationLabel
    global UsernNameLabel
    global TypingInputForWord
    global listOfplayers
    global WisielecLabel
    global UserLabel
    global hangman
    UsernNameLabel.grid(row=1, columnspan=4)
    TypingLabel.grid(row=2, column=1)
    TypingInputForWord.grid(row=3, columnspan=2, sticky=W)
    TypingButton.grid(row=3, column=4, sticky=W)
    listOfplayers.grid(rowspan=9, column=5)
    InformationLabel.grid(row=4, columnspan=2)
    LettersLabel.grid(row=5, columnspan=2)
    TypingPassLabel.grid(row=6, columnspan=2)
    WisielecLabel.grid(row=9, column=1)
    WinningLabel.grid(row=8, column=1)
    UserLabel.grid(row=3, column=5)
    UsernNameLabel['text'] = 'CZEKAJ NA RESZTE GRACZY'


def refresh(typeOfplayer):
    print('Refresh values for' + str(typeOfplayer))
    global TypingInputForWord
    global TypingButton
    global InformationLabel
    global UsernNameLabel
    global TypingInputForWord
    global listOfplayerss
    global WisielecLabel
    global UserLabel
    LettersLabel['text'] = "NIE TRAFIONE LITERY: A,F,G,H,J"
    TypingPassLabel['text'] = "Typowane hasło dsadsasdaasd"

    if typeOfplayer == 0:
        TypingInputForWord['state'] = NORMAL
        TypingButton['state'] = NORMAL
        UsernNameLabel['text'] = 'Gracz wymyślający: ' + UserName
        TypingLabel['text'] = 'Podaj słowo dla zgadujących: '
        TypingButton['text'] = 'ZadajPytanie'
        WisielecLabel['text'] = hangman[9]
        entry_text = StringVar()
        TypingInputForWord['textvariable'] = entry_text

        def CharacterLimit(entry_text):
            if len(entry_text.get()) > 0:
                if all(char.isalpha() for char in entry_text.get()):
                    pass
                else:
                    entry_text.set(entry_text.get().rstrip(entry_text.get()[-1]))
        entry_text.trace("w", lambda *args: CharacterLimit(entry_text))

    if typeOfplayer == 1:
        TypingInputForWord['state'] = NORMAL
        TypingButton['state'] = NORMAL
        UsernNameLabel['text'] = 'Gracz zgadujący: ' + UserName
        TypingLabel['text'] = 'Zgadnij litere z słowa'
        TypingButton['text'] = 'ZadajPytanie'
        WisielecLabel['text'] = ''
        entry_text = StringVar()
        TypingInputForWord['textvariable'] = entry_text

        def CharacterLimit(entry_text):
            if len(entry_text.get()) > 0:
                if all(char.isalpha() for char in entry_text.get()):
                    entry_text.set(entry_text.get()[-1])
                else:
                    entry_text.set('')
        entry_text.trace("w", lambda *args: CharacterLimit(entry_text))

view = MakeTkInter('1280x720', 'WisielecGame')
view.LogIntoGame()

ArootA.mainloop()

