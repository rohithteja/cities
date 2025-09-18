import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os

def show_ml_model_page():
    """
    Streamlit page explaining the CO2 Congestion Prediction ML Model
    """
    
    st.title("CO2 Congestion Prediction (GRID)")
    st.markdown("Predicting CO2 congestion emissions at a 500m grid level for Mumbai")
    st.markdown("---")
    
    # Overview Section
    st.header("Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Objective")
        st.write("""
        Predict **CO2 congestion emissions** from traffic for grid cells in Indian cities (Mumbai) using 
        urban characteristics and transportation patterns.
        """)
        
        st.subheader("Data")
        st.write("""
        - **Cities**: Mumbai (grids of 500m x 500m)
        - **Years**: 2021-2023  
        - **Vehicle Types**: 2W, 3W, LMV, HDV
        - 48840 data points
        """)
    
    with col2:
        st.subheader("Methodology")
        st.write("""
        - Random Forest Regression
        - **Target**: CO2 congestion emissions
        - **Predictors**: 30 urban & transport gridded features
        - 80/20 train-test split
        """)
        
        st.subheader("Metrics")
        metrics_data = {
            'Metric': ['R² Score', 'RMSE', 'RRMSE'],
            'Value': ['0.96', '9.9', '0.41']
        }
        st.dataframe(pd.DataFrame(metrics_data), hide_index=True)
    
    st.markdown("---")
    
    # Data Features Section
    st.header("Predictors")
    st.markdown('### Points of interest ')
    st.markdown('Gas_stations, Businesses, Community_centers, Edu_institutions, Entertainment, Financial_institutions, Hospitals, Landmark, Major_highways, Parks_recreation, Parking, Rail_roads, Restaurants, Secondary_highways, Shopping, Transportation_hubs, Hotels, Water_bodies, Rivers')
    st.markdown('### Road network ')
    st.markdown('Avg_speed, road_length,  major_road(%), minor_road(%), road_density, major_road_count, minor_road_count')
    st.markdown('### Miscellaneous ')
    st.markdown('year, vehicle_type, mean_nightlight')

    st.markdown("---")
    
    # Model Results Section
    st.header("SHAP Analysis")
    
    # Display SHAP importance plot if available
    shap_importance_path = "data/ml_model_grid/shap_bar_plot.png"
    if os.path.exists(shap_importance_path):
        st.subheader("SHAP Feature Importance")
        st.image(shap_importance_path, caption="Feature importance based on SHAP values")

    shap_beeswarm_path = "data/ml_model_grid/shap_beeswarm_plot.png"
    if os.path.exists(shap_beeswarm_path):
        st.subheader("SHAP Beeswarm Plot")
        st.image(shap_beeswarm_path, caption="Feature impact on individual predictions")
    # Display partial dependence plots if available
    partial_dep_path = "data/ml_model_grid/sklearn_partial_dependence_plots.png"
    if os.path.exists(partial_dep_path):
        st.subheader("📈 Partial Dependence Analysis")
        st.image(partial_dep_path, caption="How individual features affect CO2 congestion predictions")
        
    

    
# Main function to run the page
if __name__ == "__main__":
    show_ml_model_page()
