# finargy

Financial data analysis and market API connector for invertironline

## Description

`finargy` is a Python package that provides tools for financial data analysis and API integration with the InvertirOnline trading platform. It allows you to fetch market data, manage portfolios, and analyze investments.

## Installation

1. Clone the repository:
```sh
git clone https://github.com/your-username/finargy.git
cd finargy
```

2. Create and activate virtual environment
- Linux:
```sh
python3 -m venv .venv
source .venv/bin/activate
```
- Windows:
```bat
python -m venv .venv
.venv\Scripts\activate
```

3. Install requirements and finargy package from source:
```sh
pip install -r requirements.txt
pip install -e .
```
Remove the `-e` flag if you don't want to install the package in editable mode.

## Configuration

1. Create a new file named `.env` in the root directory of the project.
2. Add the following environment variables to the `.env` file:

```sh
USER=your_username
PASSWORD=your_password
```

## Usage

### API Client

```python
from finargy.api.client import InvertirOnlineAPI

# Initialize client
client = InvertirOnlineAPI() 

```

### Market Data

```python
from finargy.api.market_data.symbol_data import get_symbol_history
import datetime

# Get historical data for a symbol
data = get_symbol_history(
    client,
    symbol="AAPL",
    date_start=datetime.datetime(2024, 1, 1),
    date_end=datetime.datetime.now()
)

```