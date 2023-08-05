import click
from typing import List

from heaume_cli.utils.console import console
import requests

@click.command()
@click.option("--email", help="The email of the japascan user", required=True, envvar="HEAUME_JAPSCAN_EMAIL")
@click.option("--api-key", help="The api key of the japscan api", required=True, envvar="HEAUME_JAPSCAN_API_KEY")
@click.option(
    "--type",
    help="The output representation",
    default="nice",
    type=click.Choice(["nice", "raw"], case_sensitive=False),
    show_default=True,
)
@click.option("--add", help="Add a target to the targets", multiple=True)
@click.option("--delete", help="Delete a target to the targets", multiple=True)
def target(email, api_key, type, add, delete):
    """
    The status command gives the all plants of the system
    """
    endpoint = "https://s5snn6c3n1.execute-api.eu-west-1.amazonaws.com/Stage"
    route = "targets"
    headers = {"Api-Key": api_key}
    
    if not add and not delete:
        response = requests.get(f"{endpoint}/{route}?email={email}", headers=headers)
    else:
        if add:
            response = requests.post(f"{endpoint}/{route}?email={email}", json={"targets": list(add)}, headers=headers)
        if delete:
            response = requests.delete(f"{endpoint}/{route}?email={email}", json={"targets": list(delete)}, headers=headers)        

    targets = response.json()

    if type == "raw":
        print_raw(targets)
    else:
        print_beautify(targets)


def print_raw(targets: List[str]) -> None:
    """
    Print the status of a plant in CSV.

    :param metrics: The metrics of the plant.
    :type metrics: DataFrame
    """
    console.print(targets)


def print_beautify(targets: List[str]) -> None:
    """
    Print the all status of the plants in a nice way.

    :param metrics: The metrics of the plant.
    :type metrics: DataFrame
    """
    if not targets:
        console.print("Cet user n'a pas de targets.")
    else:
        console.print("Les targets de cet user sont:")
        for target in targets:
            console.print(f" - {target}")
