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

st.markdown("### Custom Kaya Identity for Urban Transport Emissions")
st.latex(r"""
\frac{\text{CO₂}}{\text{Population}} =
\frac{\text{VKT}}{\text{Population}} \times
\left(
\frac{\text{CO2\_freeflow}}{\text{VKT}} +
\frac{\text{CO2\_congestion}}{\text{VKT}}
\right)
""")

st.markdown("""
**Term Explanations:**

- $\dfrac{\\text{CO₂}}{\\text{Population}}$ : CO₂ emissions per unit of population.

- $\dfrac{\\text{VKT}}{\\text{Population}}$ : Vehicle kilometers traveled (VKT) per unit of population.

- $\dfrac{\\text{CO2\_freeflow}}{\\text{VKT}}$ : CO₂ emissions per VKT under free-flow conditions (speed = 85th percentile).

- $\dfrac{\\text{CO2\_congestion}}{\\text{VKT}}$ : CO₂ emissions per VKT under congestion conditions.
""")

# separation line
st.markdown("---")

select_year = st.selectbox("Select Year", [2021, 2022, 2023], index=0)

# marker size is the population of the city
# Load the data
st.markdown("### CO2 per Population")
st.markdown('Marker size is the population of the city.')
st.image(f'data/kaya_identity/{select_year}/co2_per_capita.png')
st.markdown("### VKT per Population")
st.image(f'data/kaya_identity/{select_year}/vkt_per_pop.png')
st.markdown("### CO2 Congestion per VKT")
st.image(f'data/kaya_identity/{select_year}/co2_congestion_per_vkt.png')

st.markdown("### Relationships between the drivers of CO₂ emissions")
st.markdown("Some cities with highest population are annotated.")
st.image(f'data/kaya_identity/scatter.png')

# cumulative CO2 emissions
st.markdown("### Cumulative CO₂ Emissions")
st.markdown(f"Year = {select_year}")
st.image(f'data/plots1/og/cumulative/{select_year}/all_100_cities_highlighted.png')


st.markdown("### Cumulative CO₂ Congestion Emission Contribution by Road Type")
st.image(f'data/plots1/og/congestion_contribution_fc.png')

df_fc_ratio = pd.read_csv(f'data/data_final/df_fc_ratio.csv')

# explain congestion ratio
st.markdown("### Congestion Ratio")
st.markdown("Congestion ratio = ratio of CO₂ congestion emissions in minor roads to major roads.")
st.markdown("Major roads (1,2,3 functional classes), Minor roads (4,5 functional classes).")
st.markdown("As population increases, the contribution of CO2 congestion emission from minor roads decreases (mainly for bigger cities)")
x = 'population_2020'
y = 'minor_major_ratio'
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_fc_ratio,x=x, y=y, s=100, alpha=0.7)
plt.xlabel('Population')
plt.ylabel('CO2 Congestion ratio (Minor/Major roads)')
st.pyplot(plt)