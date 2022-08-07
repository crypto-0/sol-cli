from base_parser import BaseParser, Episode, Season
from typing import List, Dict
import requests
import lxml.html
from extractors.video_extractor import *
from extractors.upcloud import *
from extractors.vidcloud import *


class sol(BaseParser):
    name : str = "sol"
    host_url: str = "https://solarmovie.pe"
    server_extracters : dict = {
            "UpCloud": UpCloud,
            "Vidcloud": Vidcloud
            #"Streamlare": None,
            #"MixDrop": None,
            #"Hydrax": None
            }
    headers =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }

    def load_seasons(self,show_link: str) -> List[Season]:
        season_url: str = "https://solarmovie.pe/ajax/v2/tv/seasons/" + show_link
        r: requests.Response = requests.get(season_url,headers=self.headers)
        html_doc: lxml.html.HtmlElement= lxml.html.fromstring(r.text)
        season_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".dropdown-item")
        seasons: List[Season] =[]
        for season_element in season_elements:
            season_number: str = season_element.text.split()[-1]
            season_id: str = season_element.get("data-id")
            seasons.append(Season(season_number,season_id))
        return seasons

    def load_episodes(self,show_link: str) -> List[Episode]:
        episodes_url: str = "https://solarmovie.pe/ajax/v2/season/episodes/"
        r = requests.get(episodes_url + show_link,headers=self.headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        episode_elements:List[lxml.html.HtmlElement] = html_doc.cssselect("a")
        episodes : List[Episode] = []
        for episode_element in episode_elements:
            episode_number: str = episode_element.get("title").split(":")[0].split()[-1]
            episode_id = episode_element.get("data-id")
            episode_title = episode_element.get("title")
            episodes.append(Episode(episode_number,episode_id,episode_title))
        return episodes


    def load_video_servers(self,episode_link: str) -> List[VideoServer]:
        episodes_server_url : str = "https://solarmovie.pe/ajax/v2/episode/servers/"
        server_embed_url: str = "https://solarmovie.pe/ajax/get_link/"
        r : requests.Response = requests.get(episodes_server_url + episode_link,headers=self.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".nav-item a")
        servers: List[VideoServer] = [] 
        for server_element in server_elements:
            server_id: str = server_element.get("data-id")
            server_title: str = server_element.get("title")
            r: requests.Response = requests.get(server_embed_url + server_id,headers=self.headers)
            embed: str = r.json()["link"]
            servers.append(VideoServer(server_title,embed))
        return servers


    def get_vide_extractor(self,server: VideoServer) -> VideoExtractor:
        return self.server_extracters[server.name]

