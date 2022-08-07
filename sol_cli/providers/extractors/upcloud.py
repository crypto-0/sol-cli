from video_extractor import *
import requests

class UpCloud(VideoExtractor):
    sources_base_url = "https://mzzcloud.life/ajax/embed-4/getSources?id="
    headers =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }
    def extract(self) -> VideoContainer:
        embed = self.server.embed.rsplit("/",1)[-1]
        r = requests.get(self.sources_base_url + embed,headers=self.headers)
        video_info = r.json()
        video_sources = video_info["sources"]
        video_tracks = video_info["tracks"]
        for video_source in video_sources:
            self.videos.append(Video("",True,video_sources["file"]))
        for track in video_tracks:
            self.subtitles.append(Subtitle(track["label"],track["file"]))
        return VideoContainer(self.videos,self.subtitles)
