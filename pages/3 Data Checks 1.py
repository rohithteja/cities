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

# Plot 1: Fuel consumption vs CO₂ (Car vs Truck)
st.markdown("### Fuel consumption vs CO₂ (Car vs Truck)")
plot_car_truck(
  df, "consumption_pc", "co2_pc",
  "Fuel Consumption (tons/person)", "CO₂ per Capita (tons/person)",
  "CO₂ vs Fuel Consumption"
)

# Plot 2: VKT vs CO₂ (Car vs Truck)
st.markdown("### VKT vs CO₂ (Car vs Truck)")
plot_car_truck(
  df, "vkt_pc", "co2_pc",
  "VKT (km/person)", "CO₂ per Capita (tons/person)",
  "CO₂ vs VKT"
)

# Plot 3: Weighted speed vs CO₂ (Car vs Truck)
st.markdown("### Weighted speed vs CO₂ (Car vs Truck)")
plot_car_truck(
  df, "weighted_speed", "co2_pc",
  "Weighted Speed (km/h)", "CO₂ per Capita (tons/person)",
  "CO₂ vs Weighted Speed"
)

# Plot 4: AADT vs CO₂ (Car vs Truck)
st.markdown("### AADT vs CO₂ (Car vs Truck)")
plot_car_truck(
  df, "aadt", "co2_pc",
  "AADT (vehicles/day)", "CO₂ per Capita (tons/person)",
  "CO₂ vs AADT"
)
