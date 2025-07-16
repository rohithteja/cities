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
df = pd.read_csv(f'data/df_gini.csv')
df = df[df['city'] != 'jabalpur']

years = [2021, 2022, 2023]

st.markdown('''
* Number of cities: ''' + str(len(df.city.unique())) + '''
* Years: ''' + str(years) + '''
''')

# Create subplots for car and truck Gini coefficients
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Plot for cars
st.markdown("### Gini Coefficients for CO₂ Emissions and Betweenness Centrality")
sns.scatterplot(
  data=df,
  x='gini_co2_car', y='gini_bc', hue="year", s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Gini for CO2 Emissions (Car)')
axes[0].set_ylabel('Gini for Betweenness Centrality')
axes[0].set_title('Gini Car')
axes[0].legend(title='Year')

# Plot for trucks
sns.scatterplot(
  data=df,
  x='gini_co2_truck', y='gini_bc', hue="year", s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Gini for CO2 Emissions (Truck)')
axes[1].set_ylabel('Gini for Betweenness Centrality')
axes[1].set_title('Gini Truck')
axes[1].legend(title='Year')

plt.tight_layout()
st.pyplot(fig)

# bar plot of top 10 cities with lowest Gini coefficients for bc
st.markdown("### Top 10 Cities with Lowest Gini Coefficients for Betweenness Centrality")
top_10_cities = df.groupby('city').mean().nsmallest(10, 'gini_bc')
plt.figure(figsize=(8, 4))
sns.barplot(
  data=top_10_cities,
  x='gini_bc', y='city', palette='viridis'
)
plt.xlabel('Gini for Betweenness Centrality')
plt.ylabel('City')
plt.title('Top 10 Cities with Lowest Gini Coefficients for Betweenness Centrality')
plt.tight_layout()
st.pyplot(plt)


# bar plot of top 10 cities with lowest Gini coefficients for co2 emissions
st.markdown("### Top 10 Cities with Lowest Gini Coefficients for CO₂ Emissions")
top_10_cities_co2 = df.groupby('city').mean().nsmallest(10, 'gini_co2_total')
plt.figure(figsize=(8, 4))
sns.barplot(
  data=top_10_cities_co2,
  x='gini_co2_total', y='city', palette='viridis'
)
plt.xlabel('Gini for CO₂ Emissions')
plt.ylabel('City')
plt.title('Top 10 Cities with Lowest Gini Coefficients for CO₂ Emissions')
plt.tight_layout()
st.pyplot(plt)

st.markdown("### Orientation of Cities")

st.image('data/oe.png', caption='Orientation of Cities')

df_oe = pd.read_csv('data/oe.csv')

# bar plot of top 10 cities with highest orientation
st.markdown("### Top 10 Cities with lowest entropy")
top_10_cities_oe = df_oe.nsmallest(10, 'oe')
plt.figure(figsize=(8, 4))
sns.barplot(
  data=top_10_cities_oe,
  x='oe', y='city', palette='viridis'
)
plt.xlabel('Orientation Entropy')
plt.ylabel('City')
plt.title('Top 10 Cities with Lowest Orientation Entropy')
plt.tight_layout()
st.pyplot(plt)
