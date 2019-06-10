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
from reverseShellClient import ClientReverseShell
from time import sleep
import threading
kivy.require("1.10.1")


class UnderControl(App):
    def build(self):
        self.gui_running = True
        self.actingAsServer = False
        self.screen_manager = ScreenManager()
        #adding the intro page of the app to the app screen manager
        self.introPage =  IntroPage(self)
        self.add_new_page(self.introPage,"Intro")
        #adding the the initializing page to the app screen manager
        self.initializingPage = InitializingPage(self)
        self.add_new_page(self.initializingPage,"Initialize")
        #adding the server page to the app screen manager
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
        #adding the page the client page that shows the server sent commands and their response to the user
        self.clientRecvCommPage = ClientRecvCommPage(self)
        self.add_new_page(self.clientRecvCommPage,"ClientRecvComm")

        return self.screen_manager

    def add_new_page(self,page,screen_name,on_enter_func=None):
        self.screen = Screen(name=screen_name)
        self.screen.add_widget(page)
        if on_enter_func != None:
            self.screen.bind(on_enter=on_enter_func)
        self.screen_manager.add_widget(self.screen)

    def on_stop(self):
        self.gui_running = False
        #making a flase client to termainate the acceptance_thread of the app
        if self.actingAsServer:
            fakeClient = ClientReverseShell("localhost",self.server_port)






if __name__ == "__main__":
    myApp = UnderControl()
    myApp.run()
