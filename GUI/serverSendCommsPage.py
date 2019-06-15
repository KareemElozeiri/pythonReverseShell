from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from scrollableLabel import ScrollableLabel
from kivy.core.window import Window

class ServerSendCommsPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.MainApp = MainApp
        self.clientNum = self.MainApp.CurrentClientCard.client_num
        #taking care of the page widgets
        self.ShowCommRes = ScrollableLabel("Connected and in control of this machine")
        self.SendingCommBox = GridLayout(cols=3)
        self.CommInput = TextInput(hint_text="Type commands here")
        self.SendingCommButton = Button(text=">>")
        self.SendingCommButton.bind(on_press=self.SendCommToClient)
        self.returnButton = Button(text="Return")

        self.SendingCommBox.add_widget(self.CommInput)
        self.SendingCommBox.add_widget(self.SendingCommButton)
        self.SendingCommBox.add_widget(self.returnButton)

        self.add_widget(self.SendingCommBox)
        self.add_widget(self.ShowCommRes)

    def SendCommToClient(self,*_):
        Comm = self.CommInput.text
        self.CommInput.text = ""
        currentDir = self.MainApp.server.send_command("pwd",self.clientNum)
        commRes = self.MainApp.server.send_command(Comm,self.clientNum)
        self.ShowCommRes.updateContent(f"\n[color=00FF00]{currentDir}${Comm}[/color]\n[color=FF0000]{commRes}[/color]")
