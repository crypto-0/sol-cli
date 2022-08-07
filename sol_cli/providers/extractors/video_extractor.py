from abc import ABC, abstractmethod
from typing import List

class VideoServer:
    def __init__(self,name: str,embed: str) -> None:
        self.name: str = name
        self.embed: str = embed

class Video:
    def __init__(self,quality: str,is_m3u8: bool,url: str) -> None:
        self.quality: str = quality
        self.is_m3u8: bool = is_m3u8
        self.url: str = url

class Subtitle:
    subtitle_type: str = "vtt"
    def __init__(self,language: str,url: str) -> None:
        self.language: str = language
        self.url: str = url
        

class VideoContainer:

    def __init__(self,videos: List[Video],subtitles: List[Subtitle]) -> None:
        self.videos: List[Video] = videos
        self.subtitles: List[Subtitle] = subtitles

class VideoExtractor(ABC):
    def __init__(self,server: VideoServer) -> None:
        self.server: VideoServer = server
        self.videos: List[Video] = []
        self.subtitles: List[Subtitle] = []

    @abstractmethod
    def extract(self) -> VideoContainer:
        pass

