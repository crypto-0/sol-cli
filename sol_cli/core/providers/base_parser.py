from abc import ABC, abstractmethod
from typing import List
from .extractors.video_extractor import VideoExtractor,VideoServer


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
    def __init__(self,title: str,link: str,is_tv: bool,info: str) -> None:
        self.title: str = title
        self.link: str = link
        self.is_tv: bool = is_tv
        self.info: str = info

class BaseParser(ABC):
    max_search_result: int = 10

    @abstractmethod
    def load_seasons(self,show_link: str) -> List[Season]:
        pass

    @abstractmethod
    def load_episodes(self,show_link: str) -> List[Episode]:
        pass

    @abstractmethod
    def load_movie_servers(self,show_link: str) -> List[VideoServer]:
        pass
    @abstractmethod
    def load_episode_servers(self,episode_link: str) -> List[VideoServer]:
        pass

    @abstractmethod
    def get_video_extractor(self,server: VideoServer) -> VideoExtractor:
        pass

    @abstractmethod
    def search(self,query: str) -> List[ShowResponse]:
        pass
    @abstractmethod
    def get_title_and_release_year(self,show_link: str) -> tuple:
        pass
