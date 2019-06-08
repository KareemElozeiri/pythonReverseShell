#these two lines are for getting the ability to import files from the parent directory
import sys
sys.path.insert(0,"..")
#importing the modules for the project
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager , Screen
from time import sleep
from transformingButton import *
from reverseShellServer import *
from reverseShellClient import *
import threading
kivy.require("1.10.1")

#this page is just for showing the title of the app
class IntroPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1
        self.title = Label(text="UnderControl",font_size=32)
        self.add_widget(self.title)
        Clock.schedule_once(self.change_to_initialize,3)

    def change_to_initialize(self,dt):
        myApp.screen_manager.current = "Initialize"

#this page is for choosing whether the device will act server/client
class InitializingPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.server_button = TransformingButton("Act as a Server",["Initialize server","Cancel"])
        self.client_button = TransformingButton("Act as a client",["Initialize client","Cancel"])
        #preventing the displaying of the secondary buttons of the two objects at the same time
        self.server_button.main_button.fbind('on_press',self.CloseTransformingButton,self.client_button)
        self.client_button.main_button.fbind('on_press',self.CloseTransformingButton,self.server_button)
        #giving thee ability of canceling the operation
        self.server_button.secondary_buttons[1].bind(on_press=self.cancelTheAct)
        self.client_button.secondary_buttons[1].bind(on_press=self.cancelTheAct)
        #giving the initialize server button its functionlity
        self.server_button.secondary_buttons[0].bind(on_press=self.goToServer)
        #giving the initialize server button its functionlity
        self.client_button.secondary_buttons[0].bind(on_press=self.goToClient)

        self.add_widget(self.server_button)
        self.add_widget(self.client_button)

    #the logic that closes the secondary buttons of the TransformingButton
    def CloseTransformingButton(self,closedButton,*_):
        if closedButton.splitted:
            for button in closedButton.secondary_buttons:
                closedButton.remove_widget(button)
            closedButton.add_widget(closedButton.main_button)
        closedButton.splitted = False

    #the logic that cancels the performed operation
    def cancelTheAct(self,*_):
        if self.server_button.splitted:
            self.CloseTransformingButton(self.server_button)
        else:
            self.CloseTransformingButton(self.client_button)

    def goToServer(self,*_):
        myApp.screen_manager.current = "ServerConnections"
        try:
            myApp.server_port = 9999
            myApp.server = ReverseShellServer(myApp.server_port)
        except Exception as err:
            self.info_label.text = str(err)

    def goToClient(self,*_):
        myApp.screen_manager.current = "ClientConnectToServer"

#this class is for the client card in the server page
class clientCard(GridLayout):
    def __init__(self,client,**kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.username = client["username"]
        self.client_ip = client["address"][0]
        self.client_port = client["address"][1]
        self.client_sock = client["Socket"]
        self.username_label = Label(text=self.username,font_size=12)
        self.address_label = Label(text=f"{self.client_ip}:{self.client_port}",font_size=10)
        self.connect_button = Button(text="Connect")
        #adding the card components
        self.add_widget(self.username_label)
        self.add_widget(self.address_label)
        self.add_widget(self.connect_button)

#this is the page for showing the clients of the server to the user(if there)
#and choosing a client to send commands to this machine
class ServerPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.info_label = Label(font_size=20)
        self.info_label.text="Server is listening for connections..."
        self.add_widget(self.info_label)
        #creating and displaying the list of client of the server
        self.clients = []
        self.clientsList = GridLayout(cols=1)
        self.add_widget(self.clientsList)

    def server_conn_acceptance(self):
        while True:
            myApp.server.accept_conn()
            client = myApp.server.connections[-1]
            self.clientsList.add_widget(clientCard(client))

#this page is for the user to connect as a client to a server
class ClientPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.ip_input = TextInput(multiline=False,hint_text="Type IP address")
        self.port_input = TextInput(multiline=False,hint_text="Type port number")
        self.connect_button = Button(text="Connect")

        self.add_widget(self.ip_input)
        self.add_widget(self.port_input)
        self.add_widget(self.connect_button)

class UnderControl(App):
    def build(self):
        self.screen_manager = ScreenManager()
        #adding the intro page of the app to the app screen manager
        self.introPage =  IntroPage()
        self.add_new_page(self.introPage,"Intro")
        #adding the the initializing page to the app screen manager
        self.initializingPage = InitializingPage()
        self.add_new_page(self.initializingPage,"Initialize")
        #adding the server page to the app screen manager
        self.serverPage = ServerPage()
        self.add_new_page(self.serverPage,"ServerConnections")
        #adding the client page that connects the user's machine to the server
        self.clientPage = ClientPage()
        self.add_new_page(self.clientPage,"ClientConnectToServer")

        return self.screen_manager


    def add_new_page(self,page,screen_name):
        self.screen = Screen(name=screen_name)
        self.screen.add_widget(page)
        self.screen_manager.add_widget(self.screen)





if __name__ == "__main__":
    myApp = UnderControl()
    myApp.run()
