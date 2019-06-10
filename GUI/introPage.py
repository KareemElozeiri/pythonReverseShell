from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
#this page is just for showing the title of the app
class IntroPage(GridLayout):
    def __init__(self,MainApp,**kwargs):
        super().__init__(**kwargs)
        self.MainApp = MainApp
        self.cols = 1
        self.rows = 1
        self.title = Label(text="UnderControl",font_size=32)
        self.add_widget(self.title)
        Clock.schedule_once(self.change_to_initialize,3)

    def change_to_initialize(self,dt):
        self.MainApp.screen_manager.current = "Initialize"
