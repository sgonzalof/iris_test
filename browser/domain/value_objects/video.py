from dataclasses import dataclass

@dataclass
class Video:
    id: str
    title: str
    url: str

    @classmethod
    def create(cls, video_id: str, title: str) -> 'Video':
        return cls(
            id=video_id,
            title=title,
            url=f"https://www.youtube.com/watch?v={video_id}"
        )