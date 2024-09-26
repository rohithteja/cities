from calendar import c
from hmac import new
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium
import pgeocode
import os
import altair as alt
import matplotlib.pyplot as plt

st.sidebar.title('City Selection')

st.markdown("# Indian Cities Project")
st.markdown("--------")


metricss = pd.read_csv('data/results/all_cf.csv').round(2)
metrics = metricss.groupby(['city']).mean().reset_index().round(2)

cities = metrics['city'].tolist()

st.markdown('### Correction Factor for different cities')
st.dataframe(metricss)

st.markdown('Correction factor is multipled to the gps vehicle count to obtain the true vehicle count.')
st.markdown('''```
            Variables:
            1. gpscount = mean hourly gps vehicle count
            2. gpsspeed = mean hourly gps vehicle speed
            3. correction_factor = correction factor
            4. new_total_count = gpscount * correction_factor
            5. city_consump = annual city fuel consumption''')

# correction factor comparison for all cities
st.markdown('### Correction Factor Comparison')
# scatter plot
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
# scatter plot
ax.scatter(metricss['gpscount'], metricss['correction_factor'])
ax.set_xlabel('GPS Count')
ax.set_ylabel('Correction Factor')
# names
for i, txt in enumerate(metricss['city']):
    ax.annotate(txt, (metricss['gpscount'][i], metricss['correction_factor'][i]))
st.pyplot(fig)

# Capitalize city names and sort them
sorted_cities = sorted([i.capitalize() for i in cities])

# check if the file exists
new_sorted_cities = []
for city in sorted_cities:
    if os.path.exists(f'data/results/cities_overview/{city.lower()}/2021/countcomparison.png'):
        new_sorted_cities.append(city)

sorted_cities = new_sorted_cities

# Grid layout for clickable boxes
num_columns = 2  # Number of columns in the grid

# Initialize session state for selected city
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = 'Aizawl'

# Create the grid
for i in range(0, len(sorted_cities), num_columns):
    cols = st.sidebar.columns(num_columns)
    for j, col in enumerate(cols):
        if i + j < len(sorted_cities):
            if col.button(sorted_cities[i + j]):
                st.session_state.selected_city = sorted_cities[i + j]

# Display the selected city
if st.session_state.selected_city:
    st.write(f'### You selected: {st.session_state.selected_city}')

    def get_city_coordinates(city_name):
        if not city_name:
            return None
        nomi = pgeocode.Nominatim('IN')  # 'IN' for India, change the country code as needed
        if city_name.lower() == 'hubli dharwad':
            location = nomi.query_location('Hubli')
            location = location[location.county_name == 'Dharwad'].iloc[0]
        elif city_name.lower() == 'imphal':
            location = nomi.query_location('Imphal')
            location = location[location.county_name.str.contains('Imphal')].iloc[0]
        elif city_name.lower() == 'kanpur':
            location = nomi.query_location('Kanpur')
            location = location[location.county_name.str.contains('Kanpur')].iloc[1]
        elif city_name.lower() == 'mangaluru':
            location = nomi.query_location('Mangalore')
            location = location[location.community_name.str.contains('Mangalore')].iloc[0]
        elif city_name.lower() == 'patna':
            return [25.5941, 85.1376]
        elif city_name.lower() == 'rourkela':
            return [22.2604, 84.8536]
        elif city_name.lower() == 'shilong':
            return [25.5788, 91.8933]
        elif city_name.lower() == 'shivamogga':
            return [13.9299, 75.5681]
        elif city_name.lower() == 'tiruppur':
            return [11.1085, 77.3411]
        elif city_name.lower() == 'varanashi':
            return [25.3176, 82.9739]
        elif city_name.lower() == 'vijaywada':
            return [16.5062, 80.6480]
        elif city_name.lower() == 'vishakhapatnam':
            return [17.6868, 83.2185]
        else:
            location = nomi.query_location(city_name)
            if location.empty:
                return None
            try:
                location = location[location.county_name.str.lower() == city_name.lower()].iloc[0]
            except:
                try:
                    location = location[location.community_name.str.lower() == city_name.lower()].iloc[0]
                except:
                    return None
        return [location.latitude, location.longitude]
    
    # Get coordinates
    coordinates = get_city_coordinates(st.session_state.selected_city)

    if coordinates:
        m = folium.Map(location=coordinates, zoom_start=5)
        folium.Marker(location=coordinates, popup=st.session_state.selected_city).add_to(m)
        st_folium(m, width=700, height=500)
    else:
        st.error(f"Could not find coordinates for {st.session_state.selected_city}.")

# make a plot to show the initial gps count and the corrected count
initial_gps = metricss[metricss['city'] == st.session_state.selected_city.lower()]['gpscount'].values[0]
corrected_count = metricss[metricss['city'] == st.session_state.selected_city.lower()]['new_total_count'].values[0]

st.markdown(f'#### Correction Factor = {metricss[metricss["city"] == st.session_state.selected_city.lower()]["correction_factor"].values[0]}')
# bar plot in % 
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
# stacked bar horizontal
ax.barh(['Initial GPS Count'], [initial_gps], label='Initial GPS Count')
ax.barh(['Corrected Count'], [corrected_count], label='Corrected Count')
ax.set_xlabel('Count')
ax.set_title('Initial GPS Count vs Corrected Count')
ax.legend()
st.pyplot(fig)

st.markdown('---------------------')
st.markdown('The following analysis is done on original gps data + imputed data (correction factor not included).')
# images 
city = st.session_state.selected_city
st.markdown('#### Mean hourly count (2021)')
st.image(f'data/results/cities_overview/{city.lower()}/2021/countcomparison.png')
st.markdown('---------------------')

st.markdown('#### Mean hourly speed (2021)')
st.image(f'data/results/cities_overview/{city.lower()}/2021/speedcomparison.png')
st.markdown('---------------------')

st.markdown('#### Daily traffic timeseries (2021)')
st.image(f'data/results/cities_overview/{city.lower()}/2021/dailycomparisoncount.png')
st.markdown('---------------------')

st.markdown('### Mean Hourly Count Map (2021)')
st.markdown('Mean hourly count of vehicles in the city')
st.image(f'data/results/cities_overview/{city.lower()}/2021/countmap.png')
st.markdown('---------------------')

st.markdown('### Mean Hourly Speed Map (2021)')
st.markdown('Mean hourly speed of vehicles in the city')
st.image(f'data/results/cities_overview/{city.lower()}/2021/speedmap.png')
