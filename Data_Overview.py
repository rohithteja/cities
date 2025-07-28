import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Filters')
st.set_page_config(
    page_title="Indian Cities Project",
    page_icon=":city_sunset:",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("# :city_sunset: Indian Cities Project")
st.markdown("--------")

cities = ['kohima', 'panaji', 'itanagar', 'gangtok', 'shilong', 'nalgonda', 'shimla', 'imphal', 'rourkela', 'siliguri',
  'durgapur', 'dewas', 'aizawl', 'haldia', 'sagar', 'jabalpur', 'thoothukkudi', 'shivamogga', 'kurnool', 
  'jalpaiguri', 'korba', 'alwar', 'silchar', 'udaipur', 'erode', 'muzaffarpur', 'ujjain', 'kolhapur', 
  'agartala', 'sangli-miraj-kupwad', 'gaya', 'nellore', 'jalgaon', 'bhilainagar', 'jhansi', 'mangaluru', 
  'patiala', 'amravati', 'dehradun', 'guntur', 'firozabad', 'tiruppur', 'chandigarh', 'cuttack', 'warangal', 
  'mysuru', 'jammu', 'srinagar', 'bhubaneswar', 'vijaywada', 'aligarh', 'jodhpur', 'hubli dharwad', 'kochi', 
  'solapur', 'tiruchirappalli', 'gurgaon', 'jalandhar', 'guwahati', 'amritsar', 'raipur', 'bareilly', 'kota', 
  'noida', 'rajkot', 'moradabad', 'aurangabad', 'ranchi', 'gwalior', 'jamshedpur', 'coimbatore', 'meerut', 
  'dhanbad', 'allahabad', 'madurai', 'nashik', 'ludhiana', 'faridabad', 'vadodara', 'varanashi', 'agra', 
  'thiruvananthapuram', 'vishakhapatnam', 'patna', 'ghaziabad', 'bhopal', 'nagpur', 'indore', 'kanpur', 
  'jaipur', 'lucknow', 'pune', 'surat', 'kolkata', 'hyderabad', 'chennai', 'ahmedabad', 'bengaluru', 'mumbai', 'delhi']

# Load the data
df = pd.read_csv(f'data/stats.csv')


types = ['All Cities', 'Top 15 Cities', 'Bottom 15 Cities']
years = [2021, 2022, 2023]
st.selectbox('Select Year', options=years, index=0, key='year')
# filter based on city selection
st.selectbox('Select Type', options=types, index=0, key='type')

# set default year in session state
if 'year' not in st.session_state:
    st.session_state.year = 2021

df = df[df['year'] == st.session_state.year]
if 'type' not in st.session_state:
    st.session_state.type = 'All Cities'
if st.session_state.type == 'All Cities':
    df_filter = df.copy()
if st.session_state.type == 'Top 15 Cities':
    df_filter = df.nlargest(15, 'co2_pc')
elif st.session_state.type == 'Bottom 15 Cities':
    df_filter = df.nsmallest(15, 'co2_pc')

st.markdown("### CO₂ Emissions by City in India")
st.markdown('''
* Number of cities: ''' + str(len(df_filter.city.unique())) + '''
* Size of markers = population of city
* Color of markers = CO₂ emissions per capita (in tons)
* Click on a marker to see more details (scroll below the interative map for plots and stats)
* Double click on the interactive map to reset the selection or click on other markers to see their details
* Colorbar midpoint is set to the median CO₂ emissions per capita
''')

# Compute the median CO₂ per capita
median_co2_pc = np.mean(df_filter["co2_pc"])

# Scale population for better size visibility
# pop_scaled = np.log1p(df_filter['population_2020'])
pop_scaled = np.sqrt(df_filter['population_2020'])
pop_scaled = 4 + 10 * (pop_scaled - pop_scaled.min()) / (pop_scaled.max() - pop_scaled.min())
df_filter['pop_scaled'] = pop_scaled

fig = px.scatter_map(
    df_filter.round(2),
    lat="lat",
    lon="lon",
    size="pop_scaled",
    size_max=15,
    color="co2_pc",
    color_continuous_scale="plasma",
    color_continuous_midpoint=median_co2_pc,
    range_color=[df_filter["co2_pc"].min(), df_filter["co2_pc"].quantile(0.97)],
    custom_data=["city", "population_2020"],
    zoom=4,
    height=800,
    map_style="carto-positron"  # still supported with MapLibre
)

# Keep text readable
fig.update_traces(textfont_color='black')

# Custom hovertemplate with actual population
fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>" +
                  "CO₂ Emissions: %{marker.color:.2f} tons per person<br>" +
                  "Population: %{customdata[1]:,}<br>" +
                  f"Year: {st.session_state.year}<extra></extra>"
)

# Title and margins
fig.update_layout(
    title=f"Year: {st.session_state.year}",
    margin={"r": 0, "t": 40, "l": 0, "b": 0}
)
 
# Colorbar title
fig.update_layout(coloraxis_colorbar=dict(
    title="CO₂ per Capita (tons/person)", 
    title_side="right",
    title_font=dict(size=14),
    tickfont=dict(size=12)
))

selected_points = st.plotly_chart(fig, use_container_width=True,on_select='rerun')

if selected_points is not None and len(selected_points['selection']['points']) > 0:
    selected_city = selected_points['selection']['points'][0]['customdata'][0]
    # empty space to avoid overlap with the map
    st.markdown("<br>" * 2, unsafe_allow_html=True)
    st.markdown(f"### 📍 Stats for {selected_city.title()}")
    city_data = df_filter[df_filter['city'] == selected_city]
    st.markdown(f"""
    • Population: {city_data['population_2020'].values[0]:,}
    """)

    st.markdown(f"#### CO2 emissions {st.session_state.year}")
    st.image("data/plots1/og/ts_co2_all_byyear/{year}/{city}.png".format(city=selected_city, year=st.session_state.year))

    if st.session_state.year == 2021 or st.session_state.year == 2022:
        st.markdown(f"#### Google Mobility {st.session_state.year}")
        # explanation for the image
        st.markdown("It shows the change in visits to places like transit stations, workplaces, and residential areas compared to a baseline period (in %)")
        st.image("data/google_mobility/{year}/{city}.png".format(city=selected_city, year=st.session_state.year))

    st.markdown("#### CO2 emissions (3 years)")
    st.image("data/plots1/og/ts_co2_all/{city}.png".format(city=selected_city))

    st.markdown(f"#### CO2 emissions fleet {st.session_state.year}")
    st.image("data/plots1/og/ts_co2_fleet_byyear/{year}/{city}.png".format(city=selected_city, year=st.session_state.year))

    st.markdown("#### CO2 emissions fleet (3 years)")
    st.image("data/plots1/og/ts_co2_fleet/{city}.png".format(city=selected_city))

    st.markdown("#### Fuel consumption car")
    st.image("data/plots1/og/ts_fuel_car/{city}.png".format(city=selected_city))

    st.markdown("#### Fuel consumption truck")
    st.image("data/plots1/og/ts_fuel_truck/{city}.png".format(city=selected_city))

    st.markdown("#### Vehicle count")
    st.image("data/plots1/og/ts_count/{city}.png".format(city=selected_city))

    st.markdown("#### Vehicle speed")
    st.image("data/plots1/og/ts_speed/{city}.png".format(city=selected_city))

    st.markdown("#### Maps")
    st.image("data/plots1/og/maps/{city}.png".format(city=selected_city))
