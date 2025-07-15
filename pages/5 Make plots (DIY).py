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
df = pd.read_csv(f'data/data_annual_streamlit.csv')
df['vkt_pc'] = df['vkt'] / df['population_2020']
df['consumption_pc'] = df['consumption'] / df['population_2020']
df['co2_pc'] = df['co2'] / df['population_2020']
df['co2_congestion'] = df['co2'] - df['co2_ff']  # CO₂ congestion

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

# Helper function to plot for car and truck side by side
def plot_car_truck(df, x, y, xlabel, ylabel, title):
  fig, axes = plt.subplots(1, 2, figsize=(15, 5))
  vehicles = ['car', 'truck']
  for i, vehicle in enumerate(vehicles):
    sns.scatterplot(
      data=df[df['vehicle'] == vehicle],
      x=x, y=y, hue="year", s=100, alpha=0.7, ax=axes[i],
      palette="Set1"
    )
    axes[i].set_title(f"{title} ({vehicle.capitalize()})")
    axes[i].set_xlabel(xlabel)
    axes[i].set_ylabel(ylabel if i == 0 else "")
    axes[i].legend(title="Year")
  plt.tight_layout()
  st.pyplot(plt)
  plt.close()

st.markdown("## Car vs Truck DIY Plot")

# User selects variables
x_var = st.selectbox("X variable", columns, format_func=lambda x: var_descriptions[x])
y_var = st.selectbox("Y variable", columns, format_func=lambda x: var_descriptions[x])

x_label = var_descriptions[x_var]
y_label = var_descriptions[y_var]
title = f"{y_label} vs {x_label}"

plot_car_truck(df, x_var, y_var, x_label, y_label, title)

