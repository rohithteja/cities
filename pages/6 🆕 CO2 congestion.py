import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

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

st.markdown("### Road Type")
st.markdown("City roads are classified into 5 categories based on their importance.")
st.markdown("""
- **Class 1:** High volume, maximum speed traffic movement between and through major metropolitan areas.
- **Class 2:** Channel traffic to Class 1 roads.
- **Class 3:** Interconnect Class 2 roads for high volume traffic movement.
- **Class 4:** High volume traffic movement at moderate speeds between neighbourhoods.
- **Class 5:** Below level of any functional class (can include marginal roads).
""")


st.markdown("### CO2 Congestion by Road Type")
st.markdown("Highest CO2 congestion is observed in Class 5 roads. We focus on Class 5 roads for further analysis.")
st.image('data/congestion_fc/1.png')

st.markdown("### CO2 Congestion distribution")
st.image('data/congestion_fc/2.png')

st.markdown("### CO2 Congestion Share")
st.markdown("It is the share of per-capita CO2 congestion emissions that comes from each road type.")
st.image('data/congestion_fc/3.png')

st.markdown("### CO2 Congestion Share Map")
st.image('data/congestion_fc/4.png')

st.markdown("### Regression Analysis")
st.markdown("Goal: Identify which city-level factors influence the share of CO₂ congestion emissions from class 5 roads using Ordinary Least Squares (OLS) regression.")
st.markdown("Dependent Variable: Share of CO₂ congestion emissions from class 5 roads")
st.markdown("Independent Variables (log transformed): Population, GDP, Urban area, VKT by public transport, Road density (Rho_r), Intersection density (Rho_i), Road-to-intersection ratio (Rho_ratio), Total road length, Mean speed, Weighted speed, Gini BC, Orientation entropy (Oe).")

# load model pkl
model = joblib.load('data/congestion_fc/model.pkl')
st.write(model.summary())

st.markdown("#### OLS Regression Feature Importance")
st.image('data/congestion_fc/5.png')

st.markdown("### Interpretation")

st.markdown("""1. Rho_ratio (road-to-intersection ratio) (Coef = +2.68, p = 0.004)
            - More roads per intersection (i.e., lower intersection density) = higher class 5 road CO₂ congestion shares.
            - Could indicate poorly connected networks where traffic is forced onto fewer minor links, causing congestion.
            """)

st.markdown("""2. Weighted speed (by count) (Coef = -1.86, p = 0)
            - Higher weighted speeds = lower congestion CO₂ shares on class 5 roads.
            - Higher speeds likely mean smoother traffic and lower emissions on minor roads.
            """)
st.markdown("""3. Mean speed (Coef = +1.33, p = 0)
            - Higher mean speeds = higher congestion-related CO₂ share on minor roads.
            - Mean speed can be skewed by some fast roads, could be spillage from major roads.
            """)
st.markdown("""4. Gini BC (Coef = -1.30, p = 0.034)
            - Heterogeneous traffic distribution (high Gini) = lower emissions from minor roads.
            - Traffic could be more focused on major roads, reducing minor road congestion.
            """)

st.markdown("""6. Rho_r (road density) (Coef = -1.03, p = 0.038)
            - Higher road density = lower congestion emissions share from minor roads.
            """)

st.markdown("""5. Rho_i (intersection density) (Coef = +0.40, p = 0.005)
            - Higher intersection density = higher congestion share on minor roads.
            """)

st.markdown("""8. Population (Coef = -0.10, p = 0)
            - Larger cities (by population) = lower minor road congestion CO₂ share.
            - Better road hierarchies and infrastructure.
            """)