from abc import ABC, abstractmethod
from typing import List
from extractors.video_extractor import *
from urllib.parse import urlparse



class Episode:
    def __init__(self,episode_number: str,link: str,title: str) -> None:
        self.episode_number: str = episode_number
        self.link: str = link
        self.title: str =title

class Season:
    def __init__(self,season_number: str,link: str) -> None:
        self.season_number: str = season_number
        self.link: str = link
class ShowResponse:
    def __init__(self) -> None:
        title: str
        link: str
        cover_url: str

class BaseParser(ABC):

    @abstractmethod
    def load_seasons(self,show_link: str) -> List[Season]:
        pass

    @abstractmethod
    def load_episodes(self,show_link: str) -> List[Episode]:
        pass

    @abstractmethod
    def load_video_servers(self,episode_link: str) -> List[VideoServer]:
        pass

    @abstractmethod
    def get_vide_extractor(self,server: VideoServer) -> VideoExtractor:
        pass

    @abstractmethod
    def search(self,title: str) -> List[ShowResponse]:
        pass
