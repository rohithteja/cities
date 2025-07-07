import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


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

st.markdown("# Indian Cities Project")
st.markdown("--------")

# Load the data
df = pd.read_csv(f'data/df_stats_streamlit.csv')
df['vkt_pc'] = df['vkt'] / df['population_2020']
df['consumption_pc'] = df['consumption'] / df['population_2020']
years = [2021, 2022, 2023]

st.markdown('''
* Number of cities: ''' + str(len(df.city.unique())) + '''
* Years: ''' + str(years) + '''
* Vehicle types: ''' + str(df.vehicle.unique()) + '''
''')

# remove all rows with city panaji
df = df[df['city'] != 'jabalpur']
df = df[df['city'] != 'panaji']

df["co2_per_gdp"] = df["co2"] / df["gdp_billions"]    # tonnes/billions usd
df["gdp_per_fuel"] = df["gdp_billions"] / df["consumption"] # billions usd/tonnes
df["fuel_per_km"] = df["consumption"] / df["vkt"]      # tonnes/km
df["vkt_per_capita"] = df["vkt"] / df["population_2020"]   # km/person
df["co2_per_fuel"] = df["co2"] / df["consumption"]          # tonnes/tonne fuel

df["fuel_per_capita"] = df["consumption"] / df["population_2020"]   # tonnes or liters per person
df["urban_density"] = df["population_2020"] / df["urban_area_km2"]  # people per km²
df['sqrt_urban_area'] = np.sqrt(df['urban_area_km2'])

df['co2_congestion_pc'] = df['co2_congestion'] / df['population_2020']  # CO₂ congestion per capita
df['co2_ff_pc'] = df['co2_ff'] / df['population_2020']  # Freeflow CO₂ per capita


# List of available columns

# Define human-readable labels
var_descriptions = {
    'co2': 'Total CO₂ emissions (tons)',
    'co2_ff': 'Freeflow CO₂ emissions (tons)',
    'mean_speed': 'Average vehicle speed (km/h)',
    'vkt': 'Vehicle kilometers travelled (km)',
    'weighted_speed': 'Weighted average speed by count (km/h)',
    'consumption': 'Total fuel consumption (tons)',
    'population_2020': 'Population',
    'urban_area_km2': 'Urban area (km²)',
    'gdp_billions': 'GDP (billions USD)',
    'co2_congestion': 'Congestion CO₂ emissions (tons)',
    'co2_pc': 'Per capita CO₂ (tons)',
    'co2_per_gdp': 'CO₂ per GDP (tons/USD)',
    'gdp_per_fuel': 'GDP per ton of fuel',
    'fuel_per_km': 'Fuel consumed per km (tons/km)',
    'vkt_per_capita': 'VKT per person',
    'co2_per_fuel': 'CO₂ per unit of fuel (tons/ton)',
    'fuel_per_capita': 'Fuel consumption per person (tons)',
    'urban_density': 'Population Density (people/km²)',
    'sqrt_urban_area': 'Square root of urban area',
    'co2_congestion_pc': 'Per capita CO₂ congestion (tons/person)',
    'co2_ff_pc': 'Per capita Freeflow CO₂ (tons/person)'
}

columns = ['co2', 'co2_ff', 'mean_speed', 'vkt',
           'weighted_speed', 'consumption', 'population_2020', 'urban_area_km2',
           'gdp_billions', 'co2_congestion', 'co2_pc', 'co2_per_gdp',
           'gdp_per_fuel', 'fuel_per_km', 'vkt_per_capita', 'co2_per_fuel',
           'fuel_per_capita', 'urban_density', 'sqrt_urban_area', 'co2_congestion_pc', 'co2_ff_pc']

columns_with_descriptions = sorted([var_descriptions[col] for col in columns])

st.markdown("## Scatterplot: Select Any Two Variables")

# Sidebar or inline dropdowns for selecting x and y
x_var = st.selectbox("Select X-axis variable", columns_with_descriptions)
y_var = st.selectbox("Select Y-axis variable", columns_with_descriptions)

# convert human-readable labels back to original column names
x_var1 = [k for k, v in var_descriptions.items() if v == x_var][0]
y_var1 = [k for k, v in var_descriptions.items() if v == y_var][0]

# Optional hue or other filters
hue_var = st.selectbox("Hue (optional)", ['None'] + ['vehicle', 'year'], index=0)
style_var = st.selectbox("Style (optional)", ['None'] + ['vehicle', 'year'], index=0)

# Create plot
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=df,
    x=x_var1,
    y=y_var1,
    hue=df[hue_var] if hue_var != 'None' else None,
    style=df[style_var] if style_var != 'None' else None,
    s=100,
    alpha=0.7
)
plt.xlabel(x_var)
plt.ylabel(y_var)
plt.title(f"{y_var} vs {x_var}")
st.pyplot(plt)


