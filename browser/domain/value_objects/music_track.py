from dataclasses import dataclass

@dataclass(frozen=True)
class MusicTrack:
    title: str
    artist: str
    url: str