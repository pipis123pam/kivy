from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
import json

BASE_URL = "https://adrian-gathering-twenty-donald.trycloudflare.com/weather"


DAYS_ENDPOINTS = [
    "weather",
    "weatherdaytwo",
    "weatherdaythree",
    "weatherdayfour",
    "weatherdayfive",
    "weatherdaysix",
    "weatherdayseven"
]

class WeatherRoot(BoxLayout):
    pass

class WeatherApp(MDApp):
    def build(self):
        return WeatherRoot()

    def on_start(self):
        
        Clock.schedule_once(lambda dt: self.fetch_all_days(), 1)

    def fetch_all_days(self):
        for day_index, endpoint in enumerate(DAYS_ENDPOINTS, start=1):
            url = f"{BASE_URL}/{endpoint}"
            print(f"⏳ Pobieranie danych dla dnia {day_index} z {url}")
            UrlRequest(url, on_success=lambda req, res, di=day_index: self.on_success(req, res, di),
                       on_error=lambda req, err, di=day_index: self.on_error(req, err, di),
                       on_failure=lambda req, res, di=day_index: self.on_failure(req, res, di))

    def on_success(self, request, result, day_index):
        print(f"✅ Odebrano dane dla dnia {day_index}")
        try:
            
            if isinstance(result, str):
                result = json.loads(result)

            hours = result.get("hour", [])
            temps = result.get("temperature", [])
            showers = result.get("shower", [])
            winds = result.get("wind", [])

            if not hours or not temps:
                self.root.ids[f"status_label_day{day_index}"].text = "Brak danych"
                return

            
            hour = hours[0]
            temp = temps[0]
            rain = showers[0] if showers else 0
            wind = winds[0] if winds else 0

            
            ids = self.root.ids
            ids[f"hour_value_day{day_index}"].text = f"{hour} h"
            ids[f"temperature_value_day{day_index}"].text = f"{temp} °C"
            ids[f"rain_value_day{day_index}"].text = f"{rain} mm"
            ids[f"wind_value_day{day_index}"].text = f"{wind} km/h"
            ids[f"status_label_day{day_index}"].text = f"Dane dnia {day_index} OK"

        except Exception as e:
            print(f"❌ Błąd w on_success dla dnia {day_index}: {e}")
            self.root.ids[f"status_label_day{day_index}"].text = f"Błąd: {e}"

    def on_error(self, request, error, day_index):
        print(f"❌ Błąd sieci dla dnia {day_index}: {error}")
        self.root.ids[f"status_label_day{day_index}"].text = "Błąd sieci"

    def on_failure(self, request, result, day_index):
        print(f"❌ Niepowodzenie dnia {day_index}: {result}")
        self.root.ids[f"status_label_day{day_index}"].text = "Niepowodzenie zapytania"

    def reload(self):
        for i in range(1, 8):
            self.root.ids[f"status_label_day{i}"].text = "Odświeżanie..."
        self.fetch_all_days()


if __name__ == '__main__':
    WeatherApp().run()

