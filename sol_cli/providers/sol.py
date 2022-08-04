from base_parser import BaseParser
from typing import List, Dict

class sol(BaseParser):
    name : str = "sol"
    host_url: str = "https://solarmovie.pe"
    servers : dict = {
            "UpCloud": None,
            "Vidcloud": None,
            "Streamlare": None,
            "MixDrop": None,
            "Hydrax": None
            }
    def load_episodes(self,show_link: str) -> List[Episode]:
        pass

    def load_video_servers(episode_link) -> List[VideoServer]:
        pass

    def get_vide_extractor(self,server: VideoServer) -> VideoExtractor:
        if "mzzcloud" in server.embed:
            pass
        elif "rabbitstream" in server.embed:
            pass
        else:
            return None

