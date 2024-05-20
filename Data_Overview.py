import streamlit as st
import pandas as pd
import numpy as np
import pickle
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium



st.sidebar.title('Filters')

st.markdown("# Indian Cities Project")
st.markdown("--------")

geolocator = Nominatim(user_agent="city_locator")

city = st.selectbox('City', ['Kochi','Kohima','Gangtok'])

def get_city_coordinates(city_name):
    location = geolocator.geocode(city_name)
    if location:
        return [location.latitude, location.longitude]
    else:
        return None

coordinates = get_city_coordinates(city)

if coordinates:
    m = folium.Map(location=coordinates, zoom_start=5)
    folium.Marker(location=coordinates, popup=city).add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.error(f"Could not find coordinates for {city}.")

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


