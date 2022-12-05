import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import altair as alt
import seaborn as sns # visualization
from io import BytesIO
import numpy as np

from skimpy import clean_columns # clean column names


@st.cache
def get_co2(): 
    co2_data = pd.read_csv("./data/CO2_EmissionByCountries.csv", encoding = "ISO-8859-1")
    return co2_data


st.markdown("# CO2 Emission By Country")
#st.sidebar.markdown("# CO2 Emission By Country")
#st.set_page_config(page_title="Plotting Demo")

df = get_co2()
df = clean_columns(df)
df.columns.tolist()
df.rename(columns = {"co_2_emission_tons":"co2_emission_tons", "density_km_2":"density(km2)", "%_of_world":"percentage_of_world"}, inplace = True)

#st.write(df.head())
COUNTRIES = df['country'].unique()
COUNTRIES_SELECTED = st.sidebar.multiselect('Select countries', COUNTRIES,default=['India', 'China', 'United Kingdom' ])

# Mask to filter dataframe
mask_countries = df['country'].isin(COUNTRIES_SELECTED)

data = df[mask_countries]
#st.write(data.head())

# save the top 10 most polluting countries in a new list
FinalData = data.groupby('country')['co2_emission_tons'].sum().reset_index().sort_values(by=['co2_emission_tons'], ascending=False).head(10)['country'].tolist()
fig = px.line(
data,
x='year',
y='co2_emission_tons',
color='country',
height= 600,
width = 400,
title='Time progression for selected countries'
)
st.plotly_chart(fig, use_container_width=True)
