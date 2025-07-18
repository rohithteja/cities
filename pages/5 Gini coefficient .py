import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

# --- Constants ---
YEARS = [2021, 2022, 2023]
OUTLIERS = ['chandigarh', 'panaji', 'faridabad']

# --- Utility Functions ---
def scatter_plot(df, x, y, hue=None, ax=None, title='', xlabel='', ylabel='', highlight=None):
  sns.scatterplot(data=df, x=x, y=y, hue=hue, s=100, alpha=0.7, palette="Set1", ax=ax)
  ax.set_xlabel(xlabel or x)
  ax.set_ylabel(ylabel or y)
  ax.set_title(title)
  if hue:
    ax.legend(title=hue)
  if highlight:
    for i in range(len(df)):
      if df['city'].iloc[i] in highlight:
        ax.text(df[x].iloc[i], df[y].iloc[i], df['city'].iloc[i], fontsize=10, color='red')

def bar_plot(df, x, y, title='', xlabel='', ylabel=''):
  fig, ax = plt.subplots(figsize=(8, 4))
  sns.barplot(data=df, x=x, y=y, palette='viridis', ax=ax)
  ax.set_xlabel(xlabel or x)
  ax.set_ylabel(ylabel or y)
  ax.set_title(title)
  plt.tight_layout()
  st.pyplot(fig)
  plt.close(fig)

def remove_outliers(df, cols, contamination=0.06):
  iso = IsolationForest(contamination=contamination, random_state=42)
  outlier_pred = iso.fit_predict(df[cols])
  return df[outlier_pred == 1]

# --- Data Loading (Cached) ---
@st.cache_data
def load_data():
  df = pd.read_csv('data/df_gini.csv')
  df = df[df['city'] != 'jabalpur']
  df_stats = pd.read_csv('data/stats.csv')
  df_stats['co2_pc'] = df_stats['co2'] / df_stats['population_2020']
  df_stats['co2_vkt'] = df_stats['co2'] / df_stats['vkt']
  df_stats = df_stats[df_stats['city'] != 'jabalpur']
  df = pd.merge(df, df_stats, on=['city', 'year'], how='left')
  df1 = df.groupby('city', as_index=False).mean(numeric_only=True)
  df_oe = pd.read_csv('data/oe.csv')
  df_oe = pd.merge(df_oe, df_stats.groupby('city', as_index=False).mean(numeric_only=True), on='city', how='left')
  df_oe['co2_area'] = df_oe['co2'] / df_oe['urban_area_km2']
  return df, df1, df_oe

df, df1, df_oe = load_data()

# --- Streamlit App ---
st.markdown("# Indian Cities Project")
st.markdown("--------")

st.markdown(f'''
* Number of cities: {len(df.city.unique())}
* Years: {YEARS}
''')

