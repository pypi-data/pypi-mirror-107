import click

from slai_cli.run import local_server


def _start_local_server(port):
    click.echo(f"** Starting local flask server on port {port} ** \n")
    click.echo("-------------------------------------------------")
    local_server.app.run(host="0.0.0.0", port=port, debug=True)


@click.command()
@click.option("--port", default=5000, help="Port to bind flask app to.")
def run(port):
    """Run a model locally."""
    _start_local_server(port)
