from abc import ABC, abstractmethod
from typing import List
from extractors.video_extractor import *
from urllib.parse import urlparse


class Episode:
    def __init__(self,season: str,number: str,link: str,title: str) -> None:
        self.season: str = season
        self.number: str = number
        self.link: str = link
        self.title: str =title

class BaseParser(ABC):

    @abstractmethod
    def load_episodes(self,show_link: str) -> List[Episode]:
        pass

    @abstractmethod
    def load_video_servers(episode_link) -> List[VideoServer]:
        pass

    @abstractmethod
    def get_vide_extractor(self,server: VideoServer) -> VideoExtractor:
        pass

