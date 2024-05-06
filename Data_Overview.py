import streamlit as st
import pandas as pd
import numpy as np
import pickle



st.sidebar.title('Filters')

st.markdown("# Indian Cities Project")
st.markdown("--------")


st.markdown('## Data Overview')

city = st.selectbox('City', ['Kohima','Delhi','Mumbai'])

st.markdown('### Vehicle Count')
st.markdown('Daily Mean(Sum of all vehicles in all roads)')
st.image(f'data/{city}/comparisoncount.png')
more_details = st.checkbox('Show Individual Plots',key='count')
if more_details:
    st.image(f'data/{city}/passengercount.png')
    st.image(f'data/{city}/truckcount.png')


st.markdown('### Vehicle Speed')
st.markdown('Daily Mean(Mean of all vehicles in all roads)')
st.image(f'data/{city}/comparisonspeed.png')
more_details2 = st.checkbox('Show Individual Plots',key='speed')
if more_details2:
    st.image(f'data/{city}/speedpassenger.png')
    st.image(f'data/{city}/speedtruck.png')