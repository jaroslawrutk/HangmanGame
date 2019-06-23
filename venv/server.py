
# server
import _thread
import socket
import ssl
import pickle
from tkinter import *

#zmienne
amountOfPlayers = 0
listOfPlayers = []
listOfPlayersClient = []
connected = False
receivedNames = False
firstMessage = False
phrase = ""
missedLetters = ""
allLetters = []
mistakes = 0
isSomeoneDisconnected = False
ArootA = Tk()
f1 = Frame(width=200, height=200, background="#FFFFFF")
f2 = Frame(ArootA, width=400, height=200)
f3 = Frame(ArootA, width=550, height=450)
f4 = Frame(ArootA, width=550, height=450)
UsernNameLabel = Label(f3, text='LOGS',justify=CENTER)
listOfplayersView = Listbox(f3, width=80)

class MakeTkInter:


    def __init__(self,resolution,nameofgame):
        global f1,f2,f3,f4
        ArootA.geometry(resolution)
        ArootA.title(nameofgame)
        f2.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
        f3.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
        f4.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)

    def LogIntoGame(self): #tworzenie ekranu logowania
        global AnameEL
        global ErrorLabel
        global ArootA
        AnameL = Label(f2, text='Podaj ilość graczy (min. 2): ')
        AnameL.grid(row=1, sticky=W)

        ErrorLabel = Label(f2, text='')
        ErrorLabel.grid(columnspan=2, sticky=W)

        AnameEL = Entry(f2)
        AnameEL.grid(row=1, column=1)

        AloginB = Button(f2, text='Rozpocznij gre', command=self.MakeGame)
        AloginB.grid(columnspan=2, sticky=W)

    def MakeGame(self):
        global amountOfPlayers
        if AnameEL.get() !="":
            try:
                amountOfPlayers = int(AnameEL.get())
                if (amountOfPlayers > 4 or amountOfPlayers < 2):
                    ErrorLabel['fg'] = "red"
                    ErrorLabel['text'] = "LICZBA NIE MIEŚCI SIĘ W PRZEDZIALE"
                else:
                    f2.destroy()
                    self.CreateView()
            except:
                ErrorLabel['fg'] = "red"
                ErrorLabel['text'] = "TO MUSI BY LICZBA"
        else:
          ErrorLabel['fg']="red"
          ErrorLabel['text'] = "WPROWADZ LICZBE GRACZY"

    def CreateView(self):
        global UsernNameLabel
        global listOfplayersView

        UsernNameLabel.grid(row=1,sticky=W+E)
        listOfplayersView.grid(row=2, columnspan=3)





class PlayerClient:
    def __init__(self, name = None):
        self.name = name


class Player:
    def __init__(self, client = None):
        self.client = client


class Datagram:
    def __init__(self, list = None, mainPhrase = None, type = None, missed = None, isEnd = None, mistakes = None):
        self.list = list
        self.phrase = mainPhrase
        self.type = type
        self.missedLetters = missed
        self.isEnd = isEnd
        self.mistakes = mistakes


#szyfrowanie
def secure():
    global context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.load_verify_locations(cafile="client.crt")


