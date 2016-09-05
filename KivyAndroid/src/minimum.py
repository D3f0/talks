from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.modules import inspector

class DemoApp(App):
    def build(self):
        label = Label(text="Hola Kivy", id="id_x1")
        inspector.create_inspector(Window, label)
        return label

if __name__ == '__main__':
    DemoApp().run()
