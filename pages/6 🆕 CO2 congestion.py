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

# # load model pkl
# model = joblib.load('data/congestion_fc/model.pkl')
# st.write(model.summary())

model_results = '''                            OLS Regression Results                            
==============================================================================
Dep. Variable:             cong_share   R-squared:                       0.626
Model:                            OLS   Adj. R-squared:                  0.610
Method:                 Least Squares   F-statistic:                     39.99
Date:                Mon, 28 Jul 2025   Prob (F-statistic):           3.09e-54
Time:                        16:00:28   Log-Likelihood:                 320.94
No. Observations:                 300   AIC:                            -615.9
Df Residuals:                     287   BIC:                            -567.7
Df Model:                          12                                         
Covariance Type:            nonrobust                                         
=============================================================================================
                                coef    std err          t      P>|t|      [0.025      0.975]
---------------------------------------------------------------------------------------------
const                         3.0697      0.536      5.723      0.000       2.014       4.125
log_population_2020_x        -0.0975      0.015     -6.401      0.000      -0.127      -0.067
log_GDP_2020(billion USD)    -0.0005      0.012     -0.047      0.962      -0.023       0.022
log_urban_area_km2           -0.4846      0.439     -1.104      0.271      -1.349       0.380
log_oe                        0.0344      0.192      0.179      0.858      -0.343       0.412
log_vkt_public_transport      0.0046      0.007      0.671      0.503      -0.009       0.018
log_rho_r                    -1.0348      0.498     -2.080      0.038      -2.014      -0.055
log_rho_i                     0.4023      0.142      2.839      0.005       0.123       0.681
log_rho_ratio                 2.6819      0.922      2.909      0.004       0.867       4.496
log_road_length_km            0.5392      0.433      1.247      0.214      -0.312       1.391
log_mean_speed                1.3261      0.144      9.219      0.000       1.043       1.609
log_weighted_speed           -1.8593      0.148    -12.589      0.000      -2.150      -1.569
log_gini_bc                  -1.2990      0.609     -2.132      0.034      -2.498      -0.100
==============================================================================
Omnibus:                       12.686   Durbin-Watson:                   1.021
Prob(Omnibus):                  0.002   Jarque-Bera (JB):               17.311
Skew:                          -0.330   Prob(JB):                     0.000174
Kurtosis:                       3.974   Cond. No.                     5.10e+03
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 5.1e+03. This might indicate that there are
strong multicollinearity or other numerical problems.
'''
st.code(model_results, language='text')

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