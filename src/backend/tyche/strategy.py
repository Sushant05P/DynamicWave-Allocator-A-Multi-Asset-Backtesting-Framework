
import numpy as np
import pandas as pd

def momentum_signal(price_df, lookback=63):
    """Return simple momentum score: pct change over lookback days."""
    return price_df.pct_change(lookback)

def to_weights_softmax(signal_df):
    """Convert raw signal (index x assets) to weights per row using softmax."""
    sig = signal_df.fillna(0).copy()
    # subtract row max for numerical stability
    arr = sig.values
    ex = np.exp(arr - np.nanmax(arr, axis=1, keepdims=True))
    denom = np.nansum(ex, axis=1, keepdims=True)
    denom[denom==0] = 1.0
    weights = ex / denom
    wdf = pd.DataFrame(weights, index=sig.index, columns=sig.columns)
    return wdf
