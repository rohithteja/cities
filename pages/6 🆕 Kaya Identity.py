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
st.image(f'data/plots1/og/cumulative.png') 


