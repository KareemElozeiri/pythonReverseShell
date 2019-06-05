import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager , Screen
from time import sleep
kivy.require("1.10.1")

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


class InitializingPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="some shitty testing.."))

class UnderControl(App):
    def build(self):
        self.screen_manager = ScreenManager()
        #adding the intro page of the app to the app screen manager
        self.introPage =  IntroPage()
        self.screen = Screen(name="Intro")
        self.screen.add_widget(self.introPage)
        self.screen_manager.add_widget(self.screen)
        #adding the the initializing page to the app screen manager
        self.initializingPage = InitializingPage()
        self.screen = Screen(name="Initialize")
        self.screen.add_widget(self.initializingPage)
        self.screen_manager.add_widget(self.screen)


        return self.screen_manager



if __name__ == "__main__":
    myApp = UnderControl()
    myApp.run()
