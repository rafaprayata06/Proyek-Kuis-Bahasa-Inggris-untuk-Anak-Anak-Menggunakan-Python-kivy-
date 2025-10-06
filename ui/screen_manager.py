from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.quiz_screen import QuizScreen
from screens.result_screen import ResultScreen
from logic.quiz_logic import QuizLogic  # ⬅ Tambahkan ini

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = QuizLogic()  # ⬅ Tambahkan ini

        self.add_widget(HomeScreen(name="home"))
        self.add_widget(QuizScreen(name="quiz"))
        self.add_widget(ResultScreen(name="result"))
