#these two lines are for getting the ability to import files from the parent directory
import sys
sys.path.insert(0,"..")
#importing the modules for the project
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager , Screen
from introPage import IntroPage
from initializingPage import InitializingPage
from serverMainPage import ServerMainPage , ClientCard
from clientConnectPage import ClientConnectPage
from clientRecvCommPage import ClientRecvCommPage
from serverSendCommsPage import ServerSendCommsPage
from reverseShellClient import ClientReverseShell
from time import sleep
from kivy.core.window import Window
import threading
kivy.require("1.10.1")


class UnderControl(App):
    def build(self):
        self.gui_running = True
        self.actingAsServer = False
        self.actingAsClient = False
        self.firstServerSendCommPage = True
        self.screen_manager = ScreenManager()
        #adding the intro page of the app to the app screen manager
        self.introPage =  IntroPage(self)
        self.add_new_page(self.introPage,"Intro")
        #adding the the initializing page to the app screen manager
        self.initializingPage = InitializingPage(self)
        self.add_new_page(self.initializingPage,"Initialize")
        #adding the server main page(that shows the clients list) to the app screen manager
        self.serverMainPage = ServerMainPage(self)
        self.first_enter_serverMainPage = True
        def server_backend_activation(*_):
            if self.first_enter_serverMainPage:
                self.acceptance_thread = threading.Thread(target=self.serverMainPage.server_conn_acceptance,args=[])
                self.acceptance_thread.start()
                self.first_enter_serverMainPage = False

        self.add_new_page(self.serverMainPage,"ServerConnections",server_backend_activation)
        #adding the client page that connects the user's machine to the server
        self.clientConnectPage = ClientConnectPage(self)
        self.add_new_page(self.clientConnectPage,"ClientConnectToServer")

        return self.screen_manager

    def add_new_page(self,page,screen_name,on_enter_func=None):
        self.screen = Screen(name=screen_name)
        self.screen.add_widget(page)
        if on_enter_func != None:
            self.screen.bind(on_enter=on_enter_func)
        self.screen_manager.add_widget(self.screen)

    def on_stop(self):
        self.gui_running = False
        #acts to be taken on closing the app in case it was acting as a server
        if self.actingAsServer:
            #closing the server connections
            for client in self.server.connections:
                client["Socket"].close()
            #making a flase client to termainate the acceptance_thread of the app
            fakeClient = ClientReverseShell("localhost",self.server_port)
            fakeClient.send_data("")
        elif self.actingAsClient:
            self.MainApp.client.sock.close()









if __name__ == "__main__":
    myApp = UnderControl()
    myApp.run()
