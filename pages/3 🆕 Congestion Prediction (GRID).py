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
    st.markdown("Predicting CO2 congestion emissions at a 500m grid level for Mumbai, Delhi and Hyderabad")
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
        - **Cities**: Mumbai, Delhi, Hyderabad (grids of 500m x 500m)
        - **Years**: 2021-2023  
        - **Vehicle Types**: 2W, 3W, LMV, HDV
        - 48840 data points
        """)
    
    with col2:
        st.subheader("Methodology")
        st.write("""
        - Random Forest Regression
        - **Target**: CO2 congestion emissions (per capita and per vkt)
        - **Predictors**: 30 urban & transport gridded features
        - 80/20 train-test split
        """)
        
    
    st.markdown("---")
    
    # Data Features Section
    st.header("Predictors")
    st.markdown('### Points of interest ')
    st.markdown('Gas_stations, Businesses, Community_centers, Edu_institutions, Entertainment, Financial_institutions, Hospitals, Landmark, Major_highways, Parks_recreation, Parking, Rail_roads, Restaurants, Secondary_highways, Shopping, Transportation_hubs, Hotels, Water_bodies, Rivers')
    st.markdown('### Road network ')
    st.markdown('Avg_speed, road_length,  major_road(%), minor_road(%), road_density, major_road_count, minor_road_count')
    st.markdown('### Miscellaneous ')
    st.markdown('year, vehicle_type, mean_nightlight, population')

    st.markdown("---")
    

    # select city
    city = st.selectbox("Select a city", ["Mumbai", "Delhi", "Hyderabad"])
    # Model Results Section
    st.header("SHAP Analysis")
    metrics_pc = pd.read_csv(f"data/ml_model/grid_pc/{city.lower()}/metrics.csv")
    metrics_vkt = pd.read_csv(f"data/ml_model/grid_vkt/{city.lower()}/metrics.csv")
    metrics_percent = pd.read_csv(f"data/ml_model/grid_percent/{city.lower()}/metrics.csv")

    # Create two columns for per capita and per vkt analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### Target: CO2 Congestion Emissions per capita (tons/person)")
        st.dataframe(metrics_pc, hide_index=True)
        # Display SHAP importance plot if available
        shap_importance_path = f"data/ml_model/grid_pc/{city.lower()}/shap_bar_plot.png"
        if os.path.exists(shap_importance_path):
            st.subheader(" Feature Importance")
            st.image(shap_importance_path, caption="Feature importance based on SHAP values")

        shap_beeswarm_path = f"data/ml_model/grid_pc/{city.lower()}/shap_beeswarm_plot.png"
        if os.path.exists(shap_beeswarm_path):
            st.subheader(" Beeswarm Plot")
            st.image(shap_beeswarm_path, caption="Feature impact on individual predictions")
            
        # Display partial dependence plots if available
        partial_dep_path = f"data/ml_model/grid_pc/{city.lower()}/sklearn_partial_dependence_plots.png"
        if os.path.exists(partial_dep_path):
            st.subheader("Partial Dependence")
            st.image(partial_dep_path, caption="How individual features affect CO2 congestion predictions")

        # Display shap dependence plots if available
        shap_dep_path = f"data/ml_model/grid_pc/{city.lower()}/shap_dependency_plots.png"
        if os.path.exists(shap_dep_path):
            st.subheader("SHAP Dependence")
            st.image(shap_dep_path, caption="Feature impact on individual predictions")
    
    with col2:
        st.markdown("##### Target: CO2 Congestion Emissions per vkt (tons/km)")
        st.dataframe(metrics_vkt, hide_index=True)
        # Display SHAP importance plot if available
        shap_importance_path = f"data/ml_model/grid_vkt/{city.lower()}/shap_bar_plot.png"
        if os.path.exists(shap_importance_path):
            st.subheader("Feature Importance")
            st.image(shap_importance_path, caption="Feature importance based on SHAP values")

        shap_beeswarm_path = f"data/ml_model/grid_vkt/{city.lower()}/shap_beeswarm_plot.png"
        if os.path.exists(shap_beeswarm_path):
            st.subheader(" Beeswarm Plot")
            st.image(shap_beeswarm_path, caption="Feature impact on individual predictions")
            
        # Display partial dependence plots if available
        partial_dep_path = f"data/ml_model/grid_vkt/{city.lower()}/sklearn_partial_dependence_plots.png"
        if os.path.exists(partial_dep_path):
            st.subheader("Partial Dependence")
            st.image(partial_dep_path, caption="How individual features affect CO2 congestion predictions")

        # Display shap dependence plots if available
        shap_dep_path = f"data/ml_model/grid_vkt/{city.lower()}/shap_dependency_plots.png"
        if os.path.exists(shap_dep_path):
            st.subheader("SHAP Dependence")
            st.image(shap_dep_path, caption="Feature impact on individual predictions")
        
    with col3:
        st.markdown("##### Target: CO2 Congestion Emissions as % of total emissions")
        st.dataframe(metrics_percent, hide_index=True)
        # Display SHAP importance plot if available
        shap_importance_path = f"data/ml_model/grid_percent/{city.lower()}/shap_bar_plot.png"
        if os.path.exists(shap_importance_path):
            st.subheader("Feature Importance")
            st.image(shap_importance_path, caption="Feature importance based on SHAP values")

        shap_beeswarm_path = f"data/ml_model/grid_percent/{city.lower()}/shap_beeswarm_plot.png"
        if os.path.exists(shap_beeswarm_path):
            st.subheader(" Beeswarm Plot")
            st.image(shap_beeswarm_path, caption="Feature impact on individual predictions")
            
        # Display partial dependence plots if available
        partial_dep_path = f"data/ml_model/grid_percent/{city.lower()}/sklearn_partial_dependence_plots.png"
        if os.path.exists(partial_dep_path):
            st.subheader("Partial Dependence")
            st.image(partial_dep_path, caption="How individual features affect CO2 congestion predictions")

        # Display shap dependence plots if available
        shap_dep_path = f"data/ml_model/grid_percent/{city.lower()}/shap_dependency_plots.png"
        if os.path.exists(shap_dep_path):
            st.subheader("SHAP Dependence")
            st.image(shap_dep_path, caption="Feature impact on individual predictions")


# Main function to run the page
if __name__ == "__main__":
    show_ml_model_page()
