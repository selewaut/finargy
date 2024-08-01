import datetime

import pandas as pd
import tqdm

from finargy.api.client import InvertirOnlineAPI
from finargy.api.market_data.symbol_data import get_symbol_history
from finargy.api.account_data import get_account_movements_finished
from finargy.data_processing.utils import get_end_of_day, parse_date_df


def create_calendar_df(
    start_date: datetime.datetime, end_date: datetime.datetime = None
):
    """Create a calendar DataFrame with dates between start and end dates."""
    if end_date is None:
        end_date = datetime.datetime.now()
    if end_date < start_date:
        raise ValueError("End date must be greater than start date.")

    calendar = pd.date_range(start=start_date, end=end_date, freq="D")
    calendar_df = pd.DataFrame(calendar, columns=["fecha"])
    # convert to date.
    calendar_df["fecha"] = calendar_df["fecha"].dt.date

    return calendar_df


def parse_movements(movements_resp):
    """Parse a DataFrame with movements data."""
    movements_df = pd.DataFrame(movements_resp)
    # convert fechaOrden to date, first remove . character
    date_cols = ["fechaOrden", "fechaOperada"]

    # apply

    movements_df["fechaOrden"] = movements_df["fechaOrden"].str.split(".").str[0]
    movements_df["fechaOrden"] = pd.to_datetime(movements_df["fechaOrden"])

    movements_df["fechaOperada"] = movements_df["fechaOperada"].str.split(".").str[0]
    movements_df["fechaOperada"] = pd.to_datetime(movements_df["fechaOperada"])

    movements_df["fecha_orden"] = movements_df["fechaOrden"].dt.date
    movements_df["fecha_operada"] = movements_df["fechaOperada"].dt.date

    return movements_df


def get_symbol_min_max_dates(movements_df):
    # get min dates for each symbol that is of type 'Compra'
    min_max_dates = (
        movements_df[movements_df["tipo"] == "Compra"]
        .groupby(["simbolo", "mercado"])["fecha_orden"]
        .agg(["min", "max"])
        .reset_index()
    )
    min_max_dates
    return min_max_dates


def get_all_symbols(client: InvertirOnlineAPI, symbol_dates: pd.DataFrame):
    # get hystorical symbol data for each symbol
    symbol_data = {}
    # add progress bar
    for i, row in tqdm.tqdm(symbol_dates.iterrows()):
        symbol = row["simbolo"]
        mercado = row["mercado"]
        symbol_response = get_symbol_history(
            client=client,
            symbol=symbol,
            date_start=row["min"],
            date_end=datetime.datetime.now(),
        )

        symbol_df = pd.DataFrame(symbol_response)
        symbol_df = parse_date_df(symbol_df, "fechaHora")
        symbol_df = get_end_of_day(symbol_df, "fechaHora")
        # get only the columns we need
        symbol_df = symbol_df[["fechaHora_date", "ultimoPrecio"]]
        symbol_data[symbol] = symbol_df

    # concat all symbol data into a single dataframe
    master_df = pd.concat(
        symbol_data.values(), keys=symbol_data.keys(), names=["symbol"]
    ).reset_index()

    # drop duplicates keep first of each date symbol combination
    master_df = master_df.drop_duplicates(
        subset=["symbol", "fechaHora_date"], keep="first"
    ).reset_index(drop=True)
    # drop level_1
    master_df = master_df.drop(columns=["level_1"])

    return master_df


if __name__ == "__main__":
    # create a calendar dataframe
    start_date = datetime.datetime(2021, 1, 1)
    calendar_df = create_calendar_df(start_date)

    # create a client
    client = InvertirOnlineAPI()

    account_movements = get_account_movements_finished(
        client=client, date_start=start_date
    )
    account_movements_df = parse_movements(account_movements)

    # get all symbols
    symbol_dates = get_symbol_min_max_dates(account_movements_df)
    # consolidate movements
    master_df = get_all_symbols(client, symbol_dates)

    # save to csv
    master_df.to_csv("master_df.csv", index=False)
