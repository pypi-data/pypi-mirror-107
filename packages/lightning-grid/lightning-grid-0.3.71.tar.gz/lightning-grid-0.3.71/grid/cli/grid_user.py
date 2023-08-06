import click

from grid.client import Grid


@click.command()
def user():
    """Show user information."""

    client = Grid()

    user_info = client.get_user_info()

    email = user_info['email']
    email = email if email is not None else "N/A"

    click.echo(f"Display name: {user_info['firstName']} {user_info['lastName']}")
    click.echo(f"Username    : {user_info['username']}")
    click.echo(f"Email       : {email}")
