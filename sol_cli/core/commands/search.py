from typing_extensions import Required
from ..providers.sol import Sol
import click
import sys

@click.command(name="search", help="Search for a movie or show.")
@click.argument("query", required=True)
def sol_cli_search(query:str):
    sol: Sol = Sol()
    q_results: list = sol.search(query=query)
    alternate_color: bool = True
    color: str = "white"
    if len(q_results) == 0:
        click.echo(click.style("No search results were found",fg="red"))
        sys.exit()
    for index,result in enumerate(q_results,start=1):
        click.echo(click.style("[{index:^2}] {result_title} ({result_info})".format(index=index,result_title= result.title,result_info=result.info) ,fg=color))
        color = "green" if alternate_color else "white"
        alternate_color = not alternate_color
    
