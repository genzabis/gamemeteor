from kivy.core.audio import SoundLoader

# Memuat dan memainkan background music
bg_music = SoundLoader.load('sounds/sound1.wav')
if bg_music:
    bg_music.loop = True  # Mengulang musik
    bg_music.play()

# Memainkan efek suara tembakan
shoot_sound = SoundLoader.load('sounds/shoot.wav')
if shoot_sound:
    shoot_sound.play()

# Memainkan efek suara tabrakan
crash_sound = SoundLoader.load('sounds/crash.wav')
if crash_sound:
    crash_sound.play()
