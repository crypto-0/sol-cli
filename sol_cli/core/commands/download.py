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
    for index,item in enumerate(items,start=1):
            color = "yellow" if alternate_color else "white"
            alternate_color = not alternate_color
            if item_type == 0:
                formated_string = "[{index:^2}] {item_title} ({item_info})".format(item.title,item.info)
            elif item_type == 1:
                formated_string = "[{index:^2}] {item_title} ({item_info})".format(item.title,item.season_number)
            elif item_type == 2:
                formated_string = "[{index:^2}] Episode: {episode_number}".format(index,item.episode_number)
            elif item_type == 3:
                formated_string = "[{index:^2}] Server: {item_title}}"
            else:
                formated_string = "[{index:^2}] {item}".format(item)
            click.secho(formated_string,fg=color)


@click.command(name="download", help="Search for a movie or show.")
@click.argument("query", required=True)
def sol_cli_download(query:str):
    color: str = "white"
    alternate_color: bool = True
    sol: Sol = Sol()
    click.secho("Getting query results...",fg=color)
    q_results: list = sol.search(query=query)
    if len(q_results) == 0:
        click.echo(click.style("No search results were found",fg="red"))
        sys.exit()
    for index,result in enumerate(q_results,start=1):
        click.echo(click.style("[{index:^2}] {result_title} ({result_info})".format(index=index,result_title= result.title,result_info=result.info) ,fg=color))
        color = "yellow" if alternate_color else "white"
        alternate_color = not alternate_color
    while True:
        try:
            click.echo(click.style("Enter a number: ",fg=color),nl=False)
            choice = int(input())
        except ValueError:
            click.secho("Not an interger! Try again.",fg="red")
        else:
            if choice < 0 or choice > len(q_results):
                click.secho("Not a valid choice! Try again.",fg="red")
            else:
                break
    if q_results[choice - 1].is_tv:
        click.secho("Getting seasons...",fg=color)
        color = "yellow" if alternate_color else "white"
        alternate_color = not alternate_color
        link: str = (q_results[choice - 1].link).rsplit("-",1)[-1]
        seasons = sol.load_seasons(link)
        if len(seasons) == 0:
            click.echo(click.style("No seasons were found",fg="red"))
            sys.exit()
        for index,season in enumerate(seasons,start=1):
            click.echo(click.style("[{index:^2}] Season: {season_number}".format(index=index,season_number=season.season_number) ,fg=color))
            color = "yellow" if alternate_color else "white"
            alternate_color = not alternate_color

        while True:
            try:
                click.echo(click.style("Select a Season: ",fg=color),nl=False)
                choice = int(input())
            except ValueError:
                click.secho("Not an interger! Try again.",fg="red")
            else:
                if choice < 0 or choice > len(q_results):
                    click.secho("Not a valid choice! Try again.",fg="red")
                else:
                    break
        click.secho("Getting episodes...",fg=color)
        link: str = seasons[choice - 1].link
        episodes = sol.load_episodes(link)
        color = "yellow" if alternate_color else "white"
        alternate_color = not alternate_color
        if len(episodes) == 0:
            click.echo(click.style("No episodes were found",fg="red"))
            sys.exit()
        for index,episode in enumerate(episodes,start=1):
            click.echo(click.style("[{index:^2}] Episode: {episode_number}".format(index=index,episode_number=episode.episode_number) ,fg=color))
            color = "yellow" if alternate_color else "white"
            alternate_color = not alternate_color

        while True:
            click.echo(click.style("Select a episodes: ",fg=color),nl=False)
            choice_with_range: str = input()
            choice_parsed = re.finditer(r"(([0-9]*)-([0-9]*))|([0-9]*)",choice_with_range)
            episodes_to_download: list = []
            for choice_p in choice_parsed:
                if choice_p.group():
                    if choice_p.group(1):
                        start: int = int(choice_p.group(2)) -1 if choice_p.group(2) else 0
                        end: int = int(choice_p.group(3)) -1 if choice_p.group(3) else len(episodes) -1
                        if start <= end and start >=0 and end < len(episodes):
                            episodes_to_download.append((start,end))
                    else:
                        start: int = int(choice_p.group(4)) -1
                        end: int = int(choice_p.group(4)) -1
                        if start <= end and start >=0 and end < len(episodes):
                            episodes_to_download.append((start,end))
            if len(episodes_to_download) > 0:
                break
            else:
                click.secho("Not a valid choice of episodes! Try again.",fg="red")
        click.secho("Getting servers...",fg=color)
        all_servers: list = []
        for episode_range in episodes_to_download:
           for idx in range(episode_range[0],episode_range[1] +1):
               servers = sol.load_video_servers(episodes[idx].link)
               all_servers += servers
        click.secho("Getting extracters...",fg=color)
        all_extracters: list= []
        for server in all_servers:
            #if server.name =="Server UpCloud" or server.name == "Server Vidcloud":
            if  server.name == "Server Vidcloud":
                all_extracters.append(sol.get_vide_extractor(server=server))
        click.secho("Getting videos...",fg=color)
        all_containers: list = []
        for extractor in all_extracters:
            all_containers.append(extractor.extract())
        if all_containers:
            print(all_containers[0].videos[0].url)
            url = all_containers[0].videos[0].url
            with httpx.Client() as client:
                handle_download(client,url,sol.headers,pathlib.Path("."),"test")



