from numpy import save
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from finargy import portfolio


class PortfolioAnalyzer:
    def __init__(self, transactions_file, historical_data_file):
        self.transactions = pd.read_csv(transactions_file)
        self.historical_data = pd.read_csv(historical_data_file)

    def preprocess_data(self):
        # Convert date columns to datetime
        self.transactions["fecha_operada"] = pd.to_datetime(
            self.transactions["fecha_operada"]
        )
        self.historical_data["fechaHora_date"] = pd.to_datetime(
            self.historical_data["fechaHora_date"]
        )

        # Sort data by date
        self.transactions = self.transactions.sort_values("fecha_operada")
        self.historical_data = self.historical_data.sort_values("fechaHora_date")

        # Rename columns
        self.transactions = self.transactions.rename(columns={"fecha_operada": "date"})
        self.historical_data = self.historical_data.rename(
            columns={"fechaHora_date": "date"}
        )
        # filter only purchases and sales (exclude dividends)
        self.transactions = self.transactions[
            self.transactions["tipo"].isin(["Compra", "Venta"])
        ]

        self.transactions["base_asset"] = self.transactions["simbolo"].apply(
            lambda x: x[:-1] if x.endswith("D") else x
        )
        self.historical_data["base_asset"] = self.historical_data["symbol"].apply(
            lambda x: x[:-1] if x.endswith("D") else x
        )
        # if Venta, change sign of cantidadOperada and montoOperado. Dont use Apply
        self.transactions.loc[
            self.transactions["tipo"] == "Venta", "cantidadOperada"
        ] = (
            -1
            * self.transactions.loc[self.transactions["tipo"] == "Venta"][
                "cantidadOperada"
            ]
        )
        self.transactions.loc[self.transactions["tipo"] == "Venta", "montoOperado"] = (
            -1
            * self.transactions.loc[self.transactions["tipo"] == "Venta"][
                "montoOperado"
            ]
        )

    def calculate_cumulative_asset_value(self, asset, start_date, end_date):
        # Filter transactions and historical data for the specific asset and date range
        asset_transactions = self.transactions[
            (self.transactions["base_asset"] == asset)
            & (self.transactions["date"] >= start_date)
            & (self.transactions["date"] <= end_date)
            & self.transactions["tipo"].isin(["Compra", "Venta"])
        ]

        asset_historical = self.historical_data[
            (self.historical_data["base_asset"] == asset)
            & (self.historical_data["date"] >= start_date)
            & (self.historical_data["date"] <= end_date)
        ]

        # Calculate cumulative quantity
        asset_transactions["cumulative_quantity"] = asset_transactions[
            "cantidadOperada"
        ].cumsum()

        # Merge transactions with historical data
        merged_data = pd.merge_asof(
            asset_historical,
            asset_transactions[["date", "cumulative_quantity"]],
            on="date",
            direction="backward",
        )

        # Calculate daily value
        merged_data["daily_value"] = (
            merged_data["ultimoPrecio"] * merged_data["cumulative_quantity"]
        )

        # Calculate performance
        initial_value = merged_data["daily_value"].iloc[0]
        merged_data["performance"] = (
            (merged_data["daily_value"] - initial_value) / initial_value * 100
        )

        return merged_data

    def portfolio_total_value(self, start_date, end_date):
        # Calculate total portfolio value for each day
        assets_datasets = []
        for asset in self.transactions["base_asset"].unique():
            asset_data = self.calculate_cumulative_asset_value(
                asset, start_date, end_date
            )
            assets_datasets.append(asset_data)

        # stack all datasets
        portfolio_data = pd.concat(assets_datasets, axis=0)
        return portfolio_data


if __name__ == "__main__":
    # Usage example
    analyzer = PortfolioAnalyzer("data/movements_df.csv", "master_df.csv")
    analyzer.preprocess_data()

    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)

    portfolio_data = analyzer.portfolio_total_value(
        start_date=datetime(2020, 1, 1), end_date=datetime(2024, 6, 30)
    )

    save_path = "portfolio_value.csv"
    portfolio_data.to_csv(save_path, index=False)
