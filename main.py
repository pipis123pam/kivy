import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class Fa:
    def print(self):
        url = "https://tied-product-nil-beyond.trycloudflare.com/weather/weather"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Błąd podczas pobierania danych: {e}")
            return {"hour": [], "temperature": [], "wind": [], "shower": []}


class WeatherScreen(BoxLayout):
    
    def get_data(self):
        fa = Fa()
        data = fa.print()
        
        hours = data["hour"]
        temps = data["temperature"]
        winds = data["wind"]
        shower = data["shower"]

        items = []
        for h, t, w, s in zip(hours, temps, winds, shower):
            items.append({"hour": h, "temp": str(t), "wind": str(w), "shower": str(s)})

        if 'rv' in self.ids:
            self.ids.rv.data = items
        else:
            print("Błąd: RecycleView o ID 'rv' nie jest dostępne.")
class WeatherItem(BoxLayout):
      hour = StringProperty('')
      temp = StringProperty('')
      wind = StringProperty('')
      shower = StringProperty('')

class WeatherApp(App):
    def build(self):
        Builder.load_file("weather.kv")
        self.root_widget = WeatherScreen()
        return self.root_widget
    def on_start(self):
        if self.root_widget:
            self.root_widget.get_data()
if __name__ == "__main__":
    WeatherApp().run()
    
