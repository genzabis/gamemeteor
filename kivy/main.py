import pygame
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button 
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from random import randint

# Initialize Pygame Mixer for audio
pygame.mixer.init()

# Set screen size
Window.size = (800, 600)

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        # Start background music when game starts
        pygame.mixer.music.load('sounds/bgsound.mp3')
        pygame.mixer.music.play(-1, 0.0)

        with self.canvas.before:
            self.background = Rectangle(
                source='images/bg9.jpg',
                size=Window.size,
                pos=(0, 0)
            )

        layout = FloatLayout()

        self.start_button = Button(
            size_hint=(None, None),
            size=(500, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_normal='images/start3.png',
            background_down='images/start3.png'
        )
        self.start_button.bind(on_release=self.start_game)
        layout.add_widget(self.start_button)
        self.add_widget(layout)

        Window.bind(size=self._update_background)

    def _update_background(self, instance, value):
        self.background.size = Window.size

    def start_game(self, instance):
        game_screen = self.manager.get_screen('game')
        game_screen.reset_game()
        self.manager.current = 'game'

class SpaceShooterGame(Screen):
    def __init__(self, **kwargs):
        super(SpaceShooterGame, self).__init__(**kwargs)
        self.game_over = False
        self.score = 0
        self.bullets = []
        self.asteroids = []
        self.update_event = None
        self._setup_game()

        Window.bind(size=self._update_background)

    def _update_background(self, instance, value):
        self.background.size = Window.size

    def _setup_game(self):
        self.canvas.clear()
        self.ship = None
        self.spawn_background()
        self.spawn_ship()
        self.spawn_score_label()
        self.spawn_asteroids()

    def reset_game(self):
        if self.update_event:
            self.update_event.cancel()
        
        self.game_over = False
        self.score = 0
        self.bullets = []
        self.asteroids = []
        self._setup_game()
        self.score_label.text = f"Score: {self.score}"
        
        self.update_event = Clock.schedule_interval(self.update, 1/60.0)

    def spawn_background(self):
        with self.canvas.before:
            self.background = Rectangle(
                source='images/bg9.jpg',
                size=Window.size,
                pos=(0, 0)
            )

    def spawn_score_label(self):
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size='20sp',
            color=(1, 1, 1, 1),
            pos=(10, Window.height - 40),
            size_hint=(None, None)
        )
        self.add_widget(self.score_label)

    def spawn_ship(self):
        with self.canvas:
            self.ship = Rectangle(
                source='images/ship.png',
                size=(220, 220),
                pos=(Window.width / 2 - 40, 50)
            )

    def spawn_asteroids(self):
        with self.canvas:
            for _ in range(5):
                x = randint(0, Window.width - 60)
                y = randint(Window.height // 2, Window.height - 60)
                asteroid = Rectangle(
                    source='images/asteroid.png',
                    size=(100, 100),
                    pos=(x, y)
                )
                self.asteroids.append(asteroid)

    def check_collision(self, obj1, obj2):
        margin = 10
        return (
            obj1.pos[0] + margin < obj2.pos[0] + obj2.size[0] - margin and
            obj1.pos[0] + obj1.size[0] - margin > obj2.pos[0] + margin and
            obj1.pos[1] + margin < obj2.pos[1] + obj2.size[1] - margin and
            obj1.pos[1] + obj1.size[1] - margin > obj2.pos[1] + margin
        )

    def on_touch_move(self, touch):
        if not self.game_over:
            new_x = min(max(touch.x - self.ship.size[0] / 2, 0), 
                       Window.width - self.ship.size[0])
            self.ship.pos = (new_x, self.ship.pos[1])

    def on_touch_down(self, touch):
        if not self.game_over:
            self.spawn_bullet()

    def spawn_bullet(self):
        with self.canvas:
            bullet = Rectangle(
                source='images/bullet2.png',
                size=(70, 70),
                pos=(self.ship.pos[0] + self.ship.size[0] / 2 - 10,
                     self.ship.pos[1] + self.ship.size[1])
            )
            self.bullets.append(bullet)
            self.play_shoot_sound()

    def update(self, dt):
        if self.game_over:
            return False

        for bullet in self.bullets[:]:
            bullet.pos = (bullet.pos[0], bullet.pos[1] + 10)
            if bullet.pos[1] > Window.height:
                self.bullets.remove(bullet)
                self.canvas.remove(bullet)

        for asteroid in self.asteroids[:]:
            asteroid.pos = (asteroid.pos[0], asteroid.pos[1] - 2)
            if asteroid.pos[1] < 0:
                asteroid.pos = (randint(0, Window.width - 60), Window.height)

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if self.check_collision(bullet, asteroid):
                    if asteroid in self.asteroids:
                        self.asteroids.remove(asteroid)
                        self.canvas.remove(asteroid)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                        self.canvas.remove(bullet)
                    self.score += 50
                    self.score_label.text = f"Score: {self.score}"
                    with self.canvas:
                        new_asteroid = Rectangle(
                            source='images/asteroid.png',
                            size=(100, 100),
                            pos=(randint(0, Window.width - 60), Window.height)
                        )
                        self.asteroids.append(new_asteroid)

        for asteroid in self.asteroids[:]:
            if self.check_collision(self.ship, asteroid):
                self.end_game()
                return False

        return True

    def play_shoot_sound(self):
        shoot_sound = pygame.mixer.Sound('sounds/tembakan.mp3')
        shoot_sound.play()

    def end_game(self):
        self.game_over = True
        if self.update_event:
            self.update_event.cancel()
        self.manager.get_screen('game_over').final_score = self.score
        self.manager.current = 'game_over'

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.final_score = 0

        with self.canvas.before:
            self.background = Rectangle(
                source='images/bg9.jpg',
                size=Window.size,
                pos=(0, 0)
            )

        layout = FloatLayout()

        game_over_label = Image(
            source='images/game_over3.png',
            size_hint=(None, None),
            size=(400, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(game_over_label)

        # Add score label
        self.score_label = Label(
            text=f"Score: 0",
            font_size='36sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        layout.add_widget(self.score_label)

        self.restart_button = Button(
            background_normal='images/restart3.png',
            background_down='images/restart3.png',
            size_hint=(None, None),
            size=(400, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        self.restart_button.bind(on_release=self.restart_game)
        layout.add_widget(self.restart_button)

        self.add_widget(layout)

        Window.bind(size=self._update_background)

    def _update_background(self, instance, value):
        self.background.size = Window.size

    def on_pre_enter(self):
        # Update score when entering the screen
        self.score_label.text = f"Score: {self.final_score}"

    def restart_game(self, instance):
        game_screen = self.manager.get_screen('game')
        game_screen.reset_game()
        self.manager.current = 'game'

class SpaceShooterApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(SpaceShooterGame(name='game'))
        sm.add_widget(GameOverScreen(name='game_over'))
        sm.current = 'start'
        return sm

if __name__ == '__main__':
    SpaceShooterApp().run()