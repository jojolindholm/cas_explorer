import streamlit as st
import pandas as pd
import numpy as np

# Read and process arbitrator info
df = pd.read_csv("info_arbitrators.csv")

with st.sidebar:
    st.title("Selection criteria")
    # Add dropdown menu for selection category
    delisted_checkbox = st.checkbox("Delisted", value=True)
    listed_checkbox = not st.checkbox("Listed", value=False)

    # Add sliders for customizing the data
    years_listed_min = np.nanmin(df["years_listed"])
    years_listed_max = np.nanmax(df["years_listed"])
    years_served_range = st.slider('Years served:', 
                                min_value=years_listed_min, 
                                max_value=years_listed_max, 
                                value=(years_listed_min, years_listed_max))

    n_cases_max = max(df["n_cases"])
    n_cases_range = st.slider('Cases decided:', 
                            min_value=0, 
                            max_value=n_cases_max, 
                            value=(0, n_cases_max))

    delisted_age_min = np.nanmin(df["delisted_age"])
    delisted_age_max = np.nanmax(df["delisted_age"])
    delisted_age_range = st.slider('Delisted age:',
                                min_value=delisted_age_min,
                                max_value=delisted_age_max,
                                value=(delisted_age_min, delisted_age_max))

# Add selector for country
# unique_countries = sorted(list(set(df['country'])))
# elected_country = st.selectbox('Select a country:', unique_countries)

# Filter dataframe based selection
filtered_df = df[(df['years_listed'] >= years_served_range[0]) & (df['years_listed'] <= years_served_range[1]) & 
                (df['n_cases'] >= n_cases_range[0]) & (df['n_cases'] <= n_cases_range[1]) &
                (df["delisted_age"] >= delisted_age_range[0]) & (df["delisted_age"] <= delisted_age_range[1]) &
                (df["delisted"] == delisted_checkbox)]

# Display filtered data
st.title('CAS Arbitrators')
st.write(filtered_df)