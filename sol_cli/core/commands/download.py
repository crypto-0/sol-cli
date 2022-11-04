import pathlib
from typing_extensions import Required
from ..providers.sol import Sol
import click
import sys
import re
import httpx
from ..downloaders.handle import handle_download

def print_info(items: list,item_type:int):
    alternate_color: bool = False
    for idx,item in enumerate(items,start=1):
            color = "cyan" if alternate_color else "white"
            alternate_color = not alternate_color
            if item_type == 0:
                formated_string = "[{index:^2}] {item_title} ({item_info})".format(index=idx,item_title=item.title,item_info=item.info)
            elif item_type == 1:
                formated_string = "[{index:^2}] Season: {season_number}".format(index=idx,season_number=item.season_number)
            elif item_type == 2:
                formated_string = "[{index:^2}] Episode: {episode_number}".format(index=idx,episode_number=item.episode_number)
            elif item_type == 3:
                formated_string = "[{index:^2}] Server: {item_title}}".format(index=idx,item_title=item.title)
            else:
                formated_string = "[{index:^2}] {item}".format(idx,item)
            click.secho(formated_string,fg=color)

def validate_choice(choice: str,choice_type: int,max_choice: int,results: list = []):
    if choice_type == 0 or choice_type == 1 or choice_type == 3:
        if not choice.isnumeric():
            click.secho("Choice needs to be an interger! Try again",fg="red")
            return False
        elif int(choice) < 0 or int(choice) > max_choice:
            click.secho("Choice is out of range! Try again",fg="red")
            return False
        else:
            return True
    elif choice_type == 2:
        choice_parsed = re.finditer(r"(([0-9]*)-([0-9]*))|([0-9]*)",choice)
        episodes_to_download: list = results
        for choice_p in choice_parsed:
            if choice_p.group():
                if choice_p.group(1):
                    start: int = int(choice_p.group(2)) -1 if choice_p.group(2) else 0
                    end: int = int(choice_p.group(3)) -1 if choice_p.group(3) else max_choice -1
                    if start <= end and start >=0 and end < max_choice:
                        episodes_to_download.append((start,end))
                else:
                    start: int = int(choice_p.group(4)) -1
                    end: int = int(choice_p.group(4)) -1
                    if start <= end and start >=0 and end < max_choice:
                        episodes_to_download.append((start,end))
        return True if episodes_to_download else False
    else:
        return False




@click.command(name="download", help="download  a movie or show by query")
@click.argument("query", required=True)
@click.option("-i", "--index",help="automatic choose index of query")
@click.option("-s", "--season",help="automatic select season index")
@click.option("-e", "--episode_ranges",help="select range of episodes")
@click.option("-q", "--quality",help="select quality if available")
@click.option("-d", "--dir",help="download directory")

def sol_cli_download(query:str,index,season,episode_ranges,quality,dir):
    color: str = "blue"
    sol: Sol = Sol()
    click.secho("Getting query results...",fg=color)
    q_results: list = sol.search(query=query)
    if len(q_results) == 0:
        click.echo(click.style("No search results were found",fg="red"))
        sys.exit()
    if index:
        choice = index
        validated_choice = validate_choice(choice,0,len(q_results))
        if not validated_choice:
            sys.exit()
    else:
        print_info(q_results,0)
        while True:
            click.echo(click.style("Enter a number: ",fg=color),nl=False)
            choice = input()
            validated_choice = validate_choice(choice,0,len(q_results))
            if validated_choice:
                index = choice
                break
    if q_results[int(choice) - 1].is_tv:
        click.secho("Getting seasons...",fg=color)
        link: str = (q_results[int(choice) - 1].link).rsplit("-",1)[-1]
        seasons = sol.load_seasons(link)
        if len(seasons) == 0:
            click.echo(click.style("No seasons were found",fg="red"))
            sys.exit()
        if season:
            choice = season
            validated_choice = validate_choice(choice,0,len(seasons))
            if not validated_choice:
                sys.exit()
        else:
            print_info(seasons,1)
            while True:
                click.echo(click.style("Select a Season: ",fg=color),nl=False)
                choice = input()
                validated_choice = validate_choice(choice,1,len(seasons))
                if validated_choice:
                    season = choice
                    break
        click.secho("Getting episodes...",fg=color)
        link: str = seasons[int(choice) - 1].link
        episodes = sol.load_episodes(link)
        if len(episodes) == 0:
            click.echo(click.style("No episodes were found",fg="red"))
            sys.exit()

        if episode_ranges:
            choice = episode_ranges;
            episodes_to_download = []
            validated_choice = validate_choice(choice,2,len(episodes),episodes_to_download)
            if not validated_choice:
                click.secho("Invalid choice! Try again",fg="red")
                sys.exit()
        else:
            print_info(episodes,2)
            while True:
                click.echo(click.style("Select range of episodes: ",fg=color),nl=False)
                episodes_to_download = []
                choice_with_range: str = input()
                validated_choice = validate_choice(choice_with_range,2,len(episodes),episodes_to_download)
                if episodes_to_download:
                    break
                else:
                    click.secho("Invalid choice! Try again",fg="red")
        click.secho("Getting servers...",fg=color)
        #all_servers: list = []
        episode_servers: dict = {}
        for episode_range in episodes_to_download:
           for idx in range(episode_range[0],episode_range[1] +1):
               if(episode_servers.get(idx) !=None):continue
               servers = sol.load_video_servers(episodes[idx].link)
               episode_servers[idx]=servers;
        click.secho("Getting extracters...",fg=color)
        episode_extracters: dict= {}
        for episode  in episode_servers:
            episode_extracters[episode] = []
            for server in episode_servers[episode]:
                extractor = sol.get_vide_extractor(server=server)
                if(extractor !=None):episode_extracters[episode].append(extractor)
                
        
        click.secho("Getting videos...",fg=color)
        episode_containers: dict={}
        for episode in episode_extracters:
            episode_containers[episode] = []
            for extractor in episode_extracters[episode]:
                episode_containers[episode].append(extractor.extract())

        title_name=q_results[int(index) -1].title.replace(" ","-")
        season = season.zfill(2)
        season_name = "Season " + season
        if not dir:
            dir = "."

        show_path = pathlib.Path("{dir}/{title_name}/{season_name}".format(dir=dir,title_name=title_name,season_name=season_name))
        pathlib.Path.mkdir(show_path,parents=True,exist_ok=True)
        click.secho("Downloading videos...",fg=color)
        with httpx.Client() as client:
            for episode in episode_containers:
                episode_name ="{title}-s{season}-e{episode}".format(title=title_name,season=season,episode=str(episode + 1).zfill(2))
                for episode_container in episode_containers[episode]:
                    try:
                        if(not episode_container.videos):continue
                        url = episode_container.videos[0].url
                        handle_download(client,url,sol.headers,show_path,episode_name)
                        break
                    except:
                        pass


