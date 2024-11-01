from pytest import param
from finargy.api.client import InvertirOnlineAPI
import datetime


# GET /api/v2/portafolio/{pais}
def get_portfolio(client: InvertirOnlineAPI, country="argentina"):
    """Retrieve portfolio data."""
    return client._request("GET", "portafolio")


# GET /api/v2/estadocuenta
def get_account_summary(client: InvertirOnlineAPI):
    """Retrieve account summary data."""
    return client._request("GET", "estadocuenta")


# GET /api/v2/operaciones
def get_account_movements(
    client: InvertirOnlineAPI,
    date_start: datetime.datetime,
    date_end: datetime.datetime = None,
    **kwargs,
):
    """Retrieve account finished movements data."""
    if date_start is None:
        raise ValueError("date_start is required.")

    if date_end is None:
        date_end = datetime.datetime.now().date()

    # convert to compatible format
    if isinstance(date_start, datetime.datetime):
        date_start = date_start.strftime("%Y-%m-%d")
    if isinstance(date_end, datetime.datetime):
        date_end = date_end.strftime("%Y-%m-%d")

    params = {"fechaDesde": date_start, "fechaHasta": date_end}

    params = {**params, **kwargs}
    return client._request("GET", "operaciones", params=params)


# GET /api/v2/operaciones


def get_account_movements_finished(
    client: InvertirOnlineAPI,
    date_start: datetime.datetime,
    date_end: datetime.datetime = None,
):
    """
    Get account movements finished.
    args:
        client: InvertirOnlineAPI: API client
        date_start: datetime.datetime
        date_end: datetime.datetime
    """
    """Retrieve account finished movements data."""
    return get_account_movements(client, date_start, date_end, estado="terminadas")


# GET /api/v2/operaciones/{numero}
def get_operation(client: InvertirOnlineAPI, number=None):
    """Retrieve operation data."""
    return client._request("GET", f"operaciones/{number}")
