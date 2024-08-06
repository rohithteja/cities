import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium
import pgeocode
import os

st.sidebar.title('Filters')

st.markdown("# Indian Cities Project")
st.markdown("--------")

city = st.selectbox('City', sorted(['Kanpur','Guwahati','Bhopal','Hyderabad','Coimbatore','Kohima']))
vehicle = st.selectbox('Vehicle', ['CAR','TRUCK'])
variable = st.selectbox('Variable', ['COUNT','MEAN'],help='COUNT: Vehicle count, MEAN: Vehicle speed')
direction = 'F'
year = '2021'
variable_renamed = 'Count' if variable == 'COUNT' else 'Speed'

def get_city_coordinates(city_name):
    nomi = pgeocode.Nominatim('IN')  # 'IN' for India, change the country code as needed
    location = nomi.query_location(city_name)
    location = location[location.community_name==city_name.capitalize()].iloc[0]    
    if location.empty:
        return None
    else:
        return [location.latitude, location.longitude]
    
# Get coordinates
coordinates = get_city_coordinates(city)

if coordinates:
    m = folium.Map(location=coordinates, zoom_start=5)
    folium.Marker(location=coordinates, popup=city).add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.error(f"Could not find coordinates for {city}.")

path = f'data/variability/{city.lower()}/{year}'

st.markdown('''Temporal predictors:
1. Hour
2. Day
3. Month
4. Day of week
5. Week of year
6. Quarter
7. Part of day (morning, afternoon, evening)''')
st.markdown('''Spatial predictors:
1. Annual mean vehicle count/ speed (binned into 4 classes)
2. Functional class of street (type of streets i.e., highway, small street etc)
3. Speed limit of street
4. Lane category of street''')

st.markdown(f'### {vehicle} {variable_renamed} Variability with predictors')
st.markdown('Mean variation of different predictors with respect to the variable')
st.image(f'{path}/{vehicle}_{direction}_{variable}_variability.png')

st.markdown('### Distribution')
st.markdown('Histogram of the predictor values')
st.image(f'{path}/{vehicle}_{direction}_{variable}_distribution.png')

