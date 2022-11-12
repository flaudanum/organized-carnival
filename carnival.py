import click

from src.file_scan import FileScan


@click.option(
    "--no-fhash",
    "no_file_hash",
    is_flag=True,
    help="Does not compute file hashes (improve performance)",
)
@click.argument("directory", type=click.Path(exists=True))
@click.command()
def scan(directory: str, no_file_hash: bool):
    """
    DIRECTORY path to the scanned directory
    """
    file_scan = FileScan(directory, no_file_hash)
    print(file_scan)


@click.group()
def cli():
    ...


cli.add_command(scan)

if __name__ == "__main__":
    cli()
