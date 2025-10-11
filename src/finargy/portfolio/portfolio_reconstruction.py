import datetime

import pandas as pd
import tqdm

from finargy.api.client import InvertirOnlineAPI
from finargy.api.market_data.symbol_data import get_symbol_history
from finargy.api.account_data import get_account_movements_finished
from finargy.data_processing.utils import get_end_of_day, parse_date_df

COLUMNS_TRANSLATE = {
    "numero": "order_number",
    "fechaOrden": "order_date",
    "tipo": "type",
    "estado": "status",
    "mercado": "market",
    "simbolo": "ticker",
    "cantidad": "quantity",
    "monto": "amount",
    "modalidad": "modality",
    "precio": "price",
    "fechaOperada": "execution_date",
    "cantidadOperada": "executed_quantity",
    "precioOperado": "executed_price",
    "montoOperado": "executed_amount",
    "plazo": "term",
}

DATE_COLS = ["order_date", "execution_date"]


ADJUSTMENTS_COLUMNS = {
    "In/out": "in_out",
    "Comitente": "account_nbr",
    "Mercado": "market",
    "Especie": "symbol",
    "Broker": "broker",
    "Cantidad": "quantity",
    "Comitente contraparte": "counterpart_account",
    "Tipo": "type",
    "Fecha": "operation_date",
    "Estado": "status",
    "Comisión": "commission",
}


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


def parse_movements(movements_resp: dict) -> pd.DataFrame:
    """Parse a DataFrame with movements data."""
    movements_df = pd.DataFrame(movements_resp)
    movements_df = movements_df.rename(columns=COLUMNS_TRANSLATE)

    # parse DATE_COLS
    for col in DATE_COLS:
        movements_df[col] = movements_df[col].str.split(".").str[0]
        movements_df[col] = pd.to_datetime(movements_df[col])

    # quantity to integer
    movements_df["quantity"] = movements_df["quantity"].fillna(0).astype("int")
    movements_df["executed_quantity"] = (
        movements_df["executed_quantity"].fillna(0).astype("int")
    )

    return movements_df


def parse_adjustments(df):
    """Parse adjustments DataFrame with standardized column names."""
    df = df.rename(columns=ADJUSTMENTS_COLUMNS)

    # Convert date column
    df["operation_date"] = pd.to_datetime(df["operation_date"], format="%d/%m/%Y")

    # Convert quantity to numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Clean commission column (remove $ and convert to numeric)
    df["commission"] = df["commission"].str.replace("$", "").str.strip()
    df["commission"] = pd.to_numeric(df["commission"], errors="coerce")

    return df


def get_symbol_min_max_dates(movements_df):
    # get min dates for each symbol that is of type 'Compra'
    min_max_dates_df = (
        movements_df.groupby(["ticker", "market"])["execution_date"]
        .agg(["min", "max"])
        .reset_index()
    )

    return min_max_dates_df


def parse_symbol_data(symbol_response):
    symbol_df = pd.DataFrame(symbol_response)
    symbol_df = parse_date_df(symbol_df, "fechaHora")
    symbol_df = get_end_of_day(symbol_df, "fechaHora")
    # get only the columns we need
    symbol_df = symbol_df[["fechaHora_date", "ultimoPrecio"]]

    return symbol_df


def get_symbol(
    symbol: str,
    client: InvertirOnlineAPI,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    symbol_response = get_symbol_history(
        client=client, symbol=symbol, date_start=start_date, date_end=end_date
    )
    symbol_df = parse_symbol_data(symbol_response)
    symbol_df = get_end_of_day(symbol_df, "fechaHora")
    symbol_df = symbol_df[["date", "price"]]

    return symbol_df


def get_all_symbols(client: InvertirOnlineAPI, symbol_dates: pd.DataFrame):
    # get hystorical symbol data for each symbol
    symbol_data = {}
    # add progress bar
    for i, row in tqdm.tqdm(symbol_dates.iterrows()):
        symbol = row["ticker"]
        mercado = row["market"]
        symbol_response = get_symbol_history(
            client=client,
            symbol=symbol,
            date_start=row["min"],
            date_end=datetime.datetime.now(),
        )

        # if no data (empty list) continue
        if not symbol_response:
            print(f"Invalid data for symbol {symbol} in market {mercado}")
            continue

        symbol_df = pd.DataFrame(symbol_response)
        symbol_df = parse_date_df(symbol_df, "fechaHora")
        symbol_df = get_end_of_day(symbol_df, "fechaHora")
        # get only the columns we need
        symbol_df = symbol_df[["fechaHora", "ultimoPrecio"]]
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


def portfolio_reconstruction(
    client: InvertirOnlineAPI,
    start_date: datetime.datetime = None,
    end_date: datetime.datetime = None,
):

    if start_date is None:
        start_date = datetime.datetime(2021, 1, 1)
        print("Start date is None, using 2021-01-01.")
    if end_date is None:
        end_date = datetime.datetime.now()
        print("End date is None, using today's date.")

    account_movements = get_account_movements_finished(
        client=client, date_start=start_date
    )
    account_movements_df = parse_movements(account_movements)

    # get all symbols
    symbol_dates = get_symbol_min_max_dates(account_movements_df)
    # consolidate movements
    master_df = get_all_symbols(client, symbol_dates)

    return master_df, account_movements_df


if __name__ == "__main__":
    # create a client
    client = InvertirOnlineAPI()

    historical_prices_path = "data/historical_prices.csv"
    account_movements_path = "data/portfolio/account_movements_df.csv"

    # check if file exists
    try:
        master_df = pd.read_csv(historical_prices_path)
        account_movements_df = pd.read_csv(account_movements_path)

        # Get the max date from the existing data
        max_date_historical = pd.to_datetime(master_df["fechaHora_date"]).max()
        max_date_movements = pd.to_datetime(account_movements_df["fecha_orden"]).max()

        # Use the latest date from both datasets as the new start date
        max_historical_date = max(max_date_historical, max_date_movements)
        incremental_date = min(max_historical_date, max_date_movements)

        if max_historical_date.date() < datetime.datetime.now().date():
            print(f"Downloading incremental data from {incremental_date}")

            # Download incremental data
            master_df_incr, account_movements_df_incr = portfolio_reconstruction(
                client=client,
                start_date=incremental_date,
                end_date=datetime.datetime.now().date(),
            )
            combined_master_df = pd.concat([master_df, master_df_incr])
            combined_account_movements_df = pd.concat(
                [account_movements_df, account_movements_df_incr]
            )
            # Save the combined data
            combined_master_df.to_csv(historical_prices_path, index=False)
            combined_account_movements_df.to_csv(account_movements_path, index=False)
        else:
            print("Data is already up to date.")
    except FileNotFoundError:
        # create a client
        client = InvertirOnlineAPI()
        start_date = datetime.datetime(2021, 1, 1)
        end_date = datetime.datetime.now().date()
        print(f"No price local data available, downloading from {start_date}")
        master_df, account_movements_df = portfolio_reconstruction(
            client=client,
            start_date=start_date,
            end_date=datetime.datetime.now().date(),
        )
        master_df.to_csv(historical_prices_path, index=False)
        account_movements_df.to_csv(account_movements_path, index=False)
