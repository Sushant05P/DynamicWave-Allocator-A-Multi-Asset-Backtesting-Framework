
import streamlit as st
from PIL import Image
import pandas as pd
import os

st.set_page_config(page_title='Tyche Backtest', layout='wide')
st.title('DynamicWave Allocator')

if not os.path.exists('reports/equity_curve.png'):
    st.warning('No reports found. Run `python run_backtest.py` first.')
else:
    st.image('reports/equity_curve.png', use_column_width=True)
    if os.path.exists('reports/equity_curve.csv'):
        df = pd.read_csv('reports/equity_curve.csv', index_col=0, parse_dates=True)
        st.subheader('Equity Curve (sample)')
        st.line_chart(df['equity'].rename('Equity'))
        st.write('Summary:')
        if os.path.exists('reports/summary.txt'):
            with open('reports/summary.txt') as f:
                txt = f.read()
            st.text(txt)
