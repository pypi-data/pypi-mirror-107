import click
from click.exceptions import ClickException

from grid.client import Grid
from grid.utilities import is_experiment


@click.command()
@click.argument('run_or_experiment_or_session', type=str, nargs=1, required=True)
def stop(run_or_experiment_or_session: str):
    """Stop a run, an experiment or a session."""

    client = Grid()

    if is_experiment(run_or_experiment_or_session):
        client.cancel(experiment_name=run_or_experiment_or_session)
    elif client.is_run(run_name=run_or_experiment_or_session):
        client.cancel(run_name=run_or_experiment_or_session)
    elif client.is_interactive_node(interactive_node_name=run_or_experiment_or_session):
        client.delete_interactive_node(interactive_node_name=run_or_experiment_or_session)
    else:
        raise ClickException(f"Could not find resource {run_or_experiment_or_session}")
