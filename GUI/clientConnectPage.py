from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from reverseShellClient import ClientReverseShell
from clientRecvCommPage import ClientRecvCommPage
from kivy.properties import BooleanProperty
from reverseShellServer import *
from reverseShellClient import *
import threading
#this page is for the user to connect as a client to a server
class ClientConnectPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.MainApp = MainApp
        self.cols = 1
        self.firstConnectButton = True
        self.username_input = TextInput(size_hint_y=0.2,height=30,multiline=False,hint_text="Enter your username")
        self.ip_input = TextInput(size_hint_y=0.2,height=30,multiline=False,hint_text="Type IP address")
        self.port_input = TextInput(size_hint_y=0.2,height=30,multiline=False,hint_text="Type port number")


        self.username_input.bind(text=self.enableConnection)
        self.ip_input.bind(text=self.enableConnection)
        self.port_input.bind(text=self.enableConnection)

        self.add_widget(self.username_input)
        self.add_widget(self.ip_input)
        self.add_widget(self.port_input)

    def connectToServer(self,*_):
        try:
            self.actingAsClient = True
            self.MainApp.username = self.username_input.text
            self.MainApp.targetedServerIp = self.ip_input.text
            self.MainApp.targetedServerPort = int(self.port_input.text.strip())

            self.MainApp.client = ClientReverseShell(self.MainApp.targetedServerIp,self.MainApp.targetedServerPort)
            self.MainApp.client.send_data(self.MainApp.username)
            #creating the page on which the user receives the commands
            self.MainApp.clientRecvCommPage = ClientRecvCommPage(self.MainApp)
            def client_backend_activation(*_):
                self.MainApp.RecvExec_Thread = threading.Thread(target=self.MainApp.clientRecvCommPage.recvAndExecComm,args=[])
                self.MainApp.RecvExec_Thread.start()
            self.MainApp.add_new_page(self.MainApp.clientRecvCommPage,"ClientRecvComm",client_backend_activation)
            #switching tp the page which displays the commands and their response
            self.MainApp.screen_manager.current = "ClientRecvComm"
        except:
            popup = Popup(title="Error",content=(Label(text="The IP or port given may be wrong!")),size_hint=(None,None),size=(250,250))
            self.username_input.text = ""
            self.ip_input.text = ""
            self.port_input.text = ""
            popup.open()

    def enableConnection(self,*_):
        if self.username_input.text != "" and self.ip_input.text != "" and self.port_input.text != "":
            if self.firstConnectButton:
                self.connect_button = Button(size_hint_y=0.2,height=30,text="Connect")
                self.connect_button.bind(on_press=self.connectToServer)
                self.add_widget(self.connect_button)
                self.firstConnectButton = False
        else:
            try:
                self.remove_widget(self.connect_button)
                self.firstConnectButton = True
            except:
                pass
