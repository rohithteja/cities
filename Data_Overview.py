import streamlit as st
import pandas as pd
import numpy as np
import pickle



st.sidebar.title('Filters')

st.markdown("# Indian Cities Project")
st.markdown("--------")


city = st.selectbox('City', ['Chandigarh','Kohima'])

st.markdown('### Data Quality')
st.markdown('Figure shows the number of data points available for number of hours in the dataset (24 hours means the 24 measurements are available for that road)')

st.image(f'data/{city.lower()}/hoursreported.png')

st.markdown('### Vehicle Count')
st.image(f'data/{city.lower()}/meancounthourly.png')
st.image(f'data/{city.lower()}/comparisoncount.png')
more_details = st.checkbox('Show Individual Plots',key='count')
if more_details:
    st.image(f'data/{city.lower()}/carcount.png')
    st.image(f'data/{city.lower()}/truckcount.png')


st.markdown('### Vehicle Speed')
st.markdown('Daily Mean(Mean of all vehicles in all roads)')
st.image(f'data/{city.lower()}/comparisonspeed.png')
st.image(f'data/{city.lower()}/speedhist.png')
more_details2 = st.checkbox('Show Individual Plots',key='speed')
if more_details2:
    st.image(f'data/{city.lower()}/speedcar.png')
    st.image(f'data/{city.lower()}/speedtruck.png')
    
st.markdown('### Vehicle Count Map')
st.image(f'data/{city.lower()}/countmap.png')

st.markdown('### Vehicle Speed Map')
st.image(f'data/{city.lower()}/speedmap.png')