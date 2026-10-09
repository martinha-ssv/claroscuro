import click
from claroscuro.authoring.processing.generate import generate_color_palettes

@click.command()
def init():
    """Initialize the Claroscuro project."""
    click.echo("Generating pretty colors...")
    palettes = generate_color_palettes()
    click.echo(f"Generated {len(palettes)} palettes.")
