import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df1 = pd.read_csv(f'data/data_final/df_static.csv')
df2 = pd.read_csv(f'data/data_final/df_dynamic.csv')

dic_agg_vehicle = {'aadt':'mean', 'co2': 'sum', 'co2_ff': 'sum',
       'mean_speed': 'mean', 'vkt': 'sum', 'weighted_speed': 'mean', 'co2_congestion': 'sum', 
       'consumption': 'sum', 'gini_bc': 'mean', 'gini_co2_total_congestion': 'mean'}
df2_agg_gini_co2 = df2.groupby(['city', 'year']).agg(dic_agg_vehicle).reset_index()
df2_agg2_bc = df2_agg_gini_co2.groupby('city').mean(numeric_only=True).reset_index()

df_gini_co2 = pd.merge(df1, df2_agg_gini_co2, on='city', how='right')
# remove panaji, chandigarh, jabalpur
df_gini_co2 = df_gini_co2[~df_gini_co2['city'].isin(['panaji', 'chandigarh','jabalpur'])]

st.markdown("# Gini Coefficient (BC) comparisons")
st.markdown("Gini BC is computed for the edge betweenness centrality of the road network.")
st.image('data/gini/bc_comparison/1.png')
st.image('data/gini/bc_comparison/2.png')
st.image('data/gini/bc_comparison/3.png')
st.image('data/gini/bc_comparison/4.png')

st.markdown("### Gini Coefficient (CO₂) comparisons")
st.markdown("Gini CO₂ is computed for the total CO₂ emissions of the road network.")
st.image('data/gini/co2_comparison/1.png')
st.image('data/gini/co2_comparison/2.png')
st.image('data/gini/co2_comparison/3.png')
st.image('data/gini/co2_comparison/4.png')

