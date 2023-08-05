import click
import pendulum
from pandas import DataFrame

from heaume_cli.utils.console import console
from heaume_cli.utils.influxdb import query


@click.command()
@click.option("--name", help="The name of the plant", required=True)
@click.option(
    "--type",
    help="The output representation",
    default="nice",
    type=click.Choice(["nice", "csv"], case_sensitive=False),
    show_default=True,
)
def status(name, type):
    """
    The status command gives the latest values from a plant.
    """
    metrics = query(
        f"""
        from(bucket: "Plant")
            |> range(start: -1d)
            |> filter(fn: (r) => r.name == "{name}")
            |> sort(columns: ["_time"], desc: true)
            |> keep(columns: ["_measurement", "_time", "_value", "unit"])
            |> limit(n: 1)
        """
    )

    if type == "csv":
        print_csv(metrics)
    else:
        print_beautify(name, metrics)


def print_csv(metrics: DataFrame) -> None:
    """
    Print the status of a plant in CSV.

    :param metrics: The metrics of the plant.
    :type metrics: DataFrame
    """
    if not metrics.size:
        console.print("null")
        return

    console.print(metrics.to_csv(index=False)[:-1])


def print_beautify(name: str, metrics: DataFrame) -> None:
    """
    Print the status of a plant in a nice way.

    :param name: The name of the plant.
    :type name: str
    :param metrics: The metrics of the plant.
    :type metrics: DataFrame
    """
    if not metrics.size:
        console.print(f"The plant named {name} doesn't exists.")
        return

    header = f"[bold green]:herb:[/bold green] Status of {name.capitalize()}"
    last_time = (
        pendulum.instance(metrics.iloc[0]["time"]).diff_for_humans()
        if metrics.size > 0
        else "More than one day"
    )
    spacing_measurement = max([len(m) for m in metrics["measurement"]])

    console.print(header)
    for row in metrics.itertuples():
        measurement = row.measurement
        value = row.value
        unit = row.unit
        title = measurement + " " * (spacing_measurement - len(measurement))
        console.print(f"   {title} > {value} {unit}")
    console.print(f"[bold u]Last update:[/bold u] {last_time}")
