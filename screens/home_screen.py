from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation

Builder.load_file("screens/home_screen.kv")

class HomeScreen(Screen):
    def on_enter(self):
        # Mainkan musik home
        self.home_music = SoundLoader.load("quiz.wav")
        if self.home_music:
            self.home_music.loop = True
            self.home_music.play()

    def mulai_quiz(self):
        # Hentikan musik home
        if hasattr(self, 'home_music') and self.home_music:
            self.home_music.stop()

        # Atur dan tampilkan countdown
        self.count = 3
        self.ids.countdown_label.text = str(self.count)
        self.ids.countdown_label.opacity = 1
        self.anim_count(self.count)

        # Mainkan suara countdown
        self.countdown_sound = SoundLoader.load("countdown.wav")
        if self.countdown_sound:
            self.countdown_sound.play()

        # Simpan event supaya bisa dibatalkan nanti jika perlu
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)

    def anim_count(self, value):
        self.ids.countdown_label.text = str(value)
        anim = Animation(font_size=80, duration=0.3) + Animation(font_size=64, duration=0.3)
        anim.start(self.ids.countdown_label)


    def update_countdown(self, dt):
        self.count -= 1
        if self.count > 0:
            self.anim_count(self.count)
        else:
            self.ids.countdown_label.opacity = 0
            Clock.unschedule(self.countdown_event)
            self.manager.current = 'quiz'
