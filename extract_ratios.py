import re
import pandas as pd

# Sample page text with multiple ticker blocks (same as before)

# BALANZ INFO FROM 24/01/2024
page_text = """
¿Cuáles son los CEDEARs con cambios en sus ratios?

3M COMPANY
Ticker: MMM

Ratio de conversión anterior: 5:1

Ratio de conversión actualizado: 10:1

ADECOAGRO S.A.
Ticker: ADGO

Ratio de conversión anterior: 1:2

Ratio de conversión actualizado: 1:1

ADOBE INC.
Ticker: ADBE

Ratio de conversión anterior: 22:1

Ratio de conversión actualizado: 44:1

AGNICO EAGLE MINES LIMITED
Ticker: AEM

Ratio de conversión anterior: 3:1

Ratio de conversión actualizado: 6:1

AMGEN INC. 
Ticker: AMGN

Ratio de conversión anterior: 10:1

Ratio de conversión actualizado: 30:1

APPLE INC.
Ticker: AAPL

Ratio de conversión anterior: 10:1

Ratio de conversión actualizado: 20:1

BANK OF AMERICA CORPORATION
Ticker: BAC

Ratio de conversión anterior: 2:1

Ratio de conversión actualizado: 4:1

BARRICK GOLD CORPORATION
Ticker: GOLD

Ratio de conversión anterior: 1:1

Ratio de conversión actualizado: 2:1

BIOCERES CROP  SOLUTIONS CORP.
Ticker: BIOX

Ratio de conversión anterior: 1:2

Ratio de conversión actualizado: 1:1

CHEVRON CORP.
Ticker: CVX

Ratio de conversión anterior: 8:1

Ratio de conversión actualizado: 16:1

ELI LILLY AND COMPANY
Ticker: LLY

Ratio de conversión anterior: 8:1

Ratio de conversión actualizado: 56:1

EXXON MOBIL CORPORATION
Ticker: XOM

Ratio de conversión anterior: 5:1

Ratio de conversión actualizado: 10:1

FIRST SOLAR INC.
Ticker: FSLR

Ratio de conversión anterior: 3:1

Ratio de conversión actualizado: 18:1

INTERNATIONAL BUSINESS MACHINES CORPORATION (IBM)
Ticker: IBM

Ratio de conversión anterior: 5:1

Ratio de conversión actualizado: 15:1

JD.COM, INC
Ticker: JD

Ratio de conversión anterior: 2:1

Ratio de conversión actualizado: 4:1

JPMORGAN CHASE & CO
Ticker: JPM

Ratio de conversión anterior: 5:1

Ratio de conversión actualizado: 15:1

MERCADO LIBRE INC.
Ticker: MELI

Ratio de conversión anterior: 60:1

Ratio de conversión actualizado: 120:1

NETFLIX INC
Ticker: NFLX

Ratio de conversión anterior: 16:1

Ratio de conversión actualizado: 48:1

PEPSICO INC.
Ticker: PEP

Ratio de conversión anterior: 6:1

Ratio de conversión actualizado: 18:1

PFIZER INC.
Ticker: PFE

Ratio de conversión anterior: 2:1

Ratio de conversión actualizado: 4:1

PROCTER & GAMBLE (P&G)
Ticker: PG

Ratio de conversión anterior: 5:1

Ratio de conversión actualizado: 15:1

RIO TINTO PLC
Ticker: RIO

Ratio de conversión anterior: 4:1

Ratio de conversión actualizado: 8:1

SONY CORP.
Ticker: SONY

Ratio de conversión anterior: 4:1

Ratio de conversión actualizado: 8:1

STARBUCKS CORP.
Ticker: SBUX

Ratio de conversión anterior: 4:1

Ratio de conversión actualizado: 12:1

TERNIUM S.A.
Ticker: TXR

Ratio de conversión anterior: 2:1

Ratio de conversión actualizado: 4:1

THE BOEING COMPANY
Ticker: BA

Ratio de conversión anterior: 6:1

Ratio de conversión actualizado: 24:1

TOYOTA MOTOR CORP.
Ticker: TM

Ratio de conversión anterior: 5:1

Ratio de conversión actualizado: 15:1

VERIZON COMMUNICATIONS INC.
Ticker: VZ

Ratio de conversión anterior: 2:1

Ratio de conversión actualizado: 4:1

VISTA ENERGY S.A.B. de CV (ADS)
Ticker: VIST

Ratio de conversión anterior: 1:1

Ratio de conversión actualizado: 3:1

WALMART INC.
​​​​Ticker: WMT

Ratio de conversión anterior: 6:1

Ratio de conversión actualizado: 18:1
"""

# Step 1: Split the text into blocks
blocks = re.split(r"(Ticker:)", page_text)
tickers = ["".join(blocks[i : i + 2]).strip() for i in range(1, len(blocks), 2)]


# Step 2: Function to extract data from each block
def extract_ticker_info(block):
    # Extract the Ticker
    ticker_match = re.search(r"Ticker:\s+(\w+)", block)
    ticker = ticker_match.group(1) if ticker_match else None

    # Extract the previous ratio
    previous_ratio_match = re.search(
        r"Ratio de conversión anterior:\s+(\d+):(\d+)", block
    )
    if previous_ratio_match:
        prev_numerator = int(previous_ratio_match.group(1))
        prev_denominator = int(previous_ratio_match.group(2))
        previous_ratio = prev_numerator / prev_denominator
    else:
        previous_ratio = None

    # Extract the new ratio
    new_ratio_match = re.search(
        r"Ratio de conversión actualizado:\s+(\d+):(\d+)", block
    )
    if new_ratio_match:
        new_numerator = int(new_ratio_match.group(1))
        new_denominator = int(new_ratio_match.group(2))
        new_ratio = new_numerator / new_denominator
    else:
        new_ratio = None

    # Calculate the ratio variation (new_ratio / previous_ratio)
    ratio_variation = (
        new_ratio / previous_ratio if previous_ratio and new_ratio else None
    )

    # Return the extracted information in a structured format (dictionary)
    return {
        "Ticker": ticker,
        "Previous Ratio": (
            f"{prev_numerator}:{prev_denominator}" if previous_ratio else None
        ),
        "New Ratio": f"{new_numerator}:{new_denominator}" if new_ratio else None,
        "Ratio Variation": ratio_variation,
    }


# Step 3: Extract data for all tickers
data = [extract_ticker_info(ticker_block) for ticker_block in tickers]

# Step 4: Create a DataFrame
df = pd.DataFrame(data)
# save to csv, add index=False to avoid saving the index column date column today
date = pd.Timestamp.today().date()

date = "2024-01-24"

df["date"] = pd.to_datetime(date)


df.to_csv(f"cedears/cedear_ratios_{date}.csv", index=False)
