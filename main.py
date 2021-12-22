from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window


from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class ContainerBox(BoxLayout):
    pass


class VBoxWidget(Widget):
    pass


class HBoxWidget(Widget):
    pass


class Scroll(ScrollView):
    pass


class Header(AnchorLayout):
    pass


class Combined(BoxLayout):
    pass


class MainApp(App):
    def build(self):
        Window.size = (1360, 768)
        return Combined()
        # return ContainerBox()


MainApp().run()
