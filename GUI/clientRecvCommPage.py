from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
#this page is the page is supposed to display the commands sent by the server and
#displays their response and in its core the ClientReverseShell will perform its function(executing the commnand on the client machine)
class ClientRecvCommPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.MainApp = MainApp
        self.cols = 1
        self.add_widget(Label(text="Testing bitchhhh!!!"))
