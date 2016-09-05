from kivy.app import App
from kivy.uix.widget import Widget

class MiWidget(Widget):
    pass

class DemoApp(App):
    def build(self):
        return MiWidget()

    def saludar(self):
        print("Prueba")

if __name__ == '__main__':
    DemoApp().run()
