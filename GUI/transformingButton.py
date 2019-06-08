#the imports are for making the object independent of the project
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

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
