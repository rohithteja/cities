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
df = pd.read_csv(f'data/stats.csv')
df['co2_pc'] = df['co2'] / df['population_2020']


years = [2021, 2022, 2023]
st.selectbox('Select Year', options=years, index=0, key='year')

# set default year in session state
if 'year' not in st.session_state:
    st.session_state.year = 2021

df_filter = df[df['year'] == st.session_state.year]

# plot bar chart for CO2 emissions per capita by city
st.markdown("### CO₂ Emissions per Capita by City")
plt.figure(figsize=(5, 3))
df_filter = df_filter.sort_values('co2_pc', ascending=True).tail(10)
plt.barh(df_filter['city'], df_filter['co2_pc'], color='skyblue')
plt.xlabel('CO2 Emissions per Capita (kg)')
plt.title('CO2 Emissions per Capita by City in 2021')
# remove gaps in y-axis beginning and end
plt.gca().set_ylim(-0.5, len(df_filter) - 0.5)
plt.grid(axis='x')
plt.tight_layout()
st.pyplot(plt)

# the outliers 
st.markdown(f"Outliers in CO₂ Emissions per Capita: Chandigarh, Panaji")
