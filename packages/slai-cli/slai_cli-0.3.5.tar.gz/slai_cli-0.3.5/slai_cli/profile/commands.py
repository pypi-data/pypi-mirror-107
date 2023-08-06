import click


from slai_cli.profile import configure as _configure
from slai_cli.profile import list as _list
from slai.modules.runtime import ValidRuntimes


@click.group()
def profile():
    pass


@click.argument("profile_name")
@profile.command()
def configure(profile_name):
    _configure.get_credentials(profile_name=profile_name, runtime=ValidRuntimes.Local)


@profile.command()
def list():
    _list.list_profiles()
