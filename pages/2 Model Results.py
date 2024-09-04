from calendar import c
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

cities = ['aizawl', 'bhopal', 'bhubaneswar', 'chandigarh', 'chennai', 'coimbatore', 'erode', 'faridabad', 'gangtok', 'guwahati', 'hubli dharwad', 'hyderabad', 'imphal', 'indore', 'jaipur', 'kanpur', 'kochi', 'kohima', 'kolkata', 'lucknow', 'madurai', 'mangaluru', 'meerut', 'mysuru', 'patna', 'pune', 'ranchi', 'rourkela', 'shilong', 'shivamogga', 'surat', 'tiruchirappalli', 'tiruppur', 'vadodara', 'varanashi', 'vijaywada', 'vishakhapatnam']

metricss = pd.read_csv('data/results/all_metrics.csv')
metrics = metricss.groupby(['city']).mean().reset_index().round(2)

st.markdown('### Metrics for different cities')
st.dataframe(metrics)

# Capitalize city names and sort them
sorted_cities = sorted([i.capitalize() for i in cities])

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


st.markdown('### Predictors')
st.markdown('ML model is trained to impute missing values in the dataset. Metrics calculated on 20\% of test data, to predict vehicle count and speed. ''')  
st.markdown('The model is trained on the following features:')
st.markdown('''```
            Temporal predictors:
            1. Hour
            2. Day
            3. Month
            4. Day of week
            5. Week of year
            6. Quarter
            7. Part of day (morning, afternoon, evening)''')

st.markdown('''```
            Spatial predictors: 
            1. Annual mean vehicle count/ speed
            2. Functional class of street (type of streets i.e., highway, small street etc)
            3. Speed limit of street
            4. Lane category of street''')

st.markdown('''```
            Model = Light GBM regression''')

st.markdown(f'#### R2 score = {metrics[metrics["city"] == st.session_state.selected_city.lower()]["R2"].values[0]}')


st.markdown('### SHAP Importance')

shap = pd.read_csv('data/results/all_shap.csv')
shap.columns = ['variables', 'value', 'city','year','vehicle','direction','variable']
shap = shap[shap['city'] == st.session_state.selected_city.lower()].groupby(['city','variables']).mean().reset_index()
shap.value = shap.value * 100
# Desired order of the variables
order = ['hour', 'day', 'month', 'day_of_week', 'week_of_year', 'quarter', 'part_of_day', 'mean_variable_annual', 'FUNC_CLASS', 'LANE_CAT', 'SPEED_CAT']
shap_sorted = shap.set_index('variables').reindex(order).reset_index()[['variables','value']]

category = {'hour':'Temporal', 'day':'Temporal', 'month':'Temporal', 'day_of_week':'Temporal', 'week_of_year':'Temporal', 'quarter':'Temporal', 'part_of_day':'Temporal', 'mean_variable_annual':'Spatial', 'FUNC_CLASS':'Spatial', 'LANE_CAT':'Spatial', 'SPEED_CAT':'Spatial'}
shap_sorted['category'] = shap_sorted['variables'].map(category)
color_scale = alt.Scale(domain=['Temporal', 'Spatial'], range=['blue', 'red'])

# Create the chart
chart = alt.Chart(shap_sorted[['variables', 'value', 'category']]).mark_bar().encode(
    x=alt.X('variables', sort=None, title="Predictors"),
    y=alt.Y('value', title="SHAP Importance (%)"),
    color=alt.Color('category:N', scale=color_scale, title='Category')
).properties(
    width=800,  # Adjust width if needed
    height=400  # Adjust height if needed
)

# Display the chart
st.altair_chart(chart, use_container_width=True)

metrics_pie = metrics[metrics['city'] == st.session_state.selected_city.lower()][['temporal (%)', 'spatial (%)']].iloc[0].reset_index()
metrics_pie.columns = ['variables', 'value']
metrics_pie['category'] = ['Temporal', 'Spatial']

# Create a pie chart
st.markdown('### Predictor Influence')

chart = alt.Chart(metrics_pie[['variables', 'value', 'category']]).mark_bar().encode(
    x=alt.X('variables', sort=None, title="Predictor Categories"),
    y=alt.Y('value', title="SHAP Importance (%)"),
    color=alt.Color('category:N', scale=color_scale, title='Category')
).properties(
    width=800,  # Adjust width if needed
    height=400  # Adjust height if needed
)

# Display the chart
st.altair_chart(chart, use_container_width=True)
