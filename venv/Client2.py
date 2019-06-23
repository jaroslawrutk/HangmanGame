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
listOfplayers = Listbox(f3)
InformationLabel = Label(f3, text='')
WisielecLabel = Label(f3, text='')
LettersLabel = Label(f3, text='')
TypingPassLabel = Label(f3, text='')
WinningLabel=Label(f3, text='')

ConntectErrorConncet=Label(f3, text='')

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="server.crt")
context.load_cert_chain(certfile="client.crt", keyfile="client.key")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname="localhost")



class PlayerClient:
    def __init__(self, name=None, address=None):
        self.name = name


class Datagram:
    def __init__(self, list = None, mainPhrase = None, type = None, missed = None, isEnd = None, mistakes = None):
        self.list = list
        self.phrase = mainPhrase
        self.type = type
        self.missedLetters = missed
        self.isEnd = isEnd
        self.mistakes = mistakes


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
        AnameL = Label(f2, text='Nazwa gracza: ')
        AnameL.grid(row=1, sticky=W)

        ErrorLabel = Label(f2, text='')
        ErrorLabel.grid(columnspan=2, sticky=W)

        AnameEL = Entry(f2)
        AnameEL.grid(row=1, column=1)

        ConntectErrorConncet.grid(row=9,column=1)

        AloginB = Button(f2, text='Dojdz do gry', command=self.JoinGame)
        AloginB.grid(columnspan=2, sticky=W)

    def JoinGame(self):
        global UserName
        if AnameEL.get() != "":
            UserName = AnameEL.get()
            f2.destroy()
            _thread.start_new_thread(connect, (UserName,))

        else:
            ErrorLabel['fg'] = "red"
            ErrorLabel['text'] = "Pole nie może być puste!!!"


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
    InformationLabel.grid(row=4, columnspan=2)
    LettersLabel.grid(row=5, columnspan=2)
    TypingPassLabel.grid(row=6, columnspan=2)
    WinningLabel.grid(row=7, columnspan=1)
    WisielecLabel.grid(row=7, columnspan=2)
    listOfplayers.grid(row=6, column=6)
    UserLabel.grid(row=6, column=5)
    UsernNameLabel['text'] = 'CZEKAJ NA RESZTE GRACZY.'

    TypingInputForWord['state'] = DISABLED
    TypingButton['state'] = DISABLED


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

    if typeOfplayer == 0:
        if firstMessage == True:
            TypingInputForWord['state'] = NORMAL
            TypingButton['state'] = NORMAL
        else:
            TypingInputForWord['state'] = DISABLED
            TypingButton['state'] = DISABLED
        UsernNameLabel['text'] =  'Gracz: ' + UserName
        TypingLabel['text'] = 'Podaj hasło do zgadnięcia: '
        TypingButton['text'] = 'Wyślij'
        WisielecLabel['text'] = ''
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
        UsernNameLabel['text'] = 'Gracz: ' + UserName
        TypingLabel['text'] = 'Zgadnij litere ze słowa'
        TypingButton['text'] = 'Wyślij'
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

    if typeOfplayer == 2:
        UsernNameLabel['text'] = 'Gracz: ' + UserName
        TypingLabel['text'] = 'Czekaj na swoją kolej.'
        TypingButton['text'] = 'Wyślij'
        WisielecLabel['text'] = ''
        TypingInputForWord['state'] = DISABLED
        TypingButton['state'] = DISABLED


