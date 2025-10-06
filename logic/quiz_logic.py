# logic/quiz_logic.py
import json
import random
import os

class QuizLogic:
    def __init__(self):
        with open("data/soal.json", "r", encoding="utf-8") as f:
            self.soal_data = json.load(f)
            self.soal_acak = []
            self.index = 0
            self.skor = 0
            self.selesai = False
            self.total_dijawab = 0
            self.skor_tertinggi = self.load_high_score()

    def shuffle_questions(self):
        self.soal_acak = random.sample(self.soal_data, len(self.soal_data))  # ambil semua soal
        self.index = 0
        self.skor = 0
        self.total_dijawab = 0
        self.selesai = False

    def get_current_question(self):
        if self.index < len(self.soal_acak):
            return self.soal_acak[self.index]
        else:
            self.selesai = True
            return None
    def cek_jawaban(self, jawaban):
        if self.selesai:
            return False

        soal = self.get_current_question()
        if soal is None:
            return False

        self.total_dijawab += 1

        if soal["jawaban"] == jawaban:
            self.skor += 1
            self.index += 1
            return True
        else:
            self.selesai = True
            self.update_high_score()
            return False



    def load_high_score(self):
        if os.path.exists("data/score.json"):
            with open("data/score.json", "r") as f:
                return json.load(f).get("high_score", 0)
        return 0

    def update_high_score(self):
        if self.skor > self.skor_tertinggi:
            self.skor_tertinggi = self.skor
            with open("data/score.json", "w") as f:
                json.dump({"high_score": self.skor}, f)

    def is_finished(self):
     return self.selesai
