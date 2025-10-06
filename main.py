from kivy.app import App
from ui.screen_manager import ScreenManagement


class QuizApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == "__main__":
    QuizApp().run()
