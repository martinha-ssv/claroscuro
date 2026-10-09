import click

@click.command()
def init():
    """Initialize the Claroscuro project."""
    click.echo("Generating pretty colors...")
    generator = ThemeGenerator()
    palettes = generator.generate()
    click.echo("Displaying generated themes.")
    