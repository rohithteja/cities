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


# plot 1
st.markdown("### Fuel consumption vs CO₂ ")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="consumption_pc", y="co2_pc", hue="vehicle",style="year", s=100,alpha=0.7)
plt.title("CO₂ vs Fuel Consumption")
plt.xlabel("Fuel Consumption (tons/person)")
plt.ylabel("CO₂ per Capita (tons/person)")
st.pyplot(plt)

# plot 2
st.markdown("### VKT vs CO₂ ")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="vkt_pc", y="co2_pc", hue="vehicle", s=100,style="year",alpha=0.7)
plt.title("CO₂ vs VKT")
plt.xlabel("VKT (km/person)")
plt.ylabel("CO₂ per Capita (tons/person)")
st.pyplot(plt)

# plot 3
st.markdown("### Weighted speed vs CO₂ ")
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x="weighted_speed", y="co2_pc", hue="vehicle", s=100,style="year",alpha=0.7)
plt.title("CO₂ vs Weighted Speed")
plt.xlabel("Weighted Speed (km/h)")
plt.ylabel("CO₂ per Capita (tons/person)")
st.pyplot(plt)

