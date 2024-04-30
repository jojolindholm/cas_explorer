import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Configure page layout
st.set_page_config(
    page_title = "CAS Explorer",
    layout="wide",  # or "centered"
    initial_sidebar_state="auto"  # or "expanded" or "collapsed"
)

# Change the theme
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Read and process arbitrator info
df = pd.read_csv("info_arbitrators.csv")

with st.sidebar:
    st.title("Data filters")
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

# Create n_cases histogram
n_cases_fig, ax = plt.subplots(figsize=(4, 3))
ax.hist(filtered_df['n_cases'], bins=30)
ax.set_xlabel('Number of cases')
ax.set_ylabel('Number of arbitrators')

# Create years_listed histogram
years_listed_fig, ax = plt.subplots(figsize=(4, 3))
ax.hist(filtered_df['years_listed'], bins=30)
ax.set_xlabel('Years listed')
ax.set_ylabel('Number of arbitrators')

# Display filtered data
st.title('CAS Arbitrators')
st.write(filtered_df)
st.pyplot(n_cases_fig)
st.pyplot(years_listed_fig)