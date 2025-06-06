from abc import ABC, abstractmethod
from ..value_objects.search_result import SearchResult
from ..value_objects.music_track import MusicTrack
from ..value_objects.video import Video

class BrowserPort(ABC):
    @abstractmethod
    def search_google(self, query: str) -> SearchResult:
        """Search in Google"""
        pass

    @abstractmethod
    def search_youtube(self, query: str) -> Video:
        """Search video in YouTube"""
        pass
    
    @abstractmethod
    def search_amazon_music(self, query: str) -> MusicTrack:
        """Search track in Amazon Music"""
        pass

    @abstractmethod
    def open_url(self, url: str) -> None:
        """Open URL in browser"""
        pass