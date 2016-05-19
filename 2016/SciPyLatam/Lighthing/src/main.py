from kivy.app import App
from kivy.uix.widget import Widget

class Ventana(Widget):
    pass

class DemoApp(App):
    def build(self):
        return Ventana()

if __name__ == '__main__':
    DemoApp().run()
