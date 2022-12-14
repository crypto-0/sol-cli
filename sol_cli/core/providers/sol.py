from .base_parser import BaseParser, Episode, Season, ShowResponse
from typing import List, Dict,Optional
import requests
import lxml.html
from .extractors.video_extractor import *
from .extractors.upcloud import *
from .extractors.vidcloud import *


class Sol(BaseParser):
    name : str = "sol"
    host_url: str = "https://solarmovie.pe"
    headers =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }

    def load_movie_servers(self,show_link: str) -> list[VideoServer]:
        movie_server_url : str = "https://solarmovie.pe/ajax/movie/episodes/"
        server_embed_url: str = "https://solarmovie.pe/ajax/get_link/"
        r : requests.Response = requests.get(movie_server_url + show_link,headers=self.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".nav-item a")
        servers: List[VideoServer] = [] 
        for server_element in server_elements:
            server_id: str = server_element.get("data-linkid")
            server_title: str = server_element.get("title")
            r: requests.Response = requests.get(server_embed_url + server_id,headers=self.headers)
            embed: str = r.json()["link"]
            servers.append(VideoServer(server_title,embed))
        return servers

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


    def load_episode_servers(self,episode_link: str) -> List[VideoServer]:
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


    def get_video_extractor(self,server: VideoServer) -> Optional[VideoExtractor]:
        if server.name == "Server UpCloud" or server.name == "UpCloud":
            return UpCloud(server)
        elif server.name == "Server Vidcloud" or server.name == "Vidcloud":
            return Vidcloud(server)
        else:
            return None
    def get_title_and_release_year(self,show_link: str) -> tuple:
        r = requests.get(show_link,headers=self.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        element: lxml.html.HtmlElement = html_doc.cssselect(".row-line")[0]
        release = element.text_content().split("Released: ")[-1].strip()
        year_released = release.split("-")[0]
        title = show_link.split("watch-")[-1].split("-free")[0].replace("-"," ")
        return (title,year_released)

    def search(self, query: str) -> List[ShowResponse]:
        search_url: str = self.host_url + "/search/"
        query = query.strip().replace(" ","-")
        r: requests.Response = requests.get(search_url + query,headers=self.headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        search_results: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        show_responses: List[ShowResponse] = []
        for search_result in search_results:
            link_tag: lxml.html.HtmlElement = search_result.cssselect(".film-poster > a")[0]
            title: str = link_tag.get("title")
            link: str = link_tag.get("href")
            film_info_tags: List[lxml.html.HtmlElement] = search_result.cssselect(".film-detail .fd-infor span")
            film_info: str = film_info_tags[0].text
            is_tv: bool = True if film_info_tags[-1].text == "TV" else False
            show_responses.append(ShowResponse(title,self.host_url + link,is_tv,film_info))
            if len(show_responses) >= self.max_search_result:
                break
        return show_responses
        