def connect(Username):
    global TypingInputForWord
    global TypingButton
    global InformationLabel
    global UsernNameLabel
    global TypingInputForWord
    global listOfplayers
    global WisielecLabel
    global isNameSent
    global firstMessage
    global s
    global conn
    TypingButton['state'] = NORMAL
    try:
        conn.connect(("127.0.0.1", 1769))
        CreateView()
    except socket.error as e:
        pass

       # ConntectErrorConncet['fg']="red"
       # ConntectErrorConncet['text']="Wystąpił błąd połączenia: " +str(e)

    while True:
        try:
            if not (isNameSent):
                data = conn.recv(1024).decode()
                while not ("Connected!" in data):
                    data += conn.recv(1024).decode()
                conn.send(Username.encode('utf-8'))
                # polączeni
                isNameSent = True
            if not (firstMessage):
                firstMessage = True
                data = conn.recv(1024)
                try:
                    unpickledRick = pickle.loads(data)
                except:
                    print("rozłączyło z serwerem, koniec gry")
                    break
                listOfplayers.delete('0', 'end')
                i=0
                for item in unpickledRick.list:
                    if i == 0:
                        listOfplayers.insert(END, item.name + ' - Wymyślający')
                    elif i == 1:
                        listOfplayers.activate(1)
                        listOfplayers.insert(END, item.name + ' - Zgadujący')
                    else:
                        listOfplayers.insert(END, item.name + ' - W kolejce')
                    i = i + 1
                if (unpickledRick.type == 0):
                    if(firstSend==False):
                        refresh(unpickledRick.type)
                    TypingButton['command'] = SendFirst
                else:
                     refresh(2)
                continue
            else:
                    data = conn.recv(1024)
                    try:
                        unpickledRick = pickle.loads(data)
                    except:
                        print("rozłączyło z serwerem, koniec gry")
                        break
                    if (unpickledRick.isEnd[0]):
                        if (unpickledRick.isEnd[1]):
                            if not (unpickledRick.type == 0):
                                WinningLabel['fg'] = "green"
                                WinningLabel['text'] = "WYGRAŁEŚ"
                                TypingInputForWord['state'] = DISABLED
                                TypingButton['state'] = DISABLED
                            else:
                                WinningLabel['fg'] = "red"
                                WinningLabel['text'] = "PRZEGRAŁEŚ"
                                TypingInputForWord['state'] = DISABLED
                                TypingButton['state'] = DISABLED
                        else:
                            if not (unpickledRick.type == 0):
                                WinningLabel['fg'] = "red"
                                WinningLabel['text'] = "PRZEGRAŁEŚ"
                                TypingInputForWord['state'] = DISABLED
                                TypingButton['state'] = DISABLED
                            else:
                                WinningLabel['fg'] = "green"
                                WinningLabel['text'] = "WYGRAŁEŚ"
                                TypingInputForWord['state'] = DISABLED
                                TypingButton['state'] = DISABLED
                        break
                    print(unpickledRick.phrase, unpickledRick.type, unpickledRick.missedLetters)
                    i = 0
                    role = ''
                    listOfplayers.delete('0', 'end')
                    for item in unpickledRick.list:
                        if i == 0:
                            listOfplayers.insert(END, item.name + ' - Wymyślający')
                        elif i == 1:
                            listOfplayers.insert(END, item.name + ' - Zgadujący')
                        else:
                            listOfplayers.insert(END, item.name + ' - W kolejce')
                        i=i+1

                    if (unpickledRick.type == 1):
                        refresh(unpickledRick.type)
                        TypingPassLabel['text'] = str(unpickledRick.phrase)
                        LettersLabel['text'] = "NIETRAFIONE LITERY: " + str(unpickledRick.missedLetters)
                        WisielecLabel['text'] = hangman[int(unpickledRick.mistakes)]
                        print("typ "+str(unpickledRick.type))
                        TypingButton['command'] = Send
                    elif (unpickledRick.type == 0):
                        InformationLabel['text'] ="Twoje hasło: " + TypingInputForWord.get()
                        print("typ "+str(unpickledRick.type))
                        LettersLabel['text']="NIETRAFIONE LITERY: " + str(unpickledRick.missedLetters)
                        TypingPassLabel['text']="Typowane hasło: "+ str(unpickledRick.phrase)
                        WisielecLabel['text'] = hangman[int(unpickledRick.mistakes)]
                        TypingInputForWord['state'] = DISABLED
                        TypingButton['state'] = DISABLED
                    else:
                        TypingPassLabel['text'] = str(unpickledRick.phrase)
                        LettersLabel['text'] = "NIETRAFIONE LITERY: " + str(unpickledRick.missedLetters)
                        WisielecLabel['text'] = hangman[int(unpickledRick.mistakes)]
                        TypingInputForWord['state'] = DISABLED
                        TypingButton['state'] = DISABLED

        except:
            print("Błąd połączenia!")
            break




def Send():
    global TypingButton, TypingInputForWord, s, conn
    sendingLetter = TypingInputForWord.get()
    conn.send(sendingLetter.encode('utf-8'))

def SendFirst():
    global TypingButton,TypingInputForWord,s,conn,firstSend
    firstSend = True
    InformationLabel['text'] = TypingInputForWord.get()
    sendingPhrase = TypingInputForWord.get()+"2137"
    conn.send(sendingPhrase.encode('utf-8'))
    TypingInputForWord['state'] = DISABLED
    TypingButton['state'] = DISABLED



view = MakeTkInter('500x700', 'WisielecGame')
view.LogIntoGame()

ArootA.mainloop()

