from kivy.core.window import Window

from kivy.app import App
from kivy.uix.label import Label

class DemoApp(App):
    def build(self):
        return Label(text="Hola Kivy!")

if __name__ == '__main__':
    DemoApp().run()
