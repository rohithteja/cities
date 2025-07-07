import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google import genai
from google.genai import types
import os


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

# Load the data
df = pd.read_csv(f'data/df_stats_streamlit.csv')
df['vkt_pc'] = df['vkt'] / df['population_2020']
df['consumption_pc'] = df['consumption'] / df['population_2020']
years = [2021, 2022, 2023]

st.markdown('''
* Number of cities: ''' + str(len(df.city.unique())) + '''
* Years: ''' + str(years) + '''
* Vehicle types: ''' + str(df.vehicle.unique()) + '''
''')

# remove all rows with city panaji
df = df[df['city'] != 'jabalpur']
df = df[df['city'] != 'panaji']

df["co2_per_gdp"] = df["co2"] / df["gdp_billions"]    # tonnes/billions usd
df["gdp_per_fuel"] = df["gdp_billions"] / df["consumption"] # billions usd/tonnes
df["fuel_per_km"] = df["consumption"] / df["vkt"]      # tonnes/km
df["vkt_per_capita"] = df["vkt"] / df["population_2020"]   # km/person
df["co2_per_fuel"] = df["co2"] / df["consumption"]          # tonnes/tonne fuel

df["fuel_per_capita"] = df["consumption"] / df["population_2020"]   # tonnes or liters per person
df["urban_density"] = df["population_2020"] / df["urban_area_km2"]  # people per km²
df['sqrt_urban_area'] = np.sqrt(df['urban_area_km2'])

df['co2_congestion_pc'] = df['co2_congestion'] / df['population_2020']  # CO₂ congestion per capita
df['co2_ff_pc'] = df['co2_ff'] / df['population_2020']  # Freeflow CO₂ per capita


# Only run this block for Gemini Developer API
client = genai.Client(api_key='AIzaSyBJ3PU3NUHCNdK30f7Nyh59yUj6p_3Ka4c')

model_name = "gemini-1.5-pro-002"

try:
  cache = client.caches.create(
      model=model_name,
      config=types.CreateCachedContentConfig(
          contents=[df.to_json(orient='records')],
          system_instruction="You are an expert in urban transportation and CO₂ emissions. This is a dataset with statistics about Indian cities. Use this data to answer questions about urban transportation, CO₂ emissions, and related topics.",
      ),
  )
except:
  pass

# --- Streamlit App ---
st.title("Gemini API Q&A")

st.write("Data preview:")
st.dataframe(df.head())
question = st.text_input("Ask a question about the data:")

if question:
  # Call Gemini 
  response = client.models.generate_content(
      model=model_name,
      contents=question,
      config=types.GenerateContentConfig(cached_content=cache.name),
  )

  st.markdown("### Answer:")
  st.write(response.text)

