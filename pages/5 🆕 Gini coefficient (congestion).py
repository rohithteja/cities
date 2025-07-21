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
  df = pd.read_csv('data/data_final/df_static.csv')
  df2 = pd.read_csv('data/data_final/df_dynamic.csv')
  df = pd.merge(df, df2, on=['city'], how='right')
  df = df[['city', 'population_2020', 'state_x', 'population_state', 'GDP_2020(billion USD)', 'urban_area_km2', 'oe', 'vkt_public_transport', 'year', 'vehicle',  'aadt', 'co2', 'co2_ff', 'mean_speed', 'vkt', 'weighted_speed', 'co2_congestion', 'state_y', 'consumption', 'gini_bc', 'gini_co2_total_congestion']]
  return df

df = load_data()
df['co2_congestion_pc'] = df['co2_congestion'] / df['population_2020']
df['co2_congestion_vkt'] = df['co2_congestion'] / df['vkt']
df['co2_congestion_area'] = df['co2_congestion'] / df['urban_area_km2']
# remove panaji, 'chandigarh', and 'faridabad' from the dataset
df = df[~df['city'].isin(['jabalpur'])]

# --- Streamlit App ---
st.markdown("# Indian Cities Project")
st.markdown("--------")

st.markdown(f'''
* Number of cities: {len(df.city.unique())}
* Years: {YEARS}
''')

# Gini Coefficient Plots

st.markdown("#### Gini BC vs CO₂ congestion per VKT")
fig, ax = plt.subplots(figsize=(6, 5))
scatter_plot(df, 'gini_bc', 'co2_congestion_vkt', hue='year', ax=ax, xlabel='Gini BC', ylabel='CO₂ congestion /vkt(tons/km)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini BC vs CO₂ per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_bc', 'co2_congestion_pc', hue='year', ax=axes[0], title='All cities', xlabel='Gini BC', ylabel='CO₂ per Capita (tons/person)')
scatter_plot(df[~df['city'].isin(OUTLIERS)], 'gini_bc', 'co2_congestion_pc', hue='year', ax=axes[1], title='Without Outliers', xlabel='Gini BC', ylabel='CO₂ per Capita (tons/person)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini CO₂ vs CO₂ congestion per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_co2_total_congestion', 'co2_congestion_pc', hue='year', ax=axes[0], title='All cities', xlabel='Gini for CO₂ Emissions', ylabel='CO₂ congestion per Capita (tons/person)')
scatter_plot(df[~df['city'].isin(OUTLIERS)], 'gini_co2_total_congestion', 'co2_congestion_pc', hue='year', ax=axes[1], title='Without Outliers', xlabel='Gini for CO₂ Emissions', ylabel='CO₂ congestion per Capita (tons/person)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini BC vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_bc', 'urban_area_km2', ax=axes[0], title='All cities', xlabel='Gini BC', ylabel='Urban Area (in km²)')
scatter_plot(remove_outliers(df, ['gini_bc', 'urban_area_km2']), 'gini_bc', 'urban_area_km2', ax=axes[1], title='Without Outliers', xlabel='Gini BC', ylabel='Urban Area (in km²)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini CO₂ congestion vs Urban Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_co2_total_congestion', 'urban_area_km2', ax=axes[0], title='All cities', xlabel='Gini CO₂', ylabel='Urban Area (in km²)')
scatter_plot(remove_outliers(df, ['gini_co2_total_congestion', 'urban_area_km2']), 'gini_co2_total_congestion', 'urban_area_km2', ax=axes[1], title='Without Outliers', xlabel='Gini CO₂', ylabel='Urban Area (in km²)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini BC vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_bc', 'GDP_2020(billion USD)', ax=axes[0], title='All cities', xlabel='Gini for BC', ylabel='GDP (in billions USD)')
scatter_plot(remove_outliers(df, ['gini_co2_total_congestion', 'GDP_2020(billion USD)'], contamination=0.08), 'gini_bc', 'GDP_2020(billion USD)', ax=axes[1], title='Without Outliers', xlabel='Gini for BC', ylabel='GDP (in billions USD)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Gini CO₂ congestion vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'gini_co2_total_congestion', 'GDP_2020(billion USD)', ax=axes[0], title='All cities', xlabel='Gini for CO₂ congestion', ylabel='GDP (in billions USD)')
scatter_plot(remove_outliers(df, ['gini_co2_total_congestion', 'GDP_2020(billion USD)'], contamination=0.08), 'gini_co2_total_congestion', 'GDP_2020(billion USD)', ax=axes[1], title='Without Outliers', xlabel='Gini for CO₂ congestion', ylabel='GDP (in billions USD)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# Orientation entropy section
st.markdown("#### Orientation of Cities")
st.markdown("Orientation entropy quantifies how uniformly a city's roads are aligned. Lower values mean roads mostly follow a single direction; higher values indicate roads are oriented in many directions.")
st.image('data/oe.png', caption='Orientation of Cities')

st.markdown("#### Orientation Entropy vs CO₂ per Capita")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'oe', 'co2_congestion_pc', ax=axes[0], title='All cities', xlabel='Orientation Entropy', ylabel='CO₂ congestion per Capita (tons/person)', highlight=OUTLIERS + ['mumbai'])
scatter_plot(df[~df['city'].isin(OUTLIERS)], 'oe', 'co2_congestion_pc', ax=axes[1], title='Without Outliers', xlabel='Orientation Entropy', ylabel='CO₂ congestion per Capita (tons/person)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Orientation Entropy vs CO₂ per Area")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'oe', 'co2_congestion_area', ax=axes[0], title='All cities', xlabel='Orientation Entropy', ylabel='CO₂ congestion per Area (tons/km²)', highlight=OUTLIERS + ['mumbai'])
scatter_plot(df[~df['city'].isin(OUTLIERS)], 'oe', 'co2_congestion_area', ax=axes[1], title='Without Outliers', xlabel='Orientation Entropy', ylabel='CO₂ congestion per Area (tons/km²)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown("#### Orientation Entropy vs GDP PPP")
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
scatter_plot(df, 'oe', 'GDP_2020(billion USD)', ax=axes[0], title='All cities', xlabel='Orientation Entropy', ylabel='GDP (in billions USD)')
scatter_plot(remove_outliers(df, ['oe', 'GDP_2020(billion USD)']), 'oe', 'GDP_2020(billion USD)', ax=axes[1], title='Without Outliers', xlabel='Orientation Entropy', ylabel='GDP (in billions USD)')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

