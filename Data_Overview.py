import streamlit as st
import pandas as pd
import numpy as np
import pickle



st.sidebar.title('Filters')

st.markdown("# Indian Cities Project")
st.markdown("--------")


city = st.selectbox('City', ['Kochi','Chandigarh','Kohima'])

st.markdown('### Data Quality')
st.markdown('Mean hourly count (2021-23)')
st.image(f'data/{city.lower()}/countcomparison.png')
st.markdown('Mean hourly speed (2021-23)')
st.image(f'data/{city.lower()}/speedcomparison.png')

st.markdown('Count speed correlation (2021-23)')

st.image(f'data/{city.lower()}/countvsspeed.png')

st.image(f'data/{city.lower()}/dailycomparisoncount.png')


st.image(f'data/{city.lower()}/hourlycomparisoncount.png')

st.markdown('### Missing Data')

st.markdown('Proportion of missing days in the data (2021)')

st.image(f'data/{city.lower()}/2021missingtimeseriespercent.png')

st.markdown('Time series of a few roads in the city (scatter plot to show the availability of the data)')
st.image(f'data/{city.lower()}/id1.png')
st.image(f'data/{city.lower()}/id2.png')
st.image(f'data/{city.lower()}/id3.png')
st.image(f'data/{city.lower()}/id4.png')

st.markdown('Criteria = Percent of roads having data > x% of days in the year and > y% of hours in a day')
st.image(f'data/{city.lower()}/2021matrix_missing.png')
st.image(f'data/{city.lower()}/2022matrix_missing.png')
st.image(f'data/{city.lower()}/2023matrix_missing.png')


