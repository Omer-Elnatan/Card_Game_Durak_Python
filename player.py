import threading
from threading import Lock
stop_event = threading.Event()
















def Close_Room():

    global PlayerList, PlayerListLastIndex, room_ready_button, round_is_on, disconnect_from_server, WaitingForPlayersLable, close_room
    close_room = True
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))
    my_socket.send(str(("room","exit")))
    my_socket.close()

    PlayerList=[0]
    PlayerListLastIndex = -1
    room_ready_button = 0
    round_is_on = False
    disconnect_from_server = False
    WaitingForPlayersLable = 0
    close_room = False
    MainWindow()





def listener(Soc):
    Soc.setblocking(False)
    try:
        return Soc.recv(4000)
    except socket.error:
        return None









class enough_player(threading.Thread):
    def __init__(self, PlayersNum):
        threading.Thread.__init__(self)
        self.PlayersNum = PlayersNum

    def run(self):
        global room_ready_button
        while PlayerListLastIndex < 1:
            pass
        room_ready_button["state"] = tk.ACTIVE











#room conversation with every client******************************************

class Conversation(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address




    def run(self):
        global PlayerList, round_is_on, PlayerListLastIndex, WaitingForPlayersLable, close_room


        client_name = self.client_socket.recv(1024)
        print client_name
        can_join = False

        lock.acquire()
        if PlayerListLastIndex == -1:
            PlayerList[0] = {"player name": client_name , "player socket": self.client_socket, "player address": self.client_address}
            PlayerListLastIndex=0
            self.client_socket.send("you have joined")
            can_join = True


        elif (PlayerListLastIndex <= 6) and (ThereIsName(client_name) == False):
            PlayerListLastIndex += 1
            PlayerList.insert(PlayerListLastIndex, {"player name": client_name, "player socket": self.client_socket, "player address": self.client_address})
            self.client_socket.send("you have joined")
            can_join = True

        elif (PlayerListLastIndex <= 6) and (ThereIsName(client_name) == True):
            self.client_socket.send("someone has already that name")

        elif PlayerListLastIndex >= 6:
            self.client_socket.send("the room is full")

        lock.release()


        if can_join == True:

            WaitingForPlayersLable = tk.Label(root, text="waiting for players...\n" + "you need at least 4 players including you\n" + "now you have " + str(PlayerListLastIndex+2), width=30, height=10, font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")
            WaitingForPlayersLable.place(x=400, y=10)







        boo = False
        waiting_to_play = False
        previous_num_of_players = 0

        if round_is_on == False:

            self.client_socket.send(str(("hello " + client_name + " ,waiting for players", str(PlayerListLastIndex+2))))
            previous_num_of_players = str(PlayerListLastIndex+2)
            waiting_to_play = True
        while round_is_on == False:
            if close_room != True:
                responde = listener(self.client_socket)
                if responde == "disconnecting":
                    lock.acquire()
                    PlayerListLastIndex = int(PlayerListLastIndex)
                    for x in PlayerList:
                        print "ey"
                        print x
                        if x["player name"] == client_name:
                            print x
                            print "ey"
                            print PlayerList
                            PlayerList.remove(x)
                    PlayerListLastIndex = PlayerListLastIndex-1
                    if PlayerListLastIndex == -1:
                        PlayerList=[0]
                    lock.release()
                    WaitingForPlayersLable = tk.Label(root, text="waiting for players...\n" + "you need at least 4 players including you\n" + "now you have " + str(PlayerListLastIndex+2), width=30, height=10, font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")
                    WaitingForPlayersLable.place(x=400, y=10)
                    self.client_socket.close()
                    print "cccccccc"
                    boo = True
                    break




                #if int(previous_num_of_players) != int(PlayerListLastIndex)+2:
                 #   previous_num_of_players = str(PlayerListLastIndex+2)
                 #   self.client_socket.send(str(PlayerListLastIndex+2))

            else:
                self.client_socket.send("disconnecting")
                self.client_socket.close()
                self._stop()
        if boo == False:



            if (round_is_on == True) and (waiting_to_play == False):
                self.client_socket.send(str(("hello " + client_name + " ,please wait for the next round", str(PlayerListLastIndex+2))))



            if (round_is_on == True) and (waiting_to_play == True):
                self.client_socket.send("hello " + client_name + " ,lets play")

            while (round_is_on == True) and (waiting_to_play == True):

                self.client_socket.send('v')
                pass


    def _stop(self):
        if self.isAlive():
            threading.Thread._Thread__stop(self)








#connection to client***************************************************************

class Connection(threading.Thread):
    def __init__(self, server_socket):
        threading.Thread.__init__(self)
        self.server_socket = server_socket

    def run(self):
        global PlayerList, PlayerListLastIndex, room_ready_button, round_is_on, disconnect_from_server, WaitingForPlayersLable, close_room
        print close_room
        while close_room == False:
            print 'waiting for connection.....'
            (client_socket, client_address) = self.server_socket.accept()
            print "get Connection From ", client_address
            conver = Conversation(client_socket, client_address)
            conver.start()







    def _stop(self):
        if self.isAlive():
            threading.Thread._Thread__stop(self)









#check if the room is playing a round*********************************

def Round_is_on():
    global round_is_on
    round_is_on = True

def Disconnect_From_Server():
    global disconnect_from_server
    disconnect_from_server = True




#client wait and play******************************************************

def ClientGame(my_socket, my_name):
    global disconnect_from_server
    for widget in root.winfo_children():
        widget.destroy()
    color=(0, 85, 51)
    tk_rgb = "#%02x%02x%02x" % color
    root["background"] = tk_rgb
    root.geometry("1300x800+30+30")
    print "joined"

    responde = my_socket.recv(1024)
    responde = eval(responde)
    responde = list(responde)

    BackArrowButton = tk.Button(root,image=BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised",command=Disconnect_From_Server)
    BackArrowButton.place(x=0, y=0)


    while responde[0] == str("hello " + my_name + " ,waiting for players"):




        WaitingForPlayersLable = tk.Label(root, text="waiting for players...\n" + "you need at least 4 players including you\n" + "now you have " + str(responde[1]), width=30, height=10, font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")
        WaitingForPlayersLable.place(x=400, y=10)
        root.update_idletasks()
        root.update()


        num = responde[1]
        while str(num) != str("hello " + my_name + " ,lets play"):
            if str(num) == "disconnecting":
                print "333"
                my_socket.close()
                showinfo("About ImageEditor1.0", "The room creator closed the room")
                MainWindow()
            if disconnect_from_server == True:
                my_socket.send("disconnecting")
                my_socket.close()
                disconnect_from_server = False
                MainWindow()
            num = listener(my_socket)

            if (str(num) != str("hello " + my_name + " ,lets play")) and (str(num) != "None"):

                WaitingForPlayersLable = tk.Label(root, text="waiting for players...\n" + "you need at least 4 players including you\n" + "now you have " + str(num) + "...", width=30, height=10, font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")

                WaitingForPlayersLable.place(x=400, y=10)

            elif str(num) != "None":

                responde[0] = num

            root.update_idletasks()
            root.update()


    while responde[0] == str("hello " + my_name + " ,please wait for the next round"):
        if disconnect_from_server == True:
            my_socket.send("disconnecting")
            my_socket.close()
            disconnect_from_server = False
            MainWindow()
        WaitingForPlayersLable = tk.Label(root, text="wait to the next round \n", width=30, height=5, font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")
        WaitingForPlayersLable.place(x=400, y=200)
        root.update_idletasks()
        root.update()


    if responde[0] == str("hello " + my_name + " ,lets play"):
        sever_data = my_socket.recv(1024)






#if there is already this name in the room******************************************

def ThereIsName(name):
    global PlayerList, PlayerListLastIndex
    for x in range(PlayerListLastIndex+1):
        if name == PlayerList[x]["player name"]:
            return True
    return False





#waiting for players*****************************************************

def StartRoom(My_Address):
    global room_ready_button, round_is_on
    for widget in root.winfo_children():
            widget.destroy()

    color=(0, 85, 51)
    tk_rgb = "#%02x%02x%02x" % color
    root["background"] = tk_rgb
    root.geometry("1300x800+30+30")
    print "room created"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    My_Address = eval(My_Address)
    server_socket.bind(My_Address)
    server_socket.listen(1)
    BackArrowButton = tk.Button(root,image=BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised",command=Close_Room)
    BackArrowButton.place(x=0, y=0)
    WaitingForPlayersLable = tk.Label(root, text="waiting for players...\n" + "you need at least 4 players including you\n" + "now you have " + str(PlayerListLastIndex+2), width=30, height=10, font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")

    con = Connection(server_socket)
    con.start()

    room_ready_button = tk.Button(root, bg=tk_rgb, fg='yellow', relief="raised", width=20, height=3 ,state=tk.DISABLED, text="Ready", font="Times 15 bold", command=Round_is_on)

    eno = enough_player(PlayerListLastIndex)
    eno.start()


    WaitingForPlayersLable.place(x=400, y=10)
    room_ready_button.place(x=460, y=400)

    root.update_idletasks()
    root.update()
    #while True:
    if close_room == True:
        con._stop()







#player join room***********************************************************************

def JoinRoomStartGame(room_address, my_name):
    print room_address

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    room_address = eval(room_address)
    my_socket.connect(room_address)
    my_socket.send(my_name)
    server_responde = my_socket.recv(1024)

    if server_responde == "you have joined":
        ClientGame(my_socket, my_name)

    else:
        showerror("About ImageEditor1.0", server_responde)
        JoinRoom()








#connect to the main server as a room******************************************************************

def SignInRoom():
    global SEnterYourNameEntry, SEnterServerNameEntry, SEnterPasswardOfServerEntry
    the_passward=SEnterPasswardOfServerEntry.get()
    room_name = SEnterServerNameEntry.get()
    if(SEnterYourNameEntry.get() == "") or (SEnterServerNameEntry.get() == "") or (SEnterPasswardOfServerEntry.get() == ""):
        showwarning("About ImageEditor1.0", "At least one of the fields is missing!")
    else:


        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((IP, PORT))

        my_socket.send(str(("room", room_name, the_passward)))
        server_responde = my_socket.recv(1024)
        print server_responde
        if server_responde[0] == "(":
            my_socket.close()
            StartRoom(server_responde)
        if server_responde == "There is already a room with this passward":
            showinfo("About ImageEditor1.0", "There is already a room with this passward")
    root.mainloop()






#connect to the main server as a player******************************************************************
def SignInClient():
    global CEnterYourNameEntry, CEnterServerNameEntry, CEnterPasswardOfServerEntry
    my_name = CEnterYourNameEntry.get()
    the_passward= CEnterPasswardOfServerEntry.get()
    room_name = CEnterServerNameEntry.get()
    if(CEnterYourNameEntry.get() == "") or (CEnterServerNameEntry.get() == "") or (CEnterPasswardOfServerEntry.get() == ""):
        showwarning("About ImageEditor1.0", "At least one of the fields is missing!")

    else:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((IP, PORT))

        my_socket.send(str(("player", room_name, the_passward)))
        server_responde = my_socket.recv(1024)

        if server_responde == "Wrong passward":
            showerror("About ImageEditor1.0", "Wrong passward")

        if (server_responde != "Wrong passward") and (server_responde[0] != "("):
            showerror("About ImageEditor1.0", server_responde)

        if server_responde[0] == "(":
            my_socket.close()
            JoinRoomStartGame(server_responde, my_name)

    root.mainloop()


#show rules**********************************************************************8

def ShowRules():
    global lastWindow
    w = Canvas(root, width=990, height=800,scrollregion=(0,0,1300,1200))
    BackImage = tk.PhotoImage(file='F:/BackArrow.gif')
    BackArrowButton = tk.Button(root,image = BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised",command=MainWindow)
    if (lastWindow=='main_window'):
        BackArrowButton = tk.Button(root,image = BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised",command=MainWindow)
    if (lastWindow=='create_room_window'):
        BackArrowButton = tk.Button(root,image = BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised",command=CreateRoom)
    if (lastWindow=='join_room_window'):
        BackArrowButton = tk.Button(root,image = BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised",command=JoinRoom)

    Rule1 = tk.PhotoImage(file ="F:/Rules1.gif")
    Rule2 = tk.PhotoImage(file ="F:/Rules2.gif")
    w.create_image(0, 0, image=Rule1, anchor="nw")
    w.create_image(0, 600, image=Rule2, anchor="nw")

    w.pack(padx=10,pady=10)
    BackArrowButton.grid(row=0, column=0,sticky=NSEW)

    w.grid(row=0, column=1,sticky=NSEW)
    scrollbar = Scrollbar(root,orient=VERTICAL)
    scrollbar.config(command=w.yview)
    w.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.LEFT,fill=Y)
    w.pack(side=tk.RIGHT,expand=YES,fill=BOTH)

    w.config(yscrollcommand=scrollbar.set)
    BackArrowButton.place(x=1224, y=0)



    root.mainloop()





#sign to create a room*************************************************************

def CreateRoom():
    global lastWindow, SEnterYourNameEntry, SEnterServerNameEntry, SEnterPasswardOfServerEntry


    lastWindow='create_room_window'
    for widget in root.winfo_children():
        widget.destroy()
    color=(0, 85, 51)
    tk_rgb = "#%02x%02x%02x" % color
    root["background"]=tk_rgb
    root.geometry("1300x800+30+30")


    SignInWindowLable = tk.Label(root, text="Sign in please", width=38, height=3, font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")
    BackImage = tk.PhotoImage(file='F:/BackArrow.gif')
    BackArrowButton = tk.Button(root,image = BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised", command=MainWindow)
    EnterYourNameLable = tk.Label(root, text="enter your name",width=38,height=3,font="Times 15", bg=tk_rgb, fg="yellow")
    SEnterYourNameEntry = tk.Entry(root, font='Arial 15', fg='black')

    EnterPasswardOfServerLable = tk.Label(root, text="enter the passward of the server",width=50,height=3,font="Times 15", bg=tk_rgb, fg="yellow")
    SEnterPasswardOfServerEntry = tk.Entry(root, font='Arial 15', fg='black')
    EnterServerNameLable = tk.Label(root, text="enter the name of the server",width=38,height=3,font="Times 15", bg=tk_rgb, fg="yellow")
    SEnterServerNameEntry = tk.Entry(root, font='Arial 15', fg='black')
    SignInButton = tk.Button(root, text='Sign in',font="Times 13 bold",width=5,height=3, relief="raised", bg=tk_rgb, fg="yellow", command=SignInRoom)
    ShowRulesButton= tk.Button(root, text='Rules',font="Times 13 bold",width=5,height=3, relief="raised", bg=tk_rgb, fg="yellow", command=ShowRules)
    SignInWindowLable.place(x=400, y=100)
    BackArrowButton.place(x=0, y=0)
    EnterYourNameLable.place(x=100, y=200)
    SEnterYourNameEntry.place(x=400, y=225)
    EnterPasswardOfServerLable.place(x=98, y=275)
    SEnterPasswardOfServerEntry.place(x=530, y=300)
    EnterServerNameLable.place(x=148, y=350)
    SEnterServerNameEntry.place(x=500, y=375)
    SignInButton.place(x=1200, y=700)
    ShowRulesButton.place(x=1120, y=700)
    SEnterPasswardOfServerEntry.focus_set()
    tk.mainloop()


#sign to join a room***********************************************************
def JoinRoom():
    global lastWindow, CEnterYourNameEntry, CEnterServerNameEntry, CEnterPasswardOfServerEntry
    lastWindow = 'join_room_window'
    for widget in root.winfo_children():
        widget.destroy()
    color=(0, 85, 51)
    tk_rgb = "#%02x%02x%02x" % color
    root["background"]=tk_rgb
    root.geometry("1300x800+30+30")
    SignInWindowLable = tk.Label(root, text="Sign in please",width=38,height=3,font="Times 15 bold",relief="sunken", bg=tk_rgb, fg="yellow")
    BackImage = tk.PhotoImage(file='F:/BackArrow.gif')
    BackArrowButton = tk.Button(root,image = BackImage, bg=tk_rgb,fg=tk_rgb, relief="raised", command=MainWindow)
    EnterYourNameLable = tk.Label(root, text="enter your name",width=38,height=3,font="Times 15", bg=tk_rgb, fg="yellow")
    CEnterYourNameEntry = tk.Entry(root, font='Arial 15', fg='black')
    CEnterPasswardOfServerLable = tk.Label(root, text="enter the passward of the server",width=50,height=3,font="Times 15", bg=tk_rgb, fg="yellow")
    CEnterPasswardOfServerEntry = tk.Entry(root, font='Arial 15', fg='black')
    EnterServerNameLable = tk.Label(root, text="enter the name of the server",width=38,height=3,font="Times 15", bg=tk_rgb, fg="yellow")
    CEnterServerNameEntry = tk.Entry(root, font='Arial 15', fg='black')
    SignInButton = tk.Button(root, text='Sign in',font="Times 13 bold",width=5,height=3, relief="raised", bg=tk_rgb, fg="yellow",command=SignInClient)
    ShowRulesButton= tk.Button(root, text='Rules',font="Times 13 bold",width=5,height=3, relief="raised", bg=tk_rgb, fg="yellow",command=ShowRules)
    SignInWindowLable.place(x=400, y=100)
    BackArrowButton.place(x=0, y=0)
    EnterYourNameLable.place(x=100, y=200)
    CEnterYourNameEntry.place(x=400, y=225)
    CEnterPasswardOfServerLable.place(x=98, y=275)
    CEnterPasswardOfServerEntry.place(x=530, y=300)
    EnterServerNameLable.place(x=148, y=350)
    CEnterServerNameEntry.place(x=500, y=375)
    SignInButton.place(x=1200, y=700)
    ShowRulesButton.place(x=1120, y=700)
    tk.mainloop()

#main window*************************************************************************
def MainWindow():
    global lastWindow
    lastWindow = 'main_window'
    for widget in root.winfo_children():
            widget.destroy()
    bg_image = tk.PhotoImage(file ="F:/background.gif")


    background = tk.Label(root, image = bg_image,width=1300,height=800)
    EnterCreateOrJoinLable = tk.Label(root, text="Do you want to create a room or join a room?",width=38,height=3,font="Times 15 bold",relief="solid", bg=tk_rgb, fg="yellow")
    JokerGameLable= tk.Label(root,text="This is the joker game",width=38,height=3,font="calibri 20 bold",relief="solid", bg=tk_rgb, fg="yellow")
    CreateRoomButton= tk.Button(root, text='Create',font="Times 10 bold",width=20,height=5,bg='Moccasin',command=CreateRoom)
    JoinRoomButton= tk.Button(root, text='Join',font="Times 10 bold",width=20,height=5,bg='Moccasin',command=JoinRoom)
    ShowRulesButton= tk.Button(root, text='Rules',font="Times 13 bold",width=5,height=3, relief="raised", bg='Moccasin', fg="black",command=ShowRules)


    JokerGameLable.place(x=400, y=20)
    background.place(x=0, y=0)
    EnterCreateOrJoinLable.place(x=440, y=130)
    CreateRoomButton.place(x= 150, y=200)
    JoinRoomButton.place(x= 1050, y=200)
    ShowRulesButton.place(x=1200, y=700)


    tk.mainloop()


#open screen*************************************************************
import socket
from Tkinter import *
from tkMessageBox import *
import Tkinter as tk



IP = '127.0.0.1'
PORT = 5000
color= (0, 85, 51)
lock = Lock()
PlayerList=[0]
PlayerListLastIndex = -1
room_ready_button = 0
round_is_on = False
disconnect_from_server = False
WaitingForPlayersLable = 0
close_room = False


root = tk.Tk()
tk_rgb = "#%02x%02x%02x" % color
#root["background"]=tk_rgb
root.geometry("1300x800+0+0")
root.resizable(width=tk.FALSE, height=tk.FALSE)
BackImage = tk.PhotoImage(file='F:/BackArrow.gif')

MainWindow()

