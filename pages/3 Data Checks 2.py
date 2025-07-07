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


# plot 1
st.markdown("### CO₂ per Fuel vs VKT per Capita")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="vkt_per_capita", y="co2_per_fuel", hue="vehicle", s=100,style="year",alpha=0.7)
plt.title("CO₂ per Fuel vs VKT per Capita")
plt.xlabel("VKT per Capita (km/person)")
plt.ylabel("CO₂ per Fuel (tons/ton fuel)")
st.pyplot(plt)

# plot 2
st.markdown("###  CO₂ per Fuel vs Fuel per KM")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="fuel_per_km", y="co2_per_fuel", hue="vehicle", s=100,style="year",alpha=0.7)
plt.title("CO₂ per Fuel vs Fuel per KM")
plt.xlabel("Fuel per KM (tons/km)")
plt.ylabel("CO₂ per Fuel (tons/ton fuel)")
st.pyplot(plt)

# plot 3
st.markdown("### Fuel per KM vs VKT per Capita")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="vkt_per_capita", y="fuel_per_km", hue="vehicle", s=100,style="year",alpha=0.7)
plt.title("Fuel per KM vs VKT per Capita")
plt.xlabel("VKT per Capita (km/person)")
plt.ylabel("Fuel per KM (tons/km)")
st.pyplot(plt)

# plot 4
st.markdown("### Fuel per Capita vs Urban Density")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="urban_density", y="fuel_per_capita", hue="vehicle", s=100,style="year",alpha=0.7)
plt.title("Fuel per Capita vs Urban Density")
plt.xlabel("Urban Density (people/km²)")
plt.ylabel("Fuel per Capita (tons/person)")
st.pyplot(plt)

# plot 5
st.markdown("### CO₂ per Capita vs Urban Area")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="sqrt_urban_area", y="co2_pc", hue="vehicle", s=100,style="year",alpha=0.7)
plt.title("CO₂ per Capita vs Urban Area")
plt.xlabel("Urban Area (sqrt km²)")
plt.ylabel("CO₂ per Capita (tons/person)")
st.pyplot(plt)


