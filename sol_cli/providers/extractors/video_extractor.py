from abc import ABC, abstractmethod
from typing import List

class VideoServer:
    def __init__(self,name: str,embed: str) -> None:
        self.name = name
        self.embed = embed

class Video:
    def __init__(self,quality,is_m3u8,url) -> None:
        self.quality = quality
        self.is_m3u8 = is_m3u8
        self.url = url

class Subtitle:
    subtitle_type: str = "vtt"
    def __init__(self,language: str,url: str) -> None:
        self.language = language
        self.url = url
        

class VideoContainer:

    def __init__(self,videos,subtitles) -> None:
        self.videos = videos
        self.subtitles = subtitles

class VideoExtractor(ABC):
    def __init__(self,server: VideoServer) -> None:
        self.server: VideoServer = server
        self.videos: List[Video]
        self.subtitles: List[Subtitle]

    @abstractmethod
    def extract(self) -> VideoContainer:
        pass

