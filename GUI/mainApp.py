import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
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

#making a special button for the initializing page
class TransformingButton(GridLayout):
    def __init__(self,main_text,secondary_buttons_text,**kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.cols = 1
        self.secondary_buttons = []
        self.splitted = False
        self.secondary_buttons_text = secondary_buttons_text
        for button_text in self.secondary_buttons_text:
            self.secondary_buttons.append(Button(text=button_text))
        self.main_button = Button(text=main_text)
        self.main_button.bind(on_press=self.split_button)
        self.add_widget(self.main_button)

    def split_button(self,_):
        #this code is for removing the main button and creating the secondary buttons
        self.splitted = True
        self.remove_widget(self.main_button)
        self.cols = len(self.secondary_buttons_text)
        for button in self.secondary_buttons:
            self.add_widget(button)

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
    def cancelTheAct(self,_):
        if self.server_button.splitted:
            self.CloseTransformingButton(self.server_button)
        else:
            self.CloseTransformingButton(self.client_button)

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
