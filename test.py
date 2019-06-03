import os

comm = os.popen("ls")
print(comm.read())
