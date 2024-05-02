import streamlit as st
import streamlit_theme
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configure page layout
st.set_page_config(
    page_title = "CAS Explorer",
    layout="wide",
    initial_sidebar_state="auto"
)

# Read and process arbitrator info
df = pd.read_csv("info_arbitrators.csv")

with st.sidebar:
    st.image('images/coats_carton.png',
             width=150)
    # st.title("Data filters")
    # Add dropdown menu for selection category
    delisted_checkbox = st.checkbox("Delisted", value=True)
    listed_checkbox =  st.checkbox("Listed", value=True)

    # Add sliders for customizing the data
    years_listed_min = int(np.nanmin(df["years_listed"]))
    years_listed_max = int(np.nanmax(df["years_listed"]))
    years_served_range = st.slider('Years served:',
                                   min_value=years_listed_min,
                                   max_value=years_listed_max,
                                   value=(years_listed_min, years_listed_max))

    n_cases_max = max(df["n_cases"])
    n_cases_range = st.slider('Cases decided:',
                              min_value=0,
                              max_value=n_cases_max,
                              value=(0, n_cases_max))

    delisted_age_min = int(np.nanmin(df["delisted_age"]))
    delisted_age_max = int(np.nanmax(df["delisted_age"]))
    delisted_age_range = st.slider('Delisted age:',
                                min_value=delisted_age_min,
                                max_value=delisted_age_max,
                                value=(delisted_age_min, delisted_age_max))

# Add selector for country
# unique_countries = sorted(list(set(df['country'])))
# elected_country = st.selectbox('Select a country:', unique_countries)

# a function to filter the data based on delisted or listed
def filter_data(df, delisted=True, listed=False):
    if delisted and not listed:
        return df[df['delisted'] == 1]
    elif listed and not delisted:
        return df[df['delisted'] == 0]
    else:
        return df

# filter the data based on the selection
filtered_df = df[(df['years_listed'] >= years_served_range[0]) &
                 (df['years_listed'] <= years_served_range[1]) &
                 (df['n_cases'] >= n_cases_range[0]) &
                 (df['n_cases'] <= n_cases_range[1]) &
                 (df["delisted_age"] >= delisted_age_range[0]) &
                 (df["delisted_age"] <= delisted_age_range[1]) |
                 (pd.isnull(df["delisted_age"]))]

filtered_df = filter_data(filtered_df, delisted=delisted_checkbox, listed=listed_checkbox)

# remove columns that are not needed
filtered_df = filtered_df.drop(columns=['arb_id', 'also_known_as', 'associated_with', 'case_nums', 'delisted'])

# Create n_cases histogram
n_cases_fig, ax = plt.subplots(figsize=(5, 3))
ax.hist(filtered_df['n_cases'], 
        bins = np.nanmax(filtered_df['n_cases']) - np.nanmin(filtered_df['n_cases']) + 1)
ax.set_xlabel('Number of cases')
ax.set_ylabel('Number of arbitrators')

# Create years_listed histogram
years_listed_fig, ax = plt.subplots(figsize=(5, 3))
ax.hist(filtered_df['years_listed'].dropna(), 
        bins = 15)
ax.set_xlabel('Years listed')
ax.set_ylabel('Number of arbitrators')

# Display data
st.title('CAS Arbitrators')
col1, col2 = st.columns([2,1])  # make col1 twice as wide as col2
col1.write(filtered_df)
col2.pyplot(n_cases_fig)
col2.pyplot(years_listed_fig)