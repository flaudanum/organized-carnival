import os
from pathlib import Path

import click

from src.file_infos import FileInfo
from src.file_scan import FileScan
from src.hasher import Hasher


@click.argument("directory", type=click.Path(exists=True))
@click.command()
def scan(directory: str):
    file_scan = FileScan(directory)
    print(file_scan)


@click.group()
def cli():
    ...


cli.add_command(scan)

if __name__ == "__main__":
    cli()
