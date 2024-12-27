from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

class HelloScreen(Screen):
    pass

class NextScreen(Screen):
    pass

class ThirdScreen(Screen):
    pass
class Playlist(Screen):
    pass

class MusicApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(HelloScreen(name="hello"))
        sm.add_widget(NextScreen(name="next"))
        sm.add_widget(ThirdScreen(name="third"))
        sm.add_widget(Playlist(name="four"))

        return sm

if __name__ == "__main__":
    MusicApp().run()