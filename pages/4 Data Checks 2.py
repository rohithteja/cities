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
df['co2_congestion_pc'] = df['co2_congestion'] / df['population_2020']  # CO₂ congestion per capita
years = [2021, 2022, 2023]

st.markdown('''
* Number of cities: ''' + str(len(df.city.unique())) + '''
* Years: ''' + str(years) + '''
* Vehicle types: ''' + str(df.vehicle.unique()) + '''
''')

# remove all rows with city panaji
df = df[df['city'] != 'jabalpur']
df = df[df['city'] != 'panaji']
df = df[df['city'] != 'chandigarh']

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

# plot 1
st.markdown("### CO₂ per Fuel vs VKT per Capita (Car vs Truck)")
plot_car_truck(
  df, "vkt_per_capita", "co2_per_fuel",
  "VKT per Capita (km/person)", "CO₂ per Fuel (tons/ton fuel)",
  "CO₂ per Fuel vs VKT per Capita"
)

# plot 2
st.markdown("### CO₂ per Fuel vs Fuel per KM (Car vs Truck)")
plot_car_truck(
  df, "fuel_per_km", "co2_per_fuel",
  "Fuel per KM (tons/km)", "CO₂ per Fuel (tons/ton fuel)",
  "CO₂ per Fuel vs Fuel per KM"
)

# plot 3
st.markdown("### Fuel per KM vs VKT per Capita (Car vs Truck)")
plot_car_truck(
  df, "vkt_per_capita", "fuel_per_km",
  "VKT per Capita (km/person)", "Fuel per KM (tons/km)",
  "Fuel per KM vs VKT per Capita"
)

# plot 4
st.markdown("### Fuel per Capita vs Urban Density (Car vs Truck)")
plot_car_truck(
  df, "urban_density", "fuel_per_capita",
  "Urban Density (people/km²)", "Fuel per Capita (tons/person)",
  "Fuel per Capita vs Urban Density"
)

# plot 5
st.markdown("### CO₂ per Capita vs Urban Area (Car vs Truck)")
plot_car_truck(
  df, "sqrt_urban_area", "co2_pc",
  "Urban Area (sqrt km²)", "CO₂ per Capita (tons/person)",
  "CO₂ per Capita vs Urban Area"
)


