from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        # Tambahkan background
        self.background = Image(
            source='images/background.png',
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.background)  # Tambahkan background terlebih dahulu

        # Tambahkan tombol di atas background
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        start_button = Button(
            text='Start Game',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='20sp'
        )
        start_button.bind(on_release=self.start_game)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'game'
