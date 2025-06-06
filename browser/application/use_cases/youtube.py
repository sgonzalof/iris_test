from dataclasses import dataclass
from ...domain.ports.browser_port import BrowserPort

@dataclass
class YouTubeSearchRequest:
    query: str

class YouTubeSearchUseCase:
    def __init__(self, browser: BrowserPort):
        self._browser = browser
    
    def execute(self, request: YouTubeSearchRequest) -> str:
        try:
            video = self._browser.search_youtube(request.query)
            self._browser.open_url(video.url)
            return f"Reproduciendo {video.title} en YouTube"
        except Exception as e:
            return f"Lo siento, no pude reproducir el video: {str(e)}"