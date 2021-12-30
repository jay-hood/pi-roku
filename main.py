from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
import threading
from roku import Roku


class Dummy:
    def __eq__(self, compare):
        if compare is False:
            return True
        return False

    def do_nothing(self):
        pass

    def __getattr__(self, name):
        return self.do_nothing


class DummyRoku(Dummy):
    def __init__(self):
        self.device_info = Dummy()


CURRENT_ROKU = DummyRoku()
ROKUS = None
EVENTS = {}


def register_event(name, callback):
    EVENTS[name] = callback


def call_event(name):
    try:
        EVENTS[name]()
    except Exception as e:
        print(e)


class ContainerBox(BoxLayout):
    def __init__(self, main_app):
        super().__init__()
        self.orientation = "horizontal"
        self.cbox = ControlBox()
        self.add_widget(self.cbox)
        self.scroll = Scroll(main_app)
        self.add_widget(self.scroll)


class ControlBox(Widget):
    def __init__(self):
        super().__init__()
        self.relay = RelativeLayout()
        self.relay.size = (100, 100)
        self.add_relay_buttons()
        self.gridlay = GridLayout()
        self.gridlay.cols = 5
        self.gridlay.rows = 2
        self.gridlay.size = (200, 250)
        self.gridlay.col_default_width = 150
        self.gridlay.spacing = 30
        self.gridlay.padding = [20, 0, 0, 50]
        self.add_gridlay_buttons()
        self.add_widget(self.relay)
        self.add_widget(self.gridlay)

    def up(*args):
        CURRENT_ROKU.up()

    def down(*args):
        CURRENT_ROKU.down()

    def select(*args):
        CURRENT_ROKU.select()

    def left(*args):
        CURRENT_ROKU.left()

    def right(*args):
        CURRENT_ROKU.right()

    def home(*args):
        CURRENT_ROKU.home()

    def back(*args):
        CURRENT_ROKU.back()

    def replay(*args):
        CURRENT_ROKU.replay()

    def info(*args):
        CURRENT_ROKU.info()

    def volume_mute(*args):
        CURRENT_ROKU.mute()

    def volume_up(*args):
        CURRENT_ROKU.volume_up()

    def volume_down(*args):
        CURRENT_ROKU.volume_down()

    def forward(*args):
        CURRENT_ROKU.forward()

    def play(*args):
        CURRENT_ROKU.play()

    def reverse(*args):
        CURRENT_ROKU.reverse()

    def add_relay_buttons(self):
        buttons = [
            ((1.25, 1.25), {"x": 4.00, "y": 5.75}, "UP", self.up),
            ((1.25, 1.25), {"x": 4.00, "y": 4.5}, "UP", self.select),
            ((1.25, 1.25), {"x": 4.00, "y": 3.25}, "UP", self.down),
            ((1.25, 1.25), {"x": 2.75, "y": 4.5}, "UP", self.left),
            ((1.25, 1.25), {"x": 5.25, "y": 4.5}, "UP", self.right),
        ]
        for button in buttons:
            btn = Button()
            btn.size_hint = button[0]
            btn.pos_hint = button[1]
            btn.text = button[2]
            btn.bind(on_press=button[3])
            self.relay.add_widget(btn)
        # btn1 = Button()
        # btn1.size_hint = (1.25, 1.25)
        # btn1.pos_hint = {"x": 4.00, "y": 5.75}
        # btn1.text = "UP"
        # btn1.bind(on_press=self.up)
        # btn2 = Button()
        # btn2.size_hint = (1.25, 1.25)
        # btn2.pos_hint = {"x": 4.00, "y": 4.5}
        # btn2.text = "OK"
        # btn2.bind(on_press=self.select)
        # btn3 = Button()
        # btn3.size_hint = (1.25, 1.25)
        # btn3.pos_hint = {"x": 4.00, "y": 3.25}
        # btn3.text = "DOWN"
        # btn3.bind(on_press=self.down)
        # btn4 = Button()
        # btn4.size_hint = (1.25, 1.25)
        # btn4.pos_hint = {"x": 2.75, "y": 4.5}
        # btn4.text = "LEFT"
        # btn4.bind(on_press=self.left)
        # btn5 = Button()
        # btn5.size_hint = (1.25, 1.25)
        # btn5.pos_hint = {"x": 5.25, "y": 4.5}
        # btn5.text = "RIGHT"
        # btn5.bind(on_press=self.right)
        # self.relay.add_widget(btn1)
        # self.relay.add_widget(btn2)
        # self.relay.add_widget(btn3)
        # self.relay.add_widget(btn4)
        # self.relay.add_widget(btn5)

    def add_gridlay_buttons(self):
        buttons = [
            ("REPLAY", self.replay),
            ("OPTIONS", self.info),
            ("HOME", self.home),
            ("BACK", self.back),
            ("MUTE", self.volume_mute),
            ("VOL UP", self.volume_up),
            ("VOL DOWN", self.volume_down),
            ("FF", self.forward),
            ("PLAY", self.play),
            ("REW", self.reverse),
        ]
        for btn in buttons:
            b = Button()
            b.text = btn[0]
            b.bind(on_press=btn[1])
            self.gridlay.add_widget(b)


