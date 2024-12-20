class GameOverScreen(Screen):
#     def __init__(self, **kwargs):
#         super(GameOverScreen, self).__init__(**kwargs)
#         layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
#         label = Label(text="GAME OVER", font_size='40sp', color=(1, 0, 0, 1))
#         layout.add_widget(label)

#         restart_button = Button(text="Restart", size_hint=(0.3, 0.1))
#         restart_button.bind(on_release=self.restart_game)
#         layout.add_widget(restart_button)

#         self.add_widget(layout)

#     def restart_game(self, instance):
#         self.manager.current = 'game'
#         game_screen = self.manager.get_screen('game')
#         game_screen.reset_game()