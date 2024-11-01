import datetime

import pandas as pd

from finargy.api.client import InvertirOnlineAPI
from finargy.api.market_data.symbol_data import get_symbol_history
from finargy.data_processing.utils import get_historical_series


def get_mep_dollar_history(
    client: InvertirOnlineAPI,
    date_start: datetime = None,
    date_end: datetime = None,
    symbol="AL30",
    dollar_symbol="AL30D",
):

    local_symbol_history = get_symbol_history(
        client=client,
        symbol=symbol,
        date_start=date_start,
        date_end=date_end,
    )

    dollar_symbol_history = get_symbol_history(
        client=client,
        symbol=dollar_symbol,
        date_start=date_start,
        date_end=date_end,
    )

    local_symbol_df = get_historical_series(local_symbol_history, "fechaHora")

    dollar_symbol_df = get_historical_series(dollar_symbol_history, "fechaHora")

    join_suffixes = (f"_{symbol}", f"_{dollar_symbol}")

    # select only needed columns
    local_symbol_df = local_symbol_df[["fechaHora_date", "ultimoPrecio"]]
    dollar_symbol_df = dollar_symbol_df[["fechaHora_date", "ultimoPrecio"]]

    dolar_mep = pd.merge(
        local_symbol_df,
        dollar_symbol_df,
        on="fechaHora_date",
        how="inner",
        suffixes=join_suffixes,
    )

    dolar_mep["dollar_mep"] = (
        dolar_mep[f"ultimoPrecio_{symbol}"] / dolar_mep[f"ultimoPrecio_{dollar_symbol}"]
    )

    return dolar_mep[["fechaHora_date", "dollar_mep"]]


if __name__ == "__main__":
    client = InvertirOnlineAPI()
    dolar_mep = get_mep_dollar_history(
        client,
        symbol="AL30",
        dollar_symbol="AL30D",
        date_start=datetime.datetime(2021, 1, 1),
        date_end=datetime.datetime.now(),
    )
    print(dolar_mep)
