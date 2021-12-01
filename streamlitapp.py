import streamlit as st
import pandas as pd
from PIL import Image

st.title('Invest With Us!')

st.header('Please select an investment oppurtunity')

option = st.selectbox('Investment',
    ('SPY portfolio', 'BTC portfolio'))
st.write('You Selected:', option)

if 'SPY portfolio' in option:
    spy = st.image("https://github.com/MoustafaMous/Project-3/blob/main/Images/returnsSPY.PNG?raw=true")
if 'BTC portfolio' in option:
    btc = st.image("https://github.com/MoustafaMous/Project-3/blob/main/Images/returnsBTC.PNG?raw=true")