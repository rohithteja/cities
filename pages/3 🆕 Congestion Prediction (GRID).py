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
    st.set_page_config(layout="wide")

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
        - **Cities**: Mumbai, Bengaluru, Hyderabad (grids of 500m x 500m)
        - **Years**: 2021-2023  
        - **Vehicle Types**: 2W, 3W, LMV, HDV
        - ~15k-60k data points
        """)
    
    with col2:
        st.subheader("Methodology")
        st.write("""
        - Random Forest Regression
        - **Target**: CO2 congestion emissions (per capita, per vkt, % of total emissions)
        - **Predictors**: ~30 urban & transport gridded features
        - K-fold cross-validation (5 folds)
        - Metrics are reported on the test set with standard deviation from CV
        - Metrics: R², RRMSE (Relative Root Mean Squared Error)
        - Note: Values of RRMSE >1 is due to skewed distribution of target variable
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
    

    # Analysis Selection
    st.header("Analysis")
    st.markdown("""
                3 types of target variables were modeled: 
                - CO2 Congestion per capita (Social context)
                - CO2 Congestion per vkt (Infrastructure context)
                - CO2 Congestion as a percentage of total emissions (Environmental context)""")
    st.markdown("(Predictors related to the target variable were removed to avoid data leakage." \
    " So there are minor changes to predictor list for each target variable.)")
    st.divider()
    # Create selection options
    analysis_type = st.radio(
        "Choose analysis type:",
        ["Compare 3 targets for one city", "Compare 3 cities for one target"],
        horizontal=True
    )

    if analysis_type == "Compare 3 targets for one city":
        # Select city
        city = st.selectbox("Select a city", ["Mumbai", "Bengaluru", "Delhi"])
        
        # Load metrics for all targets
        metrics_pc = pd.read_csv(f"data/ml_model/grid_pc/{city.lower()}/metrics.csv")
        metrics_vkt = pd.read_csv(f"data/ml_model/grid_vkt/{city.lower()}/metrics.csv")
        metrics_percent = pd.read_csv(f"data/ml_model/grid_percent/{city.lower()}/metrics.csv")
        
        st.subheader(f"Model Performance for {city}")
        
        # Create three columns for different targets
        col1, col2, col3 = st.columns(3)
        
        targets = [
            ("pc", "CO2 Congestion per capita (tons/person)", metrics_pc),
            ("vkt", "CO2 Congestion per vkt (tons/km)", metrics_vkt),
            ("percent", "CO2 Congestion as % of total emissions", metrics_percent)
        ]
        
        columns = [col1, col2, col3]
        
        for i, (target_key, target_name, metrics_df) in enumerate(targets):
            with columns[i]:
                st.markdown(f"###### Target: {target_name}")
                # Select first two and last two columns
                cols_to_show = list(metrics_df.columns[:2]) + list(metrics_df.columns[-2:])
                st.dataframe(metrics_df[cols_to_show], hide_index=True)
                
                # Display plots for this target
                base_path = f"data/ml_model/grid_{target_key}/{city.lower()}"
                
                plots = [
                    ("shap_bar_plot.png", "Feature Importance", "Feature importance based on SHAP values"),
                    ("shap_beeswarm_plot.png", "Beeswarm Plot", "Feature impact on individual predictions"),
                    ("sklearn_partial_dependence_plots.png", "Partial Dependence", "How individual features affect CO2 congestion predictions"),
                    ("shap_dependency_plots.png", "SHAP Dependence", "Feature impact on individual predictions")
                ]
                
                for plot_file, plot_title, plot_caption in plots:
                    plot_path = f"{base_path}/{plot_file}"
                    if os.path.exists(plot_path):
                        st.subheader(plot_title)
                        st.image(plot_path, caption=plot_caption)

    else:  # Compare 3 cities for one target
        # Select target
        target_option = st.selectbox(
            "Select target variable",
            ["CO2 Congestion per capita (tons/person)", 
             "CO2 Congestion per vkt (tons/km)", 
             "CO2 Congestion as % of total emissions"]
        )
        
        # Map selection to target key
        target_mapping = {
            "CO2 Congestion per capita (tons/person)": "pc",
            "CO2 Congestion per vkt (tons/km)": "vkt",
            "CO2 Congestion as % of total emissions": "percent"
        }
        target_key = target_mapping[target_option]
        
        st.subheader(f"Model Performance Comparison: {target_option}")
        
        # Create three columns for different cities
        col1, col2, col3 = st.columns(3)
        cities = ["Mumbai", "Bengaluru", "Delhi"]
        columns = [col1, col2, col3]
        
        for i, city in enumerate(cities):
            with columns[i]:
                st.markdown(f"###### {city}")
                
                # Load metrics for this city and target
                metrics_path = f"data/ml_model/grid_{target_key}/{city.lower()}/metrics.csv"
                if os.path.exists(metrics_path):
                    metrics_df = pd.read_csv(metrics_path)
                    cols_to_show = list(metrics_df.columns[:2]) + list(metrics_df.columns[-2:])
                    st.dataframe(metrics_df[cols_to_show], hide_index=True)

                    # Display plots for this city and target
                    base_path = f"data/ml_model/grid_{target_key}/{city.lower()}"
                    
                    plots = [
                        ("shap_bar_plot.png", "Feature Importance", "Feature importance based on SHAP values"),
                        ("shap_beeswarm_plot.png", "Beeswarm Plot", "Feature impact on individual predictions"),
                        ("sklearn_partial_dependence_plots.png", "Partial Dependence", "How individual features affect CO2 congestion predictions"),
                        ("shap_dependency_plots.png", "SHAP Dependence", "Feature impact on individual predictions")
                    ]
                    
                    for plot_file, plot_title, plot_caption in plots:
                        plot_path = f"{base_path}/{plot_file}"
                        if os.path.exists(plot_path):
                            st.subheader(plot_title)
                            st.image(plot_path, caption=plot_caption)
                else:
                    st.warning(f"Data not available for {city}")



# Main function to run the page
if __name__ == "__main__":
    show_ml_model_page()
