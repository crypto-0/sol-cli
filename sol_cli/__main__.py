import click
from .core.commands import download,search
from typing import Dict

commands: Dict = {
        "download": download.sol_cli_download,
        "search": search.sol_cli_search
        }

@click.group(commands=commands)
def __sol_cli__():
    pass

if __name__ == "__main__":
    __sol_cli__()
