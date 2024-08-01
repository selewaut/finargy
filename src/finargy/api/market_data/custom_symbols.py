from threading import local
from finargy.api.market_data import InvertirOnlineAPI
from finargy.api.market_data.symbol_data import get_symbol_data, get_symbol_history
from finargy.api.market_data.simplified_market_data import get_mep_price


CCL_MAPPINGS = {
    "AL30": "AL30C",
    "APPL": "APPLC",
    "GD30": "GD30C",
    "SPY": "SPYC",
}

def get_ccl_dollar(client: InvertirOnlineAPI, symbol='AL30'):
    """Retrieve CCL dollar data."""
    
    try:
        d_symbol = CCL_MAPPINGS.get(symbol)
    except KeyError:
        raise ValueError(f"Invalid symbol. Use only {CCL_MAPPINGS.keys()}")
    mep_price = get_mep_price(client, symbol=symbol)

    return mep_price


def get_ccl_dollar_history(client: InvertirOnlineAPI, symbol='AL30', date_start=None, date_end=None, adjusted=False):
    """Retrieve historical data for the CCL dollar."""
    try:
        d_symbol = CCL_MAPPINGS.get(symbol)
    except KeyError:
        raise ValueError(f"Invalid symbol. Use only {CCL_MAPPINGS.keys()}")

    local_asset_history = get_symbol_history(client, symbol=symbol, date_start=date_start, date_end=date_end, adjusted=adjusted)
    dolar_asset_history = get_symbol_history(client, symbol=d_symbol, date_start=date_start, date_end=date_end, adjusted=adjusted)

    return local_asset_history, dolar_asset_history