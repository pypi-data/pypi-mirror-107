import click
from pandas import DataFrame

from heaume_cli.utils.console import console
from heaume_cli.utils.influxdb import query


@click.command()
@click.option(
    "--type",
    help="The output representation",
    default="nice",
    type=click.Choice(["nice", "csv"], case_sensitive=False),
    show_default=True,
)
def ls(type):
    """
    The status command gives the all plants of the system
    """
    metrics = query(
        f"""
        from(bucket: "Plant")
            |> range(start: -1d)
            |> group(columns: ["name"], mode:"by")
            |> distinct(column: "name")
            |> keep(columns: ["name"])
        """
    )

    if type == "csv":
        print_csv(metrics)
    else:
        print_beautify(metrics)


def print_csv(metrics: DataFrame) -> None:
    """
    Print the status of a plant in CSV.

    :param metrics: The metrics of the plant.
    :type metrics: DataFrame
    """
    if not metrics.size:
        console.print("null")
        return

    console.print(metrics.to_csv(index=False, header=False)[:-1])


def print_beautify(metrics: DataFrame) -> None:
    """
    Print the all status of the plants in a nice way.

    :param metrics: The metrics of the plant.
    :type metrics: DataFrame
    """
    if not metrics.size:
        console.print("There is no plant in the system.")
        return

    console.print("[bold green]:herb:[/bold green] Plants of the system:")
    for row in metrics.itertuples():
        console.print(f"   {row.name.capitalize()}")
