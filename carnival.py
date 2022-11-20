import click

from src.file_scan import FileScan


@click.option(
    "--rescan", "complete_rescan", is_flag=True, help="Performs a complete scan regardless of an existing scan dump"
)
@click.option("--print", "print_out", is_flag=True, help="Prints scan result to the standard output")
@click.option("--no-fhash", "no_file_hash", is_flag=True, help="Does not compute file hashes (improve performance)")
@click.argument("directory", type=click.Path(exists=True))
@click.command()
def scan(directory: str, no_file_hash: bool, print_out: bool, complete_rescan: bool):
    """
    DIRECTORY path to the scanned directory
    """
    file_scan = FileScan(directory, no_file_hash, complete_rescan)
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
            for info in file_scan_b.files[hash_key]:
                print("*", info.path)
        print(f"Files missing in directory '{dir_b}':")
        missing = file_scan_a.hashes - file_scan_b.hashes
        for hash_key in missing:
            for info in file_scan_b.files[hash_key]:
                print("*", info.path)


@click.group()
def cli():
    ...


cli.add_command(scan)
cli.add_command(compare)

if __name__ == "__main__":
    cli()