class ScrollGrid(GridLayout):
    def __init__(self, parent):
        super().__init__()
        self.pos = parent.pos
        self.cols = 1
        self.row_default_height = 100
        self.row_force_default = True
        self.add_gridlay_buttons()
        register_event("add_gridlay_buttons", self.add_gridlay_buttons)

    def add_start_buttons(self):
        x = ["a", "b", "c"]
        for a in x:
            btn = Button()
            btn.text = a
            self.add_widget(btn)

    def add_gridlay_buttons(self):
        if CURRENT_ROKU != False:
            if self.children:
                for child in self.children:
                    self.remove_widget(child)
            for app in CURRENT_ROKU.apps:
                btn = Button()
                btn.text = app.name
                btn.bind(on_press=app.launch)
                self.add_widget(btn)


class Scroll(ScrollView):
    def __init__(self, main_app):
        super().__init__()
        self.size_hint_x = 0.5
        self.pos_hint = {"x": 0.5, "y": 0}
        self.orientation = "vertical"
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.gridlay = ScrollGrid(self)
        self.add_widget(self.gridlay)


class Header(AnchorLayout):
    def __init__(self, cbox):
        super().__init__()
        self.cbox = cbox
        self.size_hint = (1, 0.1)
        self.anchor_x = "center"
        self.anchor_y = "top"
        self.id = "header"
        self.box1 = BoxLayout()
        self.set_header_buttons()
        self.add_widget(self.box1)
        register_event("set_header_buttons", self.set_header_buttons)

    def set_header_buttons(self):
        if ROKUS is not None:
            for r in ROKUS:
                btn = ToggleButton()
                btn.group = "rokus"
                btn.size_hint_x = 0.5
                btn.text = r.device_info.model_name
                btn.bind(on_press=self.set_current_roku)
                self.box1.add_widget(btn)

    def set_current_roku(self, instance):
        global CURRENT_ROKU
        if ROKUS is not None:
            for r in ROKUS:
                if not CURRENT_ROKU or (
                    r.device_info.model_name == instance.text
                    and CURRENT_ROKU.device_info.model_name != instance.text
                ):
                    print("Not current Roku")
                    try:
                        CURRENT_ROKU = r
                        print("Setting current roku: ", r)

                        self.cbox.scroll.gridlay.add_gridlay_buttons()
                        break
                    except ConnectionError as e:
                        break


class Combined(BoxLayout):
    def __init__(self, main_app):
        super().__init__()
        self.orientation = "vertical"
        self.cbox = ContainerBox(main_app)
        self.hbox = Header(self.cbox)
        self.add_widget(self.hbox)
        self.add_widget(self.cbox)


class MainApp(App):
    def build(self):
        Window.size = (1360, 768)
        return Combined(self)


def main():
    def get_rokus():
        global ROKUS
        ROKUS = Roku.discover(timeout=5)
        call_event("set_header_buttons")
        call_event("add_gridlay_buttons")

    t = threading.Thread(target=get_rokus)
    t.start()
    MainApp().run()
    t.join()


if __name__ == "__main__":
    main()
