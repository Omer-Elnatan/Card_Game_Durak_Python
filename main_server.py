# -*- coding: utf-8 -*-
import threading
from threading import Lock
import socket





class Conversation(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address



    def run(self):
        global main_data
        global main_data_last_index
        client_data = self.client_socket.recv(1024)
        client_data = eval(str(client_data))
        client_data = list(client_data)
        print client_data


###################################################player handle
        if (client_data[0] == 'player') and (main_data_last_index >= 0):

            room_name = client_data[1]
            room_passward = client_data[2]
            found_room = False
            for x in range(main_data_last_index+1):
                if main_data[x]["room name"] == room_name:
                    if main_data[x]["room passward"] == room_passward:
                        self.client_socket.send(str((main_data[x]["room IP"], main_data[x]["room PORT"])))
                        found_room = True
                    else:
                        self.client_socket.send("Wrong passward")
            if found_room == False:
                self.client_socket.send("There is no room that called " + room_name)



        if (client_data[0] == 'player') and (main_data_last_index == -1):
            self.client_socket.send("There are no rooms")


###################################################room handle

        if (client_data[0] == 'room') and (client_data[1] != "exit"):
            room_name = client_data[1]
            room_passward = client_data[2]
            address = self.client_address
            room_IP = list(self.client_address)[0]
            room_PORT = list(self.client_address)[1]
            print room_passward
            lock.acquire()
            if main_data_last_index == -1:

                main_data.insert(0, {"room name": room_name, "room passward": room_passward, "room IP": room_IP, "room PORT": room_PORT})
                main_data_last_index += 1
                print main_data
                self.client_socket.send(str(self.client_address))

            else:
                passward_exist=False
                for x in range(main_data_last_index+1):
                    if room_passward == main_data[x]["room passward"]:
                        passward_exist = True


                if passward_exist == False:

                    main_data_last_index += 1
                    main_data.insert(main_data_last_index, {"room name": room_name, "room passward": room_passward, "room IP": room_IP, "room PORT": room_PORT})


                    self.client_socket.send(str(self.client_address))
                    print main_data

                if passward_exist == True:
                    self.client_socket.send("There is already a room with this passward")
            lock.release()



        elif (client_data[0] == 'room') and (client_data[1] == "exit"):
            lock.acquire()
            print "eyyyyyyyy " + str(main_data_last_index + 1)
            x = 0
            while(main_data_last_index >= x):
                print client_data[2]
                print main_data[x]["room passward"]
                if (str(self.client_address[0]) == str(main_data[x]["room IP"])) and (client_data[2] == str(main_data[x]["room passward"])):
                    main_data.remove(main_data[x])
                    x = x - 1
                    main_data_last_index = main_data_last_index-1
                    print main_data
                x = x + 1

            lock.release()




class Connection(threading.Thread):

    def __init__(self, server_socket):
        threading.Thread.__init__(self)
        self.server_socket = server_socket

    def run(self):
        while True:
            print 'waiting for connection.....'
            (client_socket, client_address) = self.server_socket.accept()
            print "get Connection From ", client_address
            con = Conversation(client_socket, client_address)
            con.start()




IP = '127.0.0.1'
PORT = 5001
lock = Lock()
main_data = []
main_data = list(main_data)
main_data_last_index = -1
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)
con = Connection(server_socket)
con.start()



