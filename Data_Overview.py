import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Filters')

st.markdown("# Indian Cities Project")
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
df = pd.read_csv(f'data/df_stats_streamlit.csv')
df['vkt_pc'] = df['vkt'] / df['population_2020']
df['consumption_pc'] = df['consumption'] / df['population_2020']
years = [2021, 2022, 2023]

types = ['All Cities', 'Top 15 Cities', 'Bottom 15 Cities']
st.selectbox('Select Year', options=years, index=0, key='year')
# filter based on city selection
st.selectbox('Select Type', options=types, index=0, key='type')

# set default year in session state
if 'year' not in st.session_state:
    st.session_state.year = 2021
if 'type' not in st.session_state:
    st.session_state.type = 'All Cities'
df_filter = df[df.year == st.session_state.year].groupby(['city', 'vehicle']).sum().reset_index()
if st.session_state.type == 'Top 15 Cities':
    df_filter = df_filter.nlargest(15, 'co2_pc')
elif st.session_state.type == 'Bottom 15 Cities':
    df_filter = df_filter.nsmallest(15, 'co2_pc')

st.markdown("### CO₂ Emissions by City in India")
st.markdown('''
* Number of cities: ''' + str(len(df_filter.city.unique())) + '''
* Size of markers = population of city
* Color of markers = CO₂ emissions per capita (in tons)
* Click on a marker to see more details (below the map)
* Colorbar midpoint is set to the median CO₂ emissions per capita
''')

# Compute the median CO₂ per capita
median_co2_pc = np.median(df_filter["co2_pc"])

# Scale population for better size visibility
pop_scaled = np.log1p(df_filter['population_2020'])
pop_scaled = 5 + 10 * (pop_scaled - pop_scaled.min()) / (pop_scaled.max() - pop_scaled.min())
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
    range_color=[df_filter["co2_pc"].min(), df_filter["co2_pc"].max()],
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
    title="CO₂ Emissions (tons per person)",
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

    st.markdown("#### CO2 emissions timeseries")
    st.image("data/timeseries/ts_co2/{city}.png".format(city=selected_city))

    st.markdown("#### Vehicle count timeseries")
    st.image("data/timeseries/ts_count/{city}.png".format(city=selected_city))

    st.markdown(f"#### CO2 emission maps: {selected_city.title()}")
    st.image("data/timeseries/maps/{city}.png".format(city=selected_city))

    st.markdown("Plots below show the values for the selected city over the years and compare them with the mean values for all cities.")

    st.markdown("### CO₂ Emissions Over Years")
    mean_df = df.groupby(['year', 'vehicle'])['co2_pc'].mean().reset_index()
    mean_df.year = mean_df.year.astype(str)
    plt.figure(figsize=(10,5))
    city_df = df[df['city'] == selected_city]
    sns.barplot(data=city_df, x='year', y='co2_pc', hue='vehicle', edgecolor='black')
    sns.lineplot(data=mean_df, x='year', y='co2_pc', hue='vehicle', 
                linewidth=2, linestyle='--', legend=False)
    for vehicle in mean_df['vehicle'].unique():
        vehicle_data = mean_df[mean_df['vehicle'] == vehicle]
        for i in range(len(vehicle_data)):
            plt.text(x=vehicle_data['year'].iloc[i], y=vehicle_data['co2_pc'].iloc[i],
                    s=f"mean {vehicle}", ha='center', va='bottom')

    plt.title(f'CO₂ Emissions Over Years - {selected_city.title()}')
    plt.xlabel('Year')
    plt.ylabel('CO₂ Emissions (tons per person)')
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown("### VKT Over Years")
    mean_df = df.groupby(['year', 'vehicle'])['vkt_pc'].mean().reset_index()
    mean_df.year = mean_df.year.astype(str)
    plt.figure(figsize=(10,5))
    city_df = df[df['city'] == selected_city]
    sns.barplot(data=city_df, x='year', y='vkt_pc', hue='vehicle', edgecolor='black')
    sns.lineplot(data=mean_df, x='year', y='vkt_pc', hue='vehicle', 
                linewidth=2, linestyle='--', legend=False)
    for vehicle in mean_df['vehicle'].unique():
        vehicle_data = mean_df[mean_df['vehicle'] == vehicle]
        for i in range(len(vehicle_data)):
            plt.text(x=vehicle_data['year'].iloc[i], y=vehicle_data['vkt_pc'].iloc[i],
                    s=f"mean {vehicle}", ha='center', va='bottom')

    plt.title(f'VKT Over Years - {selected_city.title()}')
    plt.xlabel('Year')
    plt.ylabel('VKT (vehicle kilometers traveled per person)')
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown("### Fuel Consumption Over Years")
    mean_df = df.groupby(['year', 'vehicle'])['consumption_pc'].mean().reset_index()
    mean_df.year = mean_df.year.astype(str)
    plt.figure(figsize=(10,5))
    city_df = df[df['city'] == selected_city]
    sns.barplot(data=city_df, x='year', y='consumption_pc', hue='vehicle', edgecolor='black')
    sns.lineplot(data=mean_df, x='year', y='consumption_pc', hue='vehicle', 
                linewidth=2, linestyle='--', legend=False)
    for vehicle in mean_df['vehicle'].unique():
        vehicle_data = mean_df[mean_df['vehicle'] == vehicle]
        for i in range(len(vehicle_data)):
            plt.text(x=vehicle_data['year'].iloc[i], y=vehicle_data['consumption_pc'].iloc[i],
                    s=f"mean {vehicle}", ha='center', va='bottom')

    plt.title(f'Fuel Consumption Over Years - {selected_city.title()}')
    plt.xlabel('Year')
    plt.ylabel('Fuel Consumption (tons per person)')
    plt.tight_layout()
    st.pyplot(plt)