import click

import mirrulations.csv
import mirrulations.fetch

@click.group()
def cli():
    """A command-line tool for working with regulations.gov docket data from the Mirrulations dataset."""
    pass

cli.add_command(mirrulations.csv.main)
cli.add_command(mirrulations.fetch.main)


if __name__ == '__main__':
    cli()