def connect():
    global firstMessage
    global phrase
    global missedLetters
    global connected
    global listOfplayers
    global mistakes
    global isSomeoneDisconnected
    guessedPhrase = ""
    while True:
        if not(connected):
            client, addr = s.accept()
            conn = context.wrap_socket(client, server_side=True)
            print("Połączono z graczem o adresie: ", addr[1])
            listOfplayersView.insert(END,"Połączono z graczem o adresie: "+ str(addr[1]))
            listOfPlayers.append(Player(conn))
            if(len(listOfPlayers) < amountOfPlayers):
                print("Jeszcze ", amountOfPlayers - len(listOfPlayers), " graczy.")
                UsernNameLabel['text']="Jeszcze ", amountOfPlayers - len(listOfPlayers), " graczy."
                listOfplayersView.insert(END, "Połączono z graczem o adresie: " + str(addr[1]))
                continue
            else:
                print("Zaczynamy!")
                connected = True
        while (True):
            #po raz pierwszy
            if not(firstMessage):
                firstMessage = True
                # odbieranie imion graczy
                for i in range(0, len(listOfPlayers)):
                    try:
                        listOfPlayers[i].client.send("Connected!".encode())
                    except:
                        # wiadomosc nie doszla
                        print("rozlaczylo jednego z graczy, koniec gry")
                        isSomeoneDisconnected = True
                        break
                if (isSomeoneDisconnected):
                    break
                for player in listOfPlayers:
                    try:
                        name = player.client.recv(1024).decode()
                        listOfPlayersClient.append(PlayerClient(name))
                    except:
                        print("rozlaczylo jednego z graczy, koniec gry")
                        isSomeoneDisconnected = True
                        break
                if (isSomeoneDisconnected):
                    break
                for i in range(0, len(listOfPlayers)):
                    datagram = Datagram(listOfPlayersClient, guessedPhrase, i, missedLetters, (False, False), mistakes)
                    pickleRick = pickle.dumps(datagram)
                    try:
                        listOfPlayers[i].client.send(pickleRick)
                    except:
                        # wiadomosc nie doszla
                        print("rozlaczylo jednego z graczy, koniec gry")
                        isSomeoneDisconnected = True
                        break
                if (isSomeoneDisconnected):
                    break
                #odbieranie hasła
                try:
                    data = (listOfPlayers[0].client.recv(1024)).decode()
                except:
                    # wiadomosc nie przyszla
                    print("rozlaczylo jednego z graczy, koniec gry")
                    break
                while not ("2137" in data):
                    try:
                        data += (listOfPlayers[0].client.recv(1024)).decode()
                    except:
                        # wiadomosc nie przyszla
                        print("rozlaczylo jednego z graczy, koniec gry")
                        isSomeoneDisconnected = True
                        break
                if (isSomeoneDisconnected):
                    break
                data = data.split("2137")[0].upper()
                phrase = data
                #tworzenie odgadnietego hasła
                for j in phrase:
                    guessedPhrase += "_ "
                #wysylanie danych z haslem i missedLetters
                for i in range(0, len(listOfPlayers)):
                    datagram = Datagram(listOfPlayersClient, guessedPhrase, i, missedLetters, (False, False), mistakes)
                    pickleRick = pickle.dumps(datagram)
                    try:
                        listOfPlayers[i].client.send(pickleRick)
                    except:
                        # wiadomosc nie doszla
                        print("rozlaczylo jednego z graczy, koniec gry")
                        isSomeoneDisconnected = True
                        break
                if (isSomeoneDisconnected):
                    break
                print(phrase, guessedPhrase)
            #kolejne razy
            else:
                try:
                    data = (listOfPlayers[1].client.recv(1024)).decode()
                except:
                    # wiadomosc nie przyszla
                    print("rozlaczylo jednego z graczy, koniec gry")
                    break
                data = data.upper()
                allLetters.append(data)
                # edycja guessedPhrase jesli zgadl
                if(data in phrase and not data in guessedPhrase):
                    temp = ''.join([letter if letter in allLetters else '_ ' for letter in phrase])
                    guessedPhrase = temp
                    if (guessedPhrase == phrase):
                        # wygranko zgadujacych
                        print("koniec gry, wygrana zgadujących")
                        for i in range(0, len(listOfPlayers)):
                            datagram = Datagram(listOfPlayersClient, guessedPhrase, i, missedLetters, (True, True), mistakes)
                            pickleRick = pickle.dumps(datagram)
                            try:
                                listOfPlayers[i].client.send(pickleRick)
                            except:
                                # wiadomosc nie doszla
                                print("rozlaczylo jednego z graczy, koniec gry")
                                break
                        break
                # edycja missedLetters jesli nie zgadl
                else:
                    mistakes += 1
                    if (mistakes == 10):
                        # przegranko
                        print("koniec gry, wygrana wymyslajacego")
                        for i in range(0, len(listOfPlayers)):
                            datagram = Datagram(listOfPlayersClient, guessedPhrase, i, missedLetters, (True, False), mistakes)
                            pickleRick = pickle.dumps(datagram)
                            try:
                                listOfPlayers[i].client.send(pickleRick)
                            except:
                                # wiadomosc nie doszla
                                print("rozlaczylo jednego z graczy, koniec gry")
                                isSomeoneDisconnected = True
                                break
                        print("brejk 1")
                        break
                    if not(data in missedLetters):
                        missedLetters += data + ", "
                    # przesunięcie listy jesli nie zgadl
                    moveList()
                    moveListClient()
                    for item in listOfPlayersClient:
                        print(item.name)
                # wysylanie informacji do wszystkich graczy kto akurat zgaduje
                for i in range(0, len(listOfPlayers)):
                    datagram = Datagram(listOfPlayersClient, guessedPhrase, i, missedLetters, (False, False), mistakes)
                    pickleRick = pickle.dumps(datagram)
                    try:
                        listOfPlayers[i].client.send(pickleRick)
                    except:
                        # wyrzucic z listy, jesli to gracz 0 to koniec gry
                        # wiadomosc nie doszla
                        print("rozlaczylo jednego z graczy, koniec gry")
                        isSomeoneDisconnected = True
                        break
                if (isSomeoneDisconnected):
                    break
        break


def moveList():
    global listOfPlayers
    temp = listOfPlayers[1]
    tempList = []
    tempList.insert(0, listOfPlayers[0])
    for i in range(2, len(listOfPlayers)):
        tempList.insert(i-1, listOfPlayers[i])
    tempList.insert(len(listOfPlayers) - 1, temp)
    listOfPlayers = tempList


def moveListClient():
    global listOfPlayersClient
    temp = listOfPlayersClient[1]
    tempList = []
    tempList.insert(0, listOfPlayersClient[0])
    for i in range(2, len(listOfPlayersClient)):
        tempList.insert(i-1, listOfPlayersClient[i])
    tempList.insert(len(listOfPlayersClient) - 1, temp)
    listOfPlayersClient = tempList



view = MakeTkInter('500x500', 'WIsielecGame')
view.LogIntoGame()

secure()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1769))
s.listen(5)
_thread.start_new_thread(connect,())

ArootA.mainloop()




