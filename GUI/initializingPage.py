from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from transformingButton import TransformingButton
from reverseShellServer import *
from reverseShellClient import *
#this page is for choosing whether the device will act server/client
class InitializingPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.MainApp = MainApp
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
        try:
            self.MainApp.server_port = 9999
            self.MainApp.server = ReverseShellServer(self.MainApp.server_port)
        except Exception as err:
            self.MainApp.serverMainPage.info_label.text = str(err)

        self.MainApp.actingAsServer = True
        self.MainApp.screen_manager.current = "ServerConnections"


    def goToClient(self,*_):
        self.actingAsClient = True
        self.MainApp.screen_manager.current = "ClientConnectToServer"
