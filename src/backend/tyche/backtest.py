
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def run_backtest_and_report(price, weights, out_folder='reports', init_cash=100000, fee=0.0005):
    """Simple daily rebalanced backtest:
    - price: DataFrame index x assets of Close prices
    - weights: DataFrame (same shape) of target weights each day
    - fee: proportional round-trip fee applied on turnover (approx)
    """
    out = Path(out_folder); out.mkdir(parents=True, exist_ok=True)
    # align
    price = price.reindex(weights.index).ffill()
    # compute daily returns per asset
    ret = price.pct_change().fillna(0)
    assets = price.columns.tolist()
    # compute portfolio returns: prev_weights * asset returns
    # we'll assume instant rebalance at close with turnover cost
    prev_w = pd.DataFrame(0.0, index=weights.index, columns=assets)
    cash = init_cash
    equity = []
    port_value = init_cash
    prev_weights = np.zeros(len(assets))
    for i, date in enumerate(weights.index):
        target_w = weights.iloc[i].fillna(0).values
        if i==0:
            # first day: allocate initial cash according to target weights
            prev_weights = target_w
            port_value = init_cash
            equity.append(port_value)
            continue
        # asset returns from yesterday to today (use ret at date)
        r = ret.iloc[i].values
        # portfolio return before rebalancing
        port_value = port_value * (1 + np.dot(prev_weights, r))
        # turnover cost: sum |new - old| * fee * port_value  (approx)
        turnover = np.sum(np.abs(target_w - prev_weights))
        cost = turnover * fee * port_value
        port_value = port_value - cost
        equity.append(port_value)
        prev_weights = target_w
    eq = pd.Series(equity, index=weights.index)
    df = pd.DataFrame({'equity': eq})
    # simple stats
    df['ret'] = df['equity'].pct_change().fillna(0)
    total_return = df['equity'].iloc[-1] / init_cash - 1.0
    ann_ret = (1 + total_return) ** (252.0 / len(df)) - 1 if len(df)>0 else 0.0
    dd = (df['equity'] / df['equity'].cummax() - 1).min()
    stats = {
        'init_cash': init_cash,
        'final_value': float(df['equity'].iloc[-1]),
        'total_return': float(total_return),
        'ann_return_approx': float(ann_ret),
        'max_drawdown': float(dd)
    }
    # save outputs
    df.to_csv(out / 'equity_curve.csv')
    with open(out / 'summary.txt', 'w') as f:
        for k,v in stats.items():
            f.write(f"{k}: {v}\n")
    # plot equity curve
    plt.figure(figsize=(8,4))
    plt.plot(df.index, df['equity'])
    plt.title('Tyche - Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out / 'equity_curve.png', dpi=150)
    plt.close()
    return df
