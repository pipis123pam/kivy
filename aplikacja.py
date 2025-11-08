from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from datetime import datetime, timedelta

class WeatherRoot(BoxLayout):
    pass

class WeatherApp(MDApp):
    BASE_URL = "https://adrian-gathering-twenty-donald.trycloudflare.com/weather"

    def build(self):
        return WeatherRoot()

    def on_start(self):
        Clock.schedule_once(self.load_all_days, 1)

    def load_all_days(self, *args):
        dni_tygodnia = ["Poniedziałek", "Wtorek", "Środa", "Czwartek",
                        "Piątek", "Sobota", "Niedziela"]

        endpointy = [
            "weather",
            "weatherdaytwo",
            "weatherdaythree",
            "weatherdayfour",
            "weatherdayfive",
            "weatherdaysix",
            "weatherdayseven"
        ]

        for i in range(7):
            data_dnia = datetime.now() + timedelta(days=i)
            nazwa_dnia = dni_tygodnia[data_dnia.weekday()]
            data_txt = data_dnia.strftime("%d.%m")

            status_label = f"status_label_day{i+1}"
            if status_label in self.root.ids:
                self.root.ids[status_label].text = f"{nazwa_dnia} ({data_txt})"

            url = f"{self.BASE_URL}/{endpointy[i]}"
            UrlRequest(url, on_success=lambda req, res, d=i: self.update_day_data(res, d))

    def update_day_data(self, data, day_index):
        ids = self.root.ids

        hours = data.get("hour", [])
        temps = data.get("temperature", [])
        showers = data.get("shower", [])
        winds = data.get("wind", [])

        if not (hours and temps and showers and winds):
            ids[f"status_label_day{day_index+1}"].text += "..."
            return

        godzina = str(hours[0])
        temperatura = f"{temps[0]} °C"
        opady = f"{showers[0]} mm"
        wiatr = f"{winds[0]} km/h"

        ids[f"hour_value_day{day_index+1}"].text = f"Godzina: {godzina}"
        ids[f"temperature_value_day{day_index+1}"].text = f"Temperatura: {temperatura}"
        ids[f"rain_value_day{day_index+1}"].text = f"Opady: {opady}"
        ids[f"wind_value_day{day_index+1}"].text = f"Wiatr: {wiatr}"
        ids[f"status_label_day{day_index+1}"].text += " Prognoza:"

    def reload(self):
        for i in range(7):
            self.root.ids[f"status_label_day{i+1}"].text = "..."
        self.load_all_days()

if __name__ == '__main__':
    WeatherApp().run()
