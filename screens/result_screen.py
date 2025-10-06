from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_file("screens/result_screen.kv")

class ResultScreen(Screen):
    def on_enter(self):
        logic = self.manager.logic

        self.ids.label_skor.text = f"Skor Terakhir: {logic.skor}"
        self.ids.label_terjawab.text = f"Soal Dijawab: {logic.total_dijawab}"
        self.ids.label_highscore.text = f"Skor Tertinggi: {logic.skor_tertinggi}"

        # Tambahan: tampilkan popup jika menjawab 15 soal dengan benar
        if logic.skor == 15:
            popup = Popup(
                title='Selamat!',
                content=Label(
                    text='Kamu berhasil menjawab semua soal dengan benar!\nLuar biasa!',
                    halign='center',
                    valign='middle'
                ),
                size_hint=(0.8, 0.4)
            )
            popup.open()
