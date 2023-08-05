import os

from influxdb_client import InfluxDBClient
from pandas import DataFrame


def query(query: str) -> DataFrame:
    """
    Query the influxDB database using the flux language.

    :param query: The query in flux.
    :type query: str
    :return: The dataframe representation of the query result.
    :rtype: DataFrame
    """
    influx_client = InfluxDBClient(
        url=os.environ["HEAUME_INFLUXDB_URL"],
        token=os.environ["HEAUME_INFLUXDB_TOKEN"],
        org="Heaume",
    )
    
    influx = influx_client.query_api()
    result = influx.query_data_frame(query)
    if result.size:
        result = result.drop(["result", "table"], axis=1)
        result = result.rename(
            columns={"_time": "time", "_value": "value", "_measurement": "measurement"}
        )
    return result
