import sys
print sys.executable

from kivy.app import App
from kivy.uix.widget import Widget

class MyWidget(Widget):
    pass

class DemoApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    DemoApp().run()
