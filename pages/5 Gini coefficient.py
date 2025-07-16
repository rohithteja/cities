import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest


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

df_stats = pd.read_csv(f'data/stats.csv')
df_stats['co2_pc'] = df_stats['co2'] / df_stats['population_2020']
df_stats = df_stats[df_stats['city'] != 'jabalpur']

# merge the two dataframes on city and year
df = pd.merge(df, df_stats, on=['city', 'year'], how='left')


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

# gini bc vs co2_pc with and without outliers
st.markdown("### Gini BC vs CO₂ per Capita")

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df,
  x='gini_bc', y='co2_pc', hue="year", s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Gini BC')
axes[0].set_ylabel('CO₂ per Capita (tons/person)')
axes[0].set_title('All cities')
axes[0].legend(title='Year')

# Second subplot: without outliers
outliers = ['chandigarh', 'panaji', 'faridabad']
df_no_outliers = df[~df['city'].isin(outliers)]
sns.scatterplot(
  data=df_no_outliers,
  x='gini_bc', y='co2_pc', hue="year", s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Gini BC')
axes[1].set_ylabel('CO₂ per Capita (tons/person)')
axes[1].set_title('Without Outliers')
axes[1].legend(title='Year')

plt.tight_layout()
st.pyplot(fig)



# gini co2 vs co2_pc
st.markdown("### Gini CO₂ vs CO₂ per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df,
  x='gini_co2_total', y='co2_pc', hue="year", s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Gini for CO₂ Emissions')
axes[0].set_ylabel('CO₂ per Capita (tons/person)')
axes[0].set_title('All cities')
axes[0].legend(title='Year')

# Second subplot: without outliers
outliers = ['chandigarh', 'panaji', 'faridabad']
df_no_outliers = df[~df['city'].isin(outliers)]
sns.scatterplot(
  data=df_no_outliers,
  x='gini_co2_total', y='co2_pc', hue="year", s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Gini for CO₂ Emissions')
axes[1].set_ylabel('CO₂ per Capita (tons/person)')
axes[1].set_title('Without Outliers')
axes[1].legend(title='Year')

plt.tight_layout()
st.pyplot(fig)

df1 = df.groupby('city').mean().reset_index()

# gini bc vs urban area
st.markdown("### Gini BC vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df1,
  x='gini_bc', y='urban_area_km2', s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Gini BC')
axes[0].set_ylabel('Urban Area (in km²)')
axes[0].set_title('All cities')
# Second subplot: without outliers
# Use IsolationForest to detect outliers based on 'gini_bc' and 'urban_area_km2'
iso = IsolationForest(contamination=0.06, random_state=42)
outlier_pred = iso.fit_predict(df1[['gini_bc', 'urban_area_km2']])
df_no_outliers = df1[outlier_pred == 1]
sns.scatterplot(
  data=df_no_outliers,
  x='gini_bc', y='urban_area_km2',  s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Gini BC')
axes[1].set_ylabel('Urban Area (in km²)')
axes[1].set_title('Without Outliers')
plt.tight_layout()
st.pyplot(fig)

# gini co2 vs urban area
st.markdown("### Gini CO₂ vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df1,
  x='gini_co2_total', y='urban_area_km2', s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Gini CO₂')
axes[0].set_ylabel('Urban Area (in km²)')
axes[0].set_title('All cities')
# Second subplot: without outliers
# Use IsolationForest to detect outliers based on 'gini_co2_total' and 'urban_area_km2'
iso = IsolationForest(contamination=0.06, random_state=42)
outlier_pred = iso.fit_predict(df1[['gini_co2_total', 'urban_area_km2']])
df_no_outliers = df1[outlier_pred == 1]
sns.scatterplot(
  data=df_no_outliers,
  x='gini_co2_total', y='urban_area_km2',  s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Gini CO₂')
axes[1].set_ylabel('Urban Area (in km²)')
axes[1].set_title('Without Outliers')
plt.tight_layout()
st.pyplot(fig)

# gini bc vs gdp_billions
st.markdown("### Gini BC vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df1,
  x='gini_bc', y='gdp_billions', s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Gini for BC')
axes[0].set_ylabel('GDP (in billions USD)')
axes[0].set_title('All cities')
# Second subplot: without outliers
# Use IsolationForest to detect outliers based on 'gini_co2_total' and 'gdp_billions'
iso = IsolationForest(contamination=0.08, random_state=42)
outlier_pred = iso.fit_predict(df1[['gini_co2_total', 'gdp_billions']])
df_no_outliers = df1[outlier_pred == 1]
sns.scatterplot(
  data=df_no_outliers,
  x='gini_bc', y='gdp_billions',  s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Gini for BC')
axes[1].set_ylabel('GDP (in billions USD)')
axes[1].set_title('Without Outliers')
plt.tight_layout()
st.pyplot(fig)


# gini co2 vs gdp_billions
st.markdown("### Gini CO₂ vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df1,
  x='gini_co2_total', y='gdp_billions', s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Gini for CO₂ Emissions')
axes[0].set_ylabel('GDP (in billions USD)')
axes[0].set_title('All cities')
# Second subplot: without outliers
# Use IsolationForest to detect outliers based on 'gini_co2_total' and 'gdp_billions'
iso = IsolationForest(contamination=0.08, random_state=42)
outlier_pred = iso.fit_predict(df1[['gini_co2_total', 'gdp_billions']])
df_no_outliers = df1[outlier_pred == 1]
sns.scatterplot(
  data=df_no_outliers,
  x='gini_co2_total', y='gdp_billions', s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Gini for CO₂ Emissions')
axes[1].set_ylabel('GDP (in billions USD)')
axes[1].set_title('Without Outliers')
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
# eplain the orientation of cities
st.markdown("Orientation entropy quantifies how uniformly a city's roads are aligned. Lower values mean roads mostly follow a single direction; higher values indicate roads are oriented in many directions.")

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

# oe vs co2_pc

# merge df_oe with df_stats on city
df_oe = pd.merge(df_oe, df_stats.groupby('city').mean().reset_index(), on=['city'], how='left')

st.markdown("### Orientation Entropy vs CO₂ Emissions per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# First subplot: with outliers
sns.scatterplot(
  data=df_oe,
  x='oe', y='co2_pc', s=100,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Orientation Entropy')
axes[0].set_ylabel('CO₂ Emissions per Capita (tons/person)')
axes[0].set_title('All cities')
# Mark the outliers
for i in range(len(df_oe)):
  if df_oe['city'].iloc[i] in ['chandigarh', 'panaji', 'faridabad', 'mumbai']:
    axes[0].text(df_oe['oe'].iloc[i], df_oe['co2_pc'].iloc[i], df_oe['city'].iloc[i], fontsize=10, color='red')

# Second subplot: without outliers
df_oe_no_outliers = df_oe[~df_oe['city'].isin(['chandigarh', 'panaji', 'faridabad'])]
sns.scatterplot(
  data=df_oe_no_outliers,
  x='oe', y='co2_pc', s=100,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Orientation Entropy')
axes[1].set_ylabel('CO₂ Emissions per Capita (tons/person)')
axes[1].set_title('Without Outliers')

plt.tight_layout()
st.pyplot(fig)

# oe vs gdp_billions
st.markdown("### Orientation Entropy vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df_oe,
  x='oe', y='gdp_billions', s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Orientation Entropy')
axes[0].set_ylabel('GDP (in billions USD)')
axes[0].set_title('All cities')
# Second subplot: without outliers
# Use IsolationForest to detect outliers based on 'oe' and 'gdp_billions'
iso = IsolationForest(contamination=0.06, random_state=42)
outlier_pred = iso.fit_predict(df_oe[['oe', 'gdp_billions']])
df_no_outliers = df_oe[outlier_pred == 1]
sns.scatterplot(
  data=df_no_outliers,
  x='oe', y='gdp_billions',  s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Orientation Entropy')
axes[1].set_ylabel('GDP (in billions USD)')
axes[1].set_title('Without Outliers')
plt.tight_layout()
st.pyplot(fig)

# oe vs urban area
st.markdown("### Orientation Entropy vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# First subplot: with outliers
sns.scatterplot(
  data=df_oe,
  x='oe', y='urban_area_km2', s=100, alpha=0.7,
  palette="Set1", ax=axes[0]
)
axes[0].set_xlabel('Orientation Entropy')
axes[0].set_ylabel('Urban Area (in km²)')
axes[0].set_title('All cities')
# Second subplot: without outliers
# Use IsolationForest to detect outliers based on 'oe' and 'urban_area_km2'
iso = IsolationForest(contamination=0.06, random_state=42)
outlier_pred = iso.fit_predict(df_oe[['oe', 'gdp_billions']])
df_no_outliers = df_oe[outlier_pred == 1]
sns.scatterplot(
  data=df_no_outliers,
  x='oe', y='urban_area_km2',  s=100, alpha=0.7,
  palette="Set1", ax=axes[1]
)
axes[1].set_xlabel('Orientation Entropy')
axes[1].set_ylabel('Urban Area (in km²)')
axes[1].set_title('Without Outliers')
plt.tight_layout()
st.pyplot(fig)

