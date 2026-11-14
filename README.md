# finargy

Financial data analysis and market API connector for invertironline

## Description

`finargy` is a Python package that provides tools for financial data analysis and API integration with the InvertirOnline trading platform. It allows you to fetch market data, manage portfolios, and analyze investments.

## Planning docs

Durable documentation (product specs and ADRs) lives in `docs/`; execution
planning (epics, features, tasks) lives in `planning/`. Work flows
`product-spec → epic → task`, each a markdown file with YAML frontmatter. Start at
[`docs/README.md`](docs/README.md) and [`planning/README.md`](planning/README.md);
agents should follow [`AGENTS.md`](AGENTS.md).

## Installation

1. Clone the repository:
```sh
git clone https://github.com/selewaut/finargy.git
cd finargy
```

2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already.

3. Create the virtual environment and install finargy in editable mode with its development dependencies:
```sh
uv sync --extra dev
```
This creates `.venv` using the Python version pinned in `.python-version` and installs the locked dependencies from `uv.lock`.

4. Activate the virtual environment (optional, `uv run <command>` works without activation):
- Linux/macOS:
```sh
source .venv/bin/activate
```
- Windows:
```bat
.venv\Scripts\activate
```

To add or update a dependency, use `uv add <package>` (or `uv add --dev <package>`). This updates `pyproject.toml` and `uv.lock` automatically.

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