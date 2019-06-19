from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

class ScrollableLabel(ScrollView):
    def __init__(self,initialContent="",**kwargs):
        super().__init__(**kwargs)
        self.scroll_y = 0
        self.do_scroll_y = True
        self.bar_width = 10
        self.scroll_type = ['bars','content']
        self.bar_pos_y = "right"
        self.layout = GridLayout(size_hint_y=None,cols=1)
        self.contentLabel = Label(markup=True,text=initialContent,
        halign="center")
        self.scrollToPoint = Label()
        self.add_widget(self.layout)
        self.layout.add_widget(self.contentLabel)
        self.layout.add_widget(self.scrollToPoint)

    def updateContent(self,newContentToAdd):
        self.contentLabel.text += newContentToAdd
        self.layout.height = self.contentLabel.texture_size[1]
        self.contentLabel.height = self.contentLabel.texture_size[1]
        self.contentLabel.text_size = (self.contentLabel.width,None)
        self.scroll_to(self.scrollToPoint,animate=True)
