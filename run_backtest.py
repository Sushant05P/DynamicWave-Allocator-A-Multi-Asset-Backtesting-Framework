
from src.backend.tyche.loader import load_data
from src.backend.tyche.strategy import momentum_signal, to_weights_softmax
from src.backend.tyche.backtest import run_backtest_and_report
import pandas as pd

TICKERS = ['SPY', 'TLT', 'GC=F', 'BTC-USD']  # equities, bonds, gold, crypto

if __name__ == '__main__':
    print('Loading price data... (will cache to data/)')
    price = load_data(TICKERS, start='2015-01-01', end=None)
    print('Computing signals...')
    sig = momentum_signal(price, lookback=63)
    weights = to_weights_softmax(sig)
    print('Running backtest...')
    pf = run_backtest_and_report(price, weights, out_folder='reports', init_cash=100000)
    # pf is a DataFrame with equity curve and returns
    print('Done. Reports saved to reports/.')
