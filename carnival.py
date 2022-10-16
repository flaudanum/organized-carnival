from pathlib import Path

import click


@click.argument('directory', type=click.Path(exists=True))
@click.command()
def tree(directory: str):
    dir_path = Path(directory)
    print(dir_path.absolute())


@click.group()
def cli():
    ...


cli.add_command(tree)

if __name__ == '__main__':
    cli()
