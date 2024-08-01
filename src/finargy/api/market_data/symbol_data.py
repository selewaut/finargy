from finargy.api.client import InvertirOnlineAPI
from datetime import datetime


#  Symbol DATA.
# GET /api/v2/Cotizaciones/{Instrumento}/{Pais}/Todos
def get_all_symbol_data(
    client: InvertirOnlineAPI, instrument="acciones", country="argentina"
):
    """Retrieve data for all instruments."""
    return client._request("GET", f"{instrument}/{country}/Todos")


# GET /api/v2/Cotizaciones/{Instrumento}/{Panel}/{Pais}
def get_panel_symbol_data(
    client: InvertirOnlineAPI,
    instrument="acciones",
    panel="merval",
    country="argentina",
):
    """Retrieve data for all instruments in a specific panel."""
    return client._request("GET", f"Cotizaciones{instrument}/{panel}/{country}")


# Single symbol data.


# GET /api/v2/{mercado}/Titulos/{simbolo}
def get_symbol_data(client: InvertirOnlineAPI, market="bCBA", symbol=None):
    """Retrieve data for a specific instrument."""
    return client._request("GET", f"{market}/Titulos/{symbol}")


# GET /api/v2/{mercado}/Titulos/{simbolo}/CotizacionDetalle
def get_symbol_quote(client: InvertirOnlineAPI, market="bCBA", symbol=None):
    """Retrieve quote data for a specific instrument."""
    return client._request("GET", f"{market}/Titulos/{symbol}/CotizacionDetalle")


# GET /api/v2/{mercado}/Titulos/{simbolo}/CotizacionDetalleMobile/{plazo}
def get_symbol_quote_mobile(
    client: InvertirOnlineAPI, market="bCBA", symbol=None, settlement="t0"
):
    """Retrieve quote data for a specific instrument."""
    return client._request(
        "GET", f"{market}/Titulos/{symbol}/CotizacionDetalleMobile/{settlement}"
    )


# GET /api/v2/{mercado}/Titulos/{simbolo}/Cotizacion/serieHistorica/{fechaDesde}/{fechaHasta}/{ajustada}
def get_symbol_history(
    client: InvertirOnlineAPI,
    market="bCBA",
    symbol=None,
    date_start: datetime = None,
    date_end: datetime = None,
    adjusted=False,
):
    """Retrieve historical data for a specific instrument."""
    if adjusted:
        adjusted = "ajustada"
    else:
        adjusted = "sinAjustar"
    # convert datetime to strings.
    date_start = date_start.strftime("%Y-%m-%d")
    date_end = date_end.strftime("%Y-%m-%d")

    return client._request(
        "GET",
        f"{market}/Titulos/{symbol}/Cotizacion/serieHistorica/{date_start}/{date_end}/{adjusted}",
    )
