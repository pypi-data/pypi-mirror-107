import click
import sys

# REMOVE THESE
sys.path.append("../slai")
sys.path.append("../../slai")

from functools import update_wrapper
from slai_cli.run import commands as run
from slai_cli.create import commands as create
from slai_cli.model import commands as model
from slai_cli.profile import commands as profile
from slai_cli.decorators import requires_slai_credentials


def with_profile(f):
    @click.pass_context
    def run(ctx, *args, **kwargs):
        _f = requires_slai_credentials(f, **kwargs)
        return ctx.invoke(_f, *args, **kwargs)

    return update_wrapper(run, f)


@click.group()
@click.option("--profile", required=False, default="default", help="Profile to use")
@with_profile
def entry_point(profile):
    pass


def main():
    entry_point.add_command(run.run)
    entry_point.add_command(create.create)
    entry_point.add_command(model.model)
    entry_point.add_command(profile.profile)

    entry_point()


if __name__ == "__main__":
    sys.exit(main())
