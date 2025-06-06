from dataclasses import dataclass
from ...domain.ports.browser_port import BrowserPort

@dataclass
class GoogleSearchRequest:
    query: str
    description: str = "Búsqueda en Google"




class GoogleSearchUseCase:
    def __init__(self, browser: BrowserPort):
        self._browser = browser
    
    def execute(self, request: GoogleSearchRequest) -> str:
        try:
            result = self._browser.search_google(request.query)
            self._browser.open_url(result.url)
            return f"He encontrado esto: {result.description}"
        except Exception as e:
            return f"Lo siento, no pude realizar la búsqueda: {str(e)}"