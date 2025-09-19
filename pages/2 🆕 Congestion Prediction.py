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
    
# make the page wider
    st.set_page_config(layout="wide")

    st.title("CO2 Congestion Prediction")
    st.markdown("Predicting CO2 congestion emissions at a annual level for 100 Indian cities")

    st.markdown("---")
    
    # Overview Section
    st.header("Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Objective")
        st.write("""
        Predict **CO2 congestion emissions** from traffic in Indian cities using 
        urban characteristics and transportation patterns.
        """)
        
        st.subheader("Data")
        st.write("""
        - **Cities**: 100 Indian cities
        - **Years**: 2021-2023  
        - **Vehicle Types**: 2W, 3W, LMV, HDV
        - 1200 data points
        """)
    
    with col2:
        st.subheader("Methodology")
        st.write("""
        - Random Forest Regression
        - **Target**: CO2 congestion emissions (per capita and per vkt)
        - **Predictors**: 16 urban & transport features
        - 80/20 train-test split
        - K-fold cross-validation (5 folds)
        - Metrics are reported on the test set with standard deviation from CV
        """)
        
      
    st.markdown("---")
    
    # Data Features Section
    st.header("Predictors")
    st.code(""" Population: city & state, Urban area (km²), Road length, Orientation entropy, VKT (public transport, FCD)
    Average speed, Rho_i, rho_r, rho_ratio, GDP (billion USD), Gini coefficients, Vehicle type, Year (temporal trends)
    """)


    st.markdown("---")
    
    # Model Results Section
    st.header("Analysis")
    st.markdown("Predictors related to the target variable were removed to avoid data leakage.")
    metrics_pc = pd.read_csv("data/ml_model/annual_pc/metrics.csv")
    metrics_vkt = pd.read_csv("data/ml_model/annual_vkt/metrics.csv")
    metrics_percent = pd.read_csv("data/ml_model/annual_percent/metrics.csv")
    
    # Create two columns for per capita and per vkt analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("###### Target: CO2 Congestion per capita (tons/person)")
        st.markdown("Metrics on test set")
        st.dataframe(metrics_pc, hide_index=True)
        # Display SHAP importance plot if available
        shap_importance_path = "data/ml_model/annual_pc/shap_bar_plot.png"
        if os.path.exists(shap_importance_path):
            st.subheader(" Feature Importance")
            st.image(shap_importance_path, caption="Feature importance based on SHAP values")

        shap_beeswarm_path = "data/ml_model/annual_pc/shap_beeswarm_plot.png"
        if os.path.exists(shap_beeswarm_path):
            st.subheader(" Beeswarm Plot")
            st.image(shap_beeswarm_path, caption="Feature impact on individual predictions")
            
        # Display partial dependence plots if available
        partial_dep_path = "data/ml_model/annual_pc/sklearn_partial_dependence_plots.png"
        if os.path.exists(partial_dep_path):
            st.subheader("Partial Dependence")
            st.image(partial_dep_path, caption="How individual features affect CO2 congestion predictions")

        # Display shap dependence plots if available
        shap_dep_path = "data/ml_model/annual_pc/shap_dependency_plots.png"
        if os.path.exists(shap_dep_path):
            st.subheader("SHAP Dependence")
            st.image(shap_dep_path, caption="Relationship between features and SHAP values")

    with col2:
        st.markdown("###### Target: CO2 Congestion per vkt (tons/km)")
        st.markdown("Metrics on test set")
        st.dataframe(metrics_vkt, hide_index=True)
        # Display SHAP importance plot if available
        shap_importance_path = "data/ml_model/annual_vkt/shap_bar_plot.png"
        if os.path.exists(shap_importance_path):
            st.subheader("Feature Importance")
            st.image(shap_importance_path, caption="Feature importance based on SHAP values")

        shap_beeswarm_path = "data/ml_model/annual_vkt/shap_beeswarm_plot.png"
        if os.path.exists(shap_beeswarm_path):
            st.subheader(" Beeswarm Plot")
            st.image(shap_beeswarm_path, caption="Feature impact on individual predictions")
            
        # Display partial dependence plots if available
        partial_dep_path = "data/ml_model/annual_vkt/sklearn_partial_dependence_plots.png"
        if os.path.exists(partial_dep_path):
            st.subheader("Partial Dependence")
            st.image(partial_dep_path, caption="How individual features affect CO2 congestion predictions")

        shap_dep_path = "data/ml_model/annual_vkt/shap_dependency_plots.png"
        if os.path.exists(shap_dep_path):
            st.subheader("SHAP Dependence")
            st.image(shap_dep_path, caption="Relationship between features and SHAP values")

    with col3:
        st.markdown("###### Target: CO2 Congestion as % of total emissions")
        st.markdown("Metrics on test set")
        st.dataframe(metrics_percent, hide_index=True)
        # Display SHAP importance plot if available
        shap_importance_path = "data/ml_model/annual_percent/shap_bar_plot.png"
        if os.path.exists(shap_importance_path):
            st.subheader("Feature Importance")
            st.image(shap_importance_path, caption="Feature importance based on SHAP values")

        shap_beeswarm_path = "data/ml_model/annual_percent/shap_beeswarm_plot.png"
        if os.path.exists(shap_beeswarm_path):
            st.subheader(" Beeswarm Plot")
            st.image(shap_beeswarm_path, caption="Feature impact on individual predictions")
            
        # Display partial dependence plots if available
        partial_dep_path = "data/ml_model/annual_percent/sklearn_partial_dependence_plots.png"
        if os.path.exists(partial_dep_path):
            st.subheader("Partial Dependence")
            st.image(partial_dep_path, caption="How individual features affect CO2 congestion predictions")

        shap_dep_path = "data/ml_model/annual_percent/shap_dependency_plots.png"
        if os.path.exists(shap_dep_path):
            st.subheader("SHAP Dependence")
            st.image(shap_dep_path, caption="Relationship between features and SHAP values")


# Main function to run the page
if __name__ == "__main__":
    show_ml_model_page()
