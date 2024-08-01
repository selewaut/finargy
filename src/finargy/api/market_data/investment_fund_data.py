from finargy.api.client import InvertirOnlineAPI

# Investment funds data. 
# GET /api/v2/Titulos/FCI
def get_investment_funds_data(client: InvertirOnlineAPI):
    """Retrieve data for all investment funds."""
    return client._request('GET', 'Titulos/FCI')

# GET /api/v2/Titulos/FCI/{simbolo}
def get_investment_fund_data(client: InvertirOnlineAPI, symbol=None):
    """Retrieve data for a specific investment fund."""
    return client._request('GET', f'Titulos/FCI/{symbol}')

# GET /api/v2/Titulos/FCI/TipoFondos
def get_investment_funds_types(client: InvertirOnlineAPI):
    """Retrieve data for all investment funds types."""
    return client._request('GET', 'Titulos/FCI/TipoFondos') 

# GET /api/v2/Titulos/FCI/Administradoras
def get_investment_funds_administrators(client: InvertirOnlineAPI):
    """Retrieve data for all investment funds administrators."""
    return client._request('GET', 'Titulos/FCI/Administradoras')

# GET /api/v2/Titulos/FCI/Administradoras/{administradora}/TipoFondos
def get_investment_funds_administrator_types(client: InvertirOnlineAPI, administrator=None):
    """Retrieve data for all investment funds administrator types."""
    return client._request('GET', f'Titulos/FCI/Administradoras/{administrator}/TipoFondos')

# GET /api/v2/Titulos/FCI/Administradoras/{administradora}/TipoFondos/{tipoFondo}
def get_investment_funds_administrator_type(client: InvertirOnlineAPI, administrator=None, fund_type=None):
    """Retrieve data for a specific investment funds administrator type."""
    return client._request('GET', f'Titulos/FCI/Administradoras/{administrator}/TipoFondos/{fund_type}')
