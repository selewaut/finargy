from finargy.api.client import InvertirOnlineAPI


def get_mep_price(client: InvertirOnlineAPI, symbol="AL30"):
    """Retrieve the MEP price."""
    # To get dollar MEP price you can use any bCBA symbol that has a dolar quote as well. For example AL30, GD30, which have AL30D and GD30D respectively.
    # You can also use CEDEAR instruments
    return client._request("GET", f"Cotizaciones/MEP/{symbol}")


# GET /api/v2/OperatoriaSimplificada/MontosEstimados/{monto}
def get_estimated_amounts(client: InvertirOnlineAPI, amount: float = None):
    """Retrieve estimated amounts for a specific amount."""
    return client._request("GET", f"OperatoriaSimplificada/MontosEstimados/{amount}")
