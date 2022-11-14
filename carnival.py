import click

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
        file_scan.dump(directory)
    if print_out:
        print(file_scan)


@click.argument("dir_b", type=click.Path(exists=True))
@click.argument("dir_a", type=click.Path(exists=True))
@click.command()
def compare(dir_a: str, dir_b: str):
    """
    Compare files in directories which paths are 'dir_a' and 'dir_b'
    """
    file_scan_a = FileScan.from_dump(dir_a)
    file_scan_b = FileScan.from_dump(dir_b)
    if file_scan_a.hashes ^ file_scan_b.hashes == set():
        print("EQUAL")
    else:
        print(f"Files missing in directory '{dir_a}':")
        missing = file_scan_b.hashes - file_scan_a.hashes
        for hash_key in missing:
            print("*", file_scan_b.files[hash_key].path)
        print(f"Files missing in directory '{dir_b}':")
        print(file_scan_a.hashes - file_scan_b.hashes)


@click.group()
def cli():
    ...


cli.add_command(scan)
cli.add_command(compare)

if __name__ == "__main__":
    cli()
