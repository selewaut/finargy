import pandas as pd


def parse_date_df(df: pd.DataFrame, column_name: str):
    """Parse a date column in a DataFrame genrated from API data."""
    # remove  everything after . and convert to datetime
    df = df.rename(columns={"fechaHora": column_name})
    df[column_name] = df[column_name].str.split(".").str[0]
    df[column_name] = pd.to_datetime(df[column_name])
    # rename column
    return df


def get_end_of_day(df, date_column):
    """Get the end of day row for each date in a DataFrame generated from API data"""
    # sort by date and time
    df = df.sort_values(by=[date_column], ascending=False)
    # get last row for each date
    df = df.drop_duplicates(subset=date_column, keep="first")
    return df


def get_historical_series(historical_resp: dict, date_column: str):
    """Get historical series from API response."""
    df = pd.DataFrame(historical_resp)
    # parse date column
    df = parse_date_df(df, date_column)
    # get end of day data
    df = get_end_of_day(df, date_column)

    # rename price column
    df = df.rename(columns={"ultimoPrecio": "price"})
    return df
