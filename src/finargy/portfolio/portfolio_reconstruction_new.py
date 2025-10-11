import datetime
import os
from pathlib import Path
import logging
from typing import List, Dict, Any

import pandas as pd
import tqdm

from finargy.api.client import InvertirOnlineAPI
from finargy.api.market_data.symbol_data import get_symbol_history
from finargy.api.account_data import get_account_movements_finished
from finargy.data_processing.utils import get_end_of_day, parse_date_df

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def parse_movements(movements_resp: Dict[str, Any]) -> pd.DataFrame:
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


def get_symbol_data(
    client: InvertirOnlineAPI,
    symbol: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> pd.DataFrame:
    """Get historical data for a single symbol"""
    try:
        symbol_response = get_symbol_history(
            client=client, symbol=symbol, date_start=start_date, date_end=end_date
        )

        symbol_df = pd.DataFrame(symbol_response)
        symbol_df = parse_date_df(symbol_df, "fechaHora")
        symbol_df = get_end_of_day(symbol_df, "fechaHora")
        symbol_df = symbol_df[["fechaHora_date", "ultimoPrecio"]]
        return symbol_df
    except Exception as e:
        logger.error(f"Error downloading data for symbol {symbol}: {str(e)}")
        return pd.DataFrame()


def update_symbol_data(
    symbol: str, existing_data: pd.DataFrame, client: InvertirOnlineAPI
) -> pd.DataFrame:
    """Update data for a single symbol"""
    if len(existing_data) > 0:
        last_date = pd.to_datetime(existing_data["fechaHora_date"]).max()
        start_date = last_date + pd.Timedelta(days=1)
    else:
        start_date = datetime.datetime(2021, 1, 1)

    end_date = datetime.datetime.now()

    if start_date.date() >= end_date.date():
        logger.info(f"Symbol {symbol} is up to date")
        return existing_data

    logger.info(f"Downloading incremental data for {symbol} from {start_date}")
    new_data = get_symbol_data(client, symbol, start_date, end_date)

    if len(new_data) > 0:
        return pd.concat([existing_data, new_data]).drop_duplicates(
            subset=["fechaHora_date"]
        )
    return existing_data


def load_or_create_data(file_path: Path) -> pd.DataFrame:
    """Load existing data or return empty DataFrame"""
    if file_path.exists():
        return pd.read_csv(file_path)
    return pd.DataFrame()


def main():
    client = InvertirOnlineAPI()
    data_dir = Path("data/portfolio")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Get account movements
    movements_file = data_dir / "account_movements_df.csv"
    account_movements_df = load_or_create_data(movements_file)

    if len(account_movements_df) > 0:
        last_movement_date = pd.to_datetime(account_movements_df["fecha_orden"]).max()
        start_date = last_movement_date + pd.Timedelta(days=1)
    else:
        start_date = datetime.datetime(2021, 1, 1)

    # Update movements
    new_movements = get_account_movements_finished(client=client, date_start=start_date)
    if new_movements:
        new_movements_df = parse_movements(new_movements)
        account_movements_df = pd.concat([account_movements_df, new_movements_df])
        account_movements_df.to_csv(movements_file, index=False)

    # Process each symbol independently
    symbol_dates = get_symbol_min_max_dates(account_movements_df)

    for _, row in symbol_dates.iterrows():
        symbol = row["simbolo"]
        symbol_file = data_dir / f"historical_prices_{symbol}.csv"

        # Load existing data for this symbol
        symbol_data = load_or_create_data(symbol_file)

        # Update symbol data
        updated_data = update_symbol_data(symbol, symbol_data, client)

        if len(updated_data) > 0:
            updated_data.to_csv(symbol_file, index=False)


if __name__ == "__main__":
    main()
