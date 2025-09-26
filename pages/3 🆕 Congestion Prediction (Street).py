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

    st.title("CO2 Congestion Prediction (Street)")
    st.markdown("Predicting CO2 congestion emissions at a street level for Mumbai")
    st.markdown("---")
    
    # Overview Section
    st.header("Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Objective")
        st.write("""
        Predict **CO2 congestion emissions** from traffic for streets in Indian cities (Mumbai) using 
        urban characteristics and transportation patterns.
        """)
        
        st.subheader("Data")
        st.write("""
        - **Cities**: Mumbai (street level)
        - **Years**: 2021 
        - **Vehicle Types**: Aggregate emissions (all vehicle types)
        - 100k+ data points
        """)
    
    with col2:
        st.subheader("Methodology")
        st.write("""
        - Random Forest Regression
        - **Target**: CO2 congestion emissions (per vkt, % of total emissions)
        - **Predictors**: ~49 urban & street level features
        - K-fold cross-validation (5 folds)
        - Metrics are reported on the test set with standard deviation from CV
        - Metrics: R², wMAPE (weighted Mean Absolute Percentage Error)
        """)
        
    
    st.markdown("---")
    
    # Data Features Section
    st.header("Predictors")
    st.markdown('### Points of interest ')
    st.markdown('Gas_stations, Businesses, Community_centers, Edu_institutions, Entertainment, Financial_institutions, Hospitals, Landmark, Major_highways, Parks_recreation, Parking, Rail_roads, Restaurants, Secondary_highways, Shopping, Transportation_hubs, Hotels, Water_bodies, Rivers')
    st.markdown('### Road network and Graph features')
    st.markdown('Road_length, VKT, Road_type, Source_degree, Target_degree,\
Source_in_degree, Source_out_degree, Target_in_degree,\
       Target_out_degree, Avg_degree, Avg_in_degree, Avg_out_degree,\
       Degree_diff, Source_clustering, Target_clustering,\
       Source_pagerank, Target_pagerank, Source_degree_centrality,\
       Target_degree_centrality, Source_in_degree_centrality,\
       Target_in_degree_centrality, Source_out_degree_centrality,\
       Target_out_degree_centrality, Avg_clustering, Avg_pagerank,\
       Avg_degree_centrality, Clustering_diff, Pagerank_diff,\
       Degree_centrality_diff, Betweeness_Centrality')
    st.markdown('### Miscellaneous ')
    st.markdown( 'Latitude, Longitude')


    st.markdown("---")
    

    # Analysis Selection
    st.header("Analysis")
    st.markdown("""
                2 types of target variables were modeled: 
                - CO2 Congestion per vkt (Infrastructure context)
                - CO2 Congestion as a percentage of total emissions (Environmental context)""")
    st.markdown("(Predictors related to the target variable were removed to avoid data leakage." \
    " So there are minor changes to predictor list for each target variable.)")
    st.divider()

    cities = ["Mumbai"]  # Currently only Mumbai is available
    for city in cities:
        
        # Load metrics for all targets
        metrics_vkt = pd.read_csv(f"data/ml_model/street_vkt/{city.lower()}/metrics.csv")
        metrics_percent = pd.read_csv(f"data/ml_model/street_percent/{city.lower()}/metrics.csv")
        
        st.subheader(f"Model Performance for {city}")
        # Create two columns for different targets
        col1, col2 = st.columns(2)

        targets = [
            ("vkt", "CO2 Congestion per vkt (tons/km)", metrics_vkt),
            ("percent", "CO2 Congestion as % of total emissions", metrics_percent)
        ]
        
        columns = [col1, col2]
        
        for i, (target_key, target_name, metrics_df) in enumerate(targets):
            with columns[i]:
                st.markdown(f"###### Target: {target_name}")
                # Select first two and last two columns
                cols_to_show = list(metrics_df.columns[:2]) + list(metrics_df.columns[-2:])
                st.dataframe(metrics_df[cols_to_show], hide_index=True)
                
                # Display plots for this target
                base_path = f"data/ml_model/street_{target_key}/{city.lower()}"
                
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

    



# Main function to run the page
if __name__ == "__main__":
    show_ml_model_page()
