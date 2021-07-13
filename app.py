import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

@st.cache
def load_data():
    boxscores_df = pd.read_pickle('data/df_boxscores.pkl')
    return boxscores_df

data_load_state = st.text('Getting your precious data...')

df = load_data()

data_load_state.text("Don't worry buddy, we got your data! (using st.cache)")

"""
# My NFL Analysis App
"""

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

st.subheader('Total minus over/under')
hist_values = np.histogram(df[['total_minus_over', 'year']], bins=50)
st.line_chart(hist_values)

# year_to_filter = st.slider('year', 2000, 2021)
# filtered