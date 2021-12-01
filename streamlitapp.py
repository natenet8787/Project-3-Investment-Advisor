import streamlit as st
import pandas as pd

st.title('Invest With Us!')

st.header('Please select an investment oppurtunity')

option = st.selectbox('Investment',
    ('SPY portfolio', 'BTC portfolio'))
st.write('You Selected:', option)