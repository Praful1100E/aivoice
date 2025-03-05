import wikipedia
import requests
import webbrowser
from config import OPENWEATHER_API_KEY

class WebServices:
    def search_wikipedia(self, query):
        try:
            results = wikipedia.summary(query.strip(), sentences=2)
            return results
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found: {', '.join(e.options[:3])}"
        except wikipedia.exceptions.PageError:
            return "No Wikipedia page found."
        except Exception as e:
            return f"Wikipedia error: {str(e)}"

    def get_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url).json()
            
            if response.get("main"):
                temperature = response["main"]["temp"]
                return f"The temperature in {city} is {temperature} degrees Celsius."
            return "City not found."
        except requests.RequestException as e:
            return f"Weather API error: {str(e)}"

    def open_website(self, site):
        try:
            if site == "youtube":
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube"
            elif site == "google":
                webbrowser.open("https://www.google.com")
                return "Opening Google"
            return "Website not supported"
        except Exception as e:
            return f"Browser error: {str(e)}"
