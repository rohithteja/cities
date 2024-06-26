import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium
import pgeocode

st.sidebar.title('Filters')

st.markdown("# Indian Cities Project")
st.markdown("--------")


city = st.selectbox('City', sorted(['Mumbai','Hyderabad', 'Chennai','Chandigarh','Kochi','Kohima','Gangtok', 'Faridabad', 'Coimbatore']))
# city = st.selectbox('City', sorted(['Mumbai','Hyderabad', 'Chennai','Chandigarh','Kochi','Kohima','Gangtok', 'Faridabad', 'Coimbatore','Bengaluru']))

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
            st.image(f'data/{city.lower()}/{year}/{category}.png')

st.markdown('### Data Quality')
st.markdown('#### Mean hourly count (2021)')
st.image(f'data/{city.lower()}/2021/countcomparison.png')
toggle_images('countcomparison', 'button_count')


st.markdown('---------------------')


st.markdown('#### Mean hourly speed (2021)')
st.image(f'data/{city.lower()}/2021/speedcomparison.png')
toggle_images('speedcomparison', 'button_speed')
st.markdown('---------------------')

st.markdown('#### Daily traffic timeseries (2021)')
st.image(f'data/{city.lower()}/2021/dailycomparisoncount.png')
toggle_images('dailycomparisoncount', 'button_daily')
st.markdown('---------------------')

st.markdown('### Missing Data')
st.markdown('Proportion of missing days in the data (2021)')
st.image(f'data/{city.lower()}/2021/missingtimeseriespercent.png')
toggle_images('missingtimeseriespercent', 'button_missing')
st.markdown('---------------------')

# Load the HTML file
html_file = open(f'data/{city.lower()}/2021/map.html', 'r', encoding='utf-8')
source_code = html_file.read() 
st.markdown('### Click on road for timeseries')
# Use the Streamlit components.html function to display the map
st.components.v1.html(source_code, height = 600, width = 900)

