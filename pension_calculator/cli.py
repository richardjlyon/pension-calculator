"""
cli.py

Command line interface for pension calculator

29 September 2022
"""


import click


@click.group()
def cli():
    pass


@click.command()
@click.option("--yob", default=1965, help="Year of birth")
@click.option("--size", default=100, help="House size (m2)")
def compute(yob, size):
    """Compute relative energy costs."""
    click.echo("Computing")


cli.add_command(compute)

if __name__ == "__main__":
    cli()
