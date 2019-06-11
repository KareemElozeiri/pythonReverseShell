from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class ServerSendCommsPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.MainApp = MainApp
        self.ShowCommRes = Label(text="Connected and in control of this machine")
        self.SendingCommBox = GridLayout(cols=2)
        self.CommInput = TextInput(hint_text="Type commands here")
        self.SendingCommButton = Button(text=">>")
        self.SendingCommBox.add_widget(self.CommInput)
        self.SendingCommBox.add_widget(self.SendingCommButton)
        self.add_widget(self.SendingCommBox)
        self.add_widget(self.ShowCommRes)
