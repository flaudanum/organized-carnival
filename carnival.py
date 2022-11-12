from pathlib import Path

import click
import orjson

from src.file_scan import FileScan


@click.option("--print", "print_out", is_flag=True, help="Prints scan result to the standard output")
@click.option("--save", "save_scan", is_flag=True, help="Saves a dump of the scan in the directory")
@click.option(
    "--no-fhash",
    "no_file_hash",
    is_flag=True,
    help="Does not compute file hashes (improve performance)",
)
@click.argument("directory", type=click.Path(exists=True))
@click.command()
def scan(directory: str, no_file_hash: bool, save_scan: bool, print_out: bool):
    """
    DIRECTORY path to the scanned directory
    """
    file_scan = FileScan(directory, no_file_hash)
    if save_scan:
        with (Path(directory) / "carnival.dump.json").open("wb") as binary_io:
            binary_io.write(orjson.dumps(file_scan.to_dict()))
    if print_out:
        print(file_scan)


@click.group()
def cli():
    ...


cli.add_command(scan)

if __name__ == "__main__":
    cli()
