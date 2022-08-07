from video_extractor import *
from typing import Dict,List
import requests

class Vidcloud(VideoExtractor):
    sources_base_url: str = "https://rabbitstream.net/ajax/embed-4/getSources?id="
    headers: Dict =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }
    def extract(self) -> VideoContainer:
        embed = self.server.embed.rsplit("/",1)[-1].rstrip("?z=")
        r: requests.Response = requests.get(self.sources_base_url + embed,headers=self.headers)
        video_info: Dict = r.json()
        video_sources: List[Dict] = video_info["sources"]
        video_tracks: List[Dict] = video_info["tracks"]
        for video_source in video_sources:
            self.videos.append(Video("",True,video_source["file"]))
        for track in video_tracks:
            self.subtitles.append(Subtitle(track["label"],track["file"]))
        return VideoContainer(self.videos,self.subtitles)
