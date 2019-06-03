import os

comm = os.popen("cd ..")
print(comm.read())
os.popen("mkdir hi")