# Gini Coefficient Plots
st.markdown("#### Gini Coefficient vs Betweenness Centrality")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_co2_car', 'gini_bc', hue='year', ax=axes[0], title='Gini Car', xlabel='Gini for CO2 Emissions (Car)', ylabel='Gini for Betweenness Centrality')
scatter_plot(df, 'gini_co2_truck', 'gini_bc', hue='year', ax=axes[1], title='Gini Truck', xlabel='Gini for CO2 Emissions (Truck)', ylabel='Gini for Betweenness Centrality')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini BC vs CO₂ per VKT")
fig, ax = plt.subplots(figsize=(6, 5))
scatter_plot(df, 'gini_bc', 'co2_vkt', hue='year', ax=ax, xlabel='Gini BC', ylabel='CO₂ /vkt(tons/km)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini BC vs CO₂ per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_bc', 'co2_pc', hue='year', ax=axes[0], title='All cities', xlabel='Gini BC', ylabel='CO₂ per Capita (tons/person)')
scatter_plot(df[~df['city'].isin(OUTLIERS)], 'gini_bc', 'co2_pc', hue='year', ax=axes[1], title='Without Outliers', xlabel='Gini BC', ylabel='CO₂ per Capita (tons/person)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini CO₂ vs CO₂ per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_co2_total', 'co2_pc', hue='year', ax=axes[0], title='All cities', xlabel='Gini for CO₂ Emissions', ylabel='CO₂ per Capita (tons/person)')
scatter_plot(df[~df['city'].isin(OUTLIERS)], 'gini_co2_total', 'co2_pc', hue='year', ax=axes[1], title='Without Outliers', xlabel='Gini for CO₂ Emissions', ylabel='CO₂ per Capita (tons/person)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini BC vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df1, 'gini_bc', 'urban_area_km2', ax=axes[0], title='All cities', xlabel='Gini BC', ylabel='Urban Area (in km²)')
scatter_plot(remove_outliers(df1, ['gini_bc', 'urban_area_km2']), 'gini_bc', 'urban_area_km2', ax=axes[1], title='Without Outliers', xlabel='Gini BC', ylabel='Urban Area (in km²)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini CO₂ vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df1, 'gini_co2_total', 'urban_area_km2', ax=axes[0], title='All cities', xlabel='Gini CO₂', ylabel='Urban Area (in km²)')
scatter_plot(remove_outliers(df1, ['gini_co2_total', 'urban_area_km2']), 'gini_co2_total', 'urban_area_km2', ax=axes[1], title='Without Outliers', xlabel='Gini CO₂', ylabel='Urban Area (in km²)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini BC vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df1, 'gini_bc', 'gdp_billions', ax=axes[0], title='All cities', xlabel='Gini for BC', ylabel='GDP (in billions USD)')
scatter_plot(remove_outliers(df1, ['gini_co2_total', 'gdp_billions'], contamination=0.08), 'gini_bc', 'gdp_billions', ax=axes[1], title='Without Outliers', xlabel='Gini for BC', ylabel='GDP (in billions USD)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini CO₂ vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df1, 'gini_co2_total', 'gdp_billions', ax=axes[0], title='All cities', xlabel='Gini for CO₂ Emissions', ylabel='GDP (in billions USD)')
scatter_plot(remove_outliers(df1, ['gini_co2_total', 'gdp_billions'], contamination=0.08), 'gini_co2_total', 'gdp_billions', ax=axes[1], title='Without Outliers', xlabel='Gini for CO₂ Emissions', ylabel='GDP (in billions USD)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Bar plots for top 10 cities
st.markdown("#### Top 10 Cities with Lowest Gini Coefficients for Betweenness Centrality")
bar_plot(df1.nsmallest(10, 'gini_bc'), 'gini_bc', 'city', title='Top 10 Cities with Lowest Gini Coefficients for Betweenness Centrality', xlabel='Gini for Betweenness Centrality', ylabel='City')

st.markdown("#### Top 10 Cities with Lowest Gini Coefficients for CO₂ Emissions")
bar_plot(df1.nsmallest(10, 'gini_co2_total'), 'gini_co2_total', 'city', title='Top 10 Cities with Lowest Gini Coefficients for CO₂ Emissions', xlabel='Gini for CO₂ Emissions', ylabel='City')

# Orientation entropy section
st.markdown("#### Orientation of Cities")
st.markdown("Orientation entropy quantifies how uniformly a city's roads are aligned. Lower values mean roads mostly follow a single direction; higher values indicate roads are oriented in many directions.")
st.image('data/oe.png', caption='Orientation of Cities')

st.markdown("#### Top 10 Cities with lowest entropy")
bar_plot(df_oe.nsmallest(10, 'oe'), 'oe', 'city', title='Top 10 Cities with Lowest Orientation Entropy', xlabel='Orientation Entropy', ylabel='City')

st.markdown("#### Orientation Entropy vs CO₂ per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df_oe, 'oe', 'co2_pc', ax=axes[0], title='All cities', xlabel='Orientation Entropy', ylabel='CO₂ Emissions per Capita (tons/person)', highlight=OUTLIERS + ['mumbai'])
scatter_plot(df_oe[~df_oe['city'].isin(OUTLIERS)], 'oe', 'co2_pc', ax=axes[1], title='Without Outliers', xlabel='Orientation Entropy', ylabel='CO₂ Emissions per Capita (tons/person)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Orientation Entropy vs CO₂ per Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df_oe, 'oe', 'co2_area', ax=axes[0], title='All cities', xlabel='Orientation Entropy', ylabel='CO₂ Emissions per Area (tons/km²)', highlight=OUTLIERS + ['mumbai'])
scatter_plot(df_oe[~df_oe['city'].isin(OUTLIERS)], 'oe', 'co2_area', ax=axes[1], title='Without Outliers', xlabel='Orientation Entropy', ylabel='CO₂ Emissions per Area (tons/km²)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Orientation Entropy vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df_oe, 'oe', 'gdp_billions', ax=axes[0], title='All cities', xlabel='Orientation Entropy', ylabel='GDP (in billions USD)')
scatter_plot(remove_outliers(df_oe, ['oe', 'gdp_billions']), 'oe', 'gdp_billions', ax=axes[1], title='Without Outliers', xlabel='Orientation Entropy', ylabel='GDP (in billions USD)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Orientation Entropy vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df_oe, 'oe', 'urban_area_km2', ax=axes[0], title='All cities', xlabel='Orientation Entropy', ylabel='Urban Area (in km²)')
scatter_plot(remove_outliers(df_oe, ['oe', 'gdp_billions']), 'oe', 'urban_area_km2', ax=axes[1], title='Without Outliers', xlabel='Orientation Entropy', ylabel='Urban Area (in km²)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)
