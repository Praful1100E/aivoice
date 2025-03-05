import wikipedia
import webbrowser

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