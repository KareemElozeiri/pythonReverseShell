from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
import os
#this page is the page is supposed to display the commands sent by the server and
#displays their response and in its core the ClientReverseShell will perform its function(executing the commnand on the client machine)
class ClientRecvCommPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.MainApp = MainApp
        self.cols = 1
        self.pageHead = Label(text="The commands sent to your machine")
        self.CommAndRes = Label()
        self.add_widget(self.pageHead)
        self.add_widget(self.CommAndRes)

    def recvAndExecComm(self):
        while self.MainApp.gui_running:
            self.MainApp.client.exec_command()
            self.CommAndRes.text += f"\n{os.getcwd()}${self.MainApp.client.comm_to_exec}\n{self.MainApp.client.comm_res}"
