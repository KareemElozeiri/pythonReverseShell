import socket
import threading
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from serverSendCommsPage import ServerSendCommsPage

#this is the page for showing the clients of the server to the user(if there)
#and choosing a client to send commands to this machine
class ServerMainPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.MainApp = MainApp
        self.cols = 1
        self.info_label = Label(markup=True,font_size=20)
        self.info_label.text="Server is listening for connections..."
        self.add_widget(self.info_label)
        #creating and displaying the list of client of the server
        self.clients = []
        self.clientsList = GridLayout(cols=1)
        self.add_widget(self.clientsList)

    def server_conn_acceptance(self):
            while self.MainApp.gui_running:
                try:
                    self.MainApp.server.accept_conn()
                    client = self.MainApp.server.connections[-1]
                    #getting the client username
                    curr_client_num = self.MainApp.server.connections.index(client)
                    curr_client_username = self.MainApp.server.recv_data(curr_client_num)
                    client["username"] = curr_client_username
                    self.clientsList.add_widget(ClientCard(self.MainApp,client))
                except socket.error as err:
                    pass
#this widget is for the client card in the server page
class ClientCard(GridLayout):
    def __init__(self,MainApp,client,**kwargs):
        super().__init__(**kwargs)
        self.firstConnect = True
        self.cols = 3
        self.MainApp = MainApp
        self.username = client["username"]
        self.client_num = self.MainApp.server.connections.index(client)
        self.id = f"client{self.client_num}"
        self.client_ip = client["address"][0]
        self.client_port = client["address"][1]
        self.client_sock = client["Socket"]
        self.username_label = Label(text=self.username,font_size=12)
        self.address_label = Label(text=f"{self.client_ip}:{self.client_port}",font_size=10)
        self.connect_button = Button(text="Connect")
        self.connect_button.bind(on_press=self.connectToClient)
        #adding the card components
        self.add_widget(self.username_label)
        self.add_widget(self.address_label)
        self.add_widget(self.connect_button)

    def connectToClient(self,*_):
        self.MainApp.CurrentClientCard = self
        #creating the shell for the client of this card on first time of connection
        if self.firstConnect:
            self.serverSendCommsPage = ServerSendCommsPage(self.MainApp)
            self.MainApp.add_new_page(self.serverSendCommsPage,f"ServerSendComms{self.client_num}")
            self.firstConnect = False

        self.MainApp.screen_manager.current = f"ServerSendComms{self.client_num}"
