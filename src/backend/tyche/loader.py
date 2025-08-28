
import yfinance as yf
import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

def load_data(tickers, start='2010-01-01', end=None):
    """Download or load cached Close price CSVs for tickers and return a price DataFrame."""
    frames = {}
    for t in tickers:
        csv_path = DATA_DIR / f"{t}.csv"
        if csv_path.exists():
    # try reading with Date column, fallback if missing
            try:
                 df = pd.read_csv(csv_path, parse_dates=['Date'], index_col='Date')
            except ValueError:
                df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        else:
            print(f"Downloading {t} from Yahoo Finance...")
            df = yf.download(t, start=start, end=end, progress=False)
            if df.empty:
                raise RuntimeError(f"No data for {t}")
            df.to_csv(csv_path)

        if 'Close' not in df.columns:
            raise RuntimeError(f"Downloaded data for {t} has no Close column.")
        frames[t] = df['Close']
        frames[t].name = t

    price = pd.concat(frames.values(), axis=1)
    price = price.sort_index().ffill().dropna(how='all')
    return price
