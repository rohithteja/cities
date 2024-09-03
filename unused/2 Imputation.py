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

city = st.selectbox('City', sorted(['Kanpur','Guwahati']))
direction = 'F'

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

def toggle_images(category, button_key):
    if f'show_{category}' not in st.session_state:
        st.session_state[f'show_{category}'] = False
    if st.button(f'Show/Hide data for 2022 and 2023', key=button_key):
        st.session_state[f'show_{category}'] = not st.session_state[f'show_{category}']
    if st.session_state[f'show_{category}']:
        for year in [2022, 2023]:
            st.markdown(f'({year})')
            st.image(f'data/{city.lower()}/{year}/full_data/{direction}/{category}.png')

st.markdown('### Model Performance')
st.markdown('* Light GBM regression')
st.markdown('* Train\:Test = 80:20')
st.markdown('Metrics for different combinations')

path = f'data/impute/{city.lower()}/'
st.dataframe(pd.read_csv(path +'metrics.csv'))


st.markdown('### Data Quality')
st.markdown('Note: all images shown below correspond to traffic direction "F"')
st.markdown('#### Mean hourly count (2021)')
st.markdown('Original data')
st.image(path +'initial_data/2021/countcomparison.png')
st.markdown('Imputed data')
st.image(path +'full_data/2021/countcomparison.png')

# toggle_images('countcomparison', 'button_count')


st.markdown('---------------------')


st.markdown('#### Mean hourly speed (2021)')
st.markdown('Original data')
st.image(path +'initial_data/2021/speedcomparison.png')
st.markdown('Imputed data')
st.image(path +'full_data/2021/speedcomparison.png')
# toggle_images('speedcomparison', 'button_speed')
st.markdown('---------------------')

st.markdown('#### Daily traffic timeseries (2021)')
st.markdown('Original data')
st.image(path +'initial_data/2021/dailycomparisoncount.png')
st.markdown('Imputed data')
st.image(path +'full_data/2021/dailycomparisoncount.png')
# toggle_images('dailycomparisoncount', 'button_daily')
st.markdown('---------------------')

# st.markdown('### Missing Data')
# st.markdown('No gaps in data after imputation')
# st.markdown('Proportion of missing days in the data (2021)')
# st.markdown('Original data')
# st.image(path +'initial_data/2021/missingtimeseriespercent.png')
# st.markdown('Imputed data')
# st.image(path +'full_data/2021/missingtimeseriespercent.png')
# # toggle_images('missingtimeseriespercent', 'button_missing')
# st.markdown('---------------------')

# Load the HTML file
st.markdown('Original data')

html_file = open(path +'initial_data/2021/map.html', 'r', encoding='utf-8')
source_code = html_file.read() 
st.markdown('### Click on road for timeseries')
# Use the Streamlit components.html function to display the map
st.components.v1.html(source_code, height = 600, width = 900)
st.markdown('Imputed data')

html_file = open(path +'full_data/2021/map.html', 'r', encoding='utf-8')
source_code = html_file.read() 
st.markdown('### Click on road for timeseries')
# Use the Streamlit components.html function to display the map
st.components.v1.html(source_code, height = 600, width = 900)