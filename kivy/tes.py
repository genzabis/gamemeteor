from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class TestApp(App):
    def build(self):
        layout = BoxLayout()
        background = Image(source='images/background.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)
        return layout

if __name__ == '__main__':
    TestApp().run()
