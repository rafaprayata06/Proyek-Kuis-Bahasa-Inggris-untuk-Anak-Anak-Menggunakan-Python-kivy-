from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

Builder.load_file("screens/quiz_screen.kv")


class QuizScreen(Screen):
    def on_enter(self):
        self.backsound = SoundLoader.load("tegang.wav")
        if self.backsound:
            self.backsound.loop = True
            self.backsound.play()

        if not self.manager.logic.soal_acak:
            self.manager.logic.shuffle_questions()
            self.manager.logic.index = 0
            self.manager.logic.skor = 0

        self.tampilkan_soal()

    def tampilkan_soal(self):
        try:
            soal = self.manager.logic.get_current_question()
        except IndexError:
            self.show_popup("Soal Habis", "Tidak ada soal yang tersedia.")
            return

        self.ids.pertanyaan.text = soal["deskripsi"]
        for i, pilihan in enumerate(soal["pilihan"]):
            btn = self.ids[f"btn{i}"]
            btn.text = pilihan
            btn.background_color = (0.75, 0.85, 1, 1)
            btn.color = (0, 0, 0, 1)

    def jawab(self, pilihan):
        hasil = self.manager.logic.cek_jawaban(pilihan)
        jawaban_benar = self.manager.logic.get_current_question()["jawaban"]

        # Highlight semua tombol
        for i in range(4):
            btn = self.ids[f"btn{i}"]
            if btn.text == jawaban_benar:
                btn.background_color = (0.3, 0.8, 0.3, 1)  # Hijau terang
                btn.color = (1, 1, 1, 1)
            elif btn.text == pilihan:
                if not hasil:
                    btn.background_color = (1, 0.2, 0.2, 1)  # Merah terang
                    btn.color = (1, 1, 1, 1)

        # Mainkan efek suara
        if hasil:
            sound = SoundLoader.load("benar.wav")
        else:
            sound = SoundLoader.load("salah.wav")
        if sound:
            sound.play()

        # Jika selesai atau salah => tampilkan popup statistik
        if not hasil or self.manager.logic.selesai:
            if hasattr(self, 'backsound') and self.backsound:
                self.backsound.stop()

            self.manager.logic.update_high_score()
            Clock.schedule_once(lambda dt: tampilkan_popup_statistik(
                total=self.manager.logic.total_dijawab,
                skor=self.manager.logic.skor,
                skor_tertinggi=self.manager.logic.skor_tertinggi,
                manager=self.manager
            ), 1)
        else:
            Clock.schedule_once(lambda dt: self.next_soal(), 0.9)

    def next_soal(self):
        self.manager.logic.index += 1
        self.tampilkan_soal()

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()


def tampilkan_popup_statistik(total, skor, skor_tertinggi, manager):
    layout = BoxLayout(
        orientation='vertical',
        spacing=dp(10),
        padding=dp(16),
        size_hint=(None, None)
    )
    layout.size = (dp(320), dp(260))

    layout.canvas.before.clear()
    with layout.canvas.before:
        Color(1, 1, 1, 1)
        layout.bg_rect = RoundedRectangle(pos=layout.pos, size=layout.size, radius=[15])
    layout.bind(pos=lambda *x: setattr(layout.bg_rect, 'pos', layout.pos))
    layout.bind(size=lambda *x: setattr(layout.bg_rect, 'size', layout.size))

    layout.add_widget(Label(
        text='[b]Statistik Kuis[/b]',
        markup=True,
        font_size='18sp',
        halign='center',
        color=[0, 0, 0, 1],
        size_hint_y=None,
        height=dp(28)
    ))

    for text in [
        f"total dijawab   : {total}",
        f"skor terakhir   : {skor}",
        f"skor tertinggi  : {skor_tertinggi}"
    ]:
        layout.add_widget(Label(
            text=text,
            font_size='15sp',
            color=[0, 0, 0, 1],
            size_hint_y=None,
            height=dp(24)
        ))

    tombol_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10), padding=(0, dp(10), 0, 0))

    btn_kembali = Button(
        text='kembali',
        background_color=[0.7, 0.2, 0.2, 1],
        color=[1, 1, 1, 1],
        bold=True,
       on_release=lambda x: popup.dismiss() or reset_to_home(manager)
    )

    btn_mainlagi = Button(
        text='main lagi',
        background_color=[0.1, 0.6, 0.1, 1],
        color=[1, 1, 1, 1],
        bold=True,
        on_release=lambda x: popup.dismiss() or restart_quiz(manager)
    )

    tombol_box.add_widget(btn_kembali)
    tombol_box.add_widget(btn_mainlagi)
    layout.add_widget(tombol_box)

    popup = Popup(
        title='',
        content=layout,
        size_hint=(None, None),
        size=layout.size,
        auto_dismiss=False,
        background_color=(0, 0, 0, 0),
        background='',
        separator_height=0
    )
    popup.open()

def reset_to_home(manager):
        logic = manager.logic
        logic.index = 0
        logic.skor = 0
        logic.total_dijawab = 0
        logic.soal_acak = []  # reset juga soal yang lama
        manager.current = 'home'


def restart_quiz(manager):
    screen = manager.get_screen('quiz')
    screen.manager.logic.shuffle_questions()
    screen.manager.logic.index = 0
    screen.manager.logic.skor = 0
    screen.on_enter()
