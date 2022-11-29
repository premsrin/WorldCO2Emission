import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import altair as alt
import seaborn as sns # visualization

from PIL import Image
from skimpy import clean_columns # clean column names

@st.cache
def get_co2_data_with_loc(): 
    # OWID Data on CO2 and Greenhouse Gas Emissions
    # Creative Commons BY license
    CO2DATA = pd.read_csv('./data/CO2DATA.csv', encoding = "ISO-8859-1")
    return CO2DATA

@st.cache
def get_co2(): 
    # OWID Data on CO2 and Greenhouse Gas Emissions
    # Creative Commons BY license
    df = pd.read_csv("./data/CO2_EmissionByCountries.csv", encoding = "ISO-8859-1")
    return df

#st.set_page_config(layout = "wide")

st.markdown("# World Co2 Emissions")
#displaying the image on streamlit app


st.sidebar.markdown("# Home")
st.sidebar.markdown("CO2 Emission by Vehicles and Flights")

#Data Cleansing
df = get_co2()
df = clean_columns(df)
df.columns.tolist()
df.rename(columns = {"co_2_emission_tons":"co2_emission_tons", "density_km_2":"density(km2)", "%_of_world":"percentage_of_world"}, inplace = True)

df["percentage_of_world"] = df["percentage_of_world"].str.replace("%", "", regex=True)
df["percentage_of_world"] = df["percentage_of_world"].astype(float)

df["density(km2)"] = df["density(km2)"].str.replace("/km²", "", regex=True)
df["density(km2)"] = df["density(km2)"].str.replace(',','.', regex=True)
df["density(km2)"] = df["density(km2)"].astype(float)

tab0, tab1, tab2, tab3, tab4 = st.tabs(['Co2 Emissions', 'World Yearly CO2 Emission','Top 20 Countries','Bottom 20 countries','Map'])

with tab0:
    image = Image.open('facecover.jpg')
    col1, col2 = st.columns([3,1])
    with col1:
        st.write("Carbon dioxide(CO2) emissions are the primary driver of global climate change. It’s widely recognised that to avoid the worst impacts of climate change, the world needs to urgently reduce emissions")
        #st.image(image, caption='World Co2 Emissions Analysis', width= 500)

    with col2:
        st.write("")
        st.image(image, caption='World Co2 Emissions', width= 300)

with tab1:
    yearly_world_emission_df = df.groupby("year").sum()
    fig = plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    plt.plot(yearly_world_emission_df.index, yearly_world_emission_df["co2_emission_tons"])
    plt.title("World yearly CO2 emission");
    top20_emission_df = df[(df.year > 2011) & (df["year"] < 2023)].groupby("country")[["co2_emission_tons"]].sum().sort_values(by=["co2_emission_tons"], ascending=False).head(20)
    st.pyplot(fig)

with tab2:
    fig = plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    sns.barplot(data=top20_emission_df, x="co2_emission_tons", y=top20_emission_df.index, palette="bright")
    plt.title("Top 20 CO2 emitting countries from 2012 - 2022")
    plt.xlabel("CO2 emission in tons")
    plt.ylabel("Countries");
    st.pyplot(fig)

with tab3:
    bottom20_emission_df = df[(df.year > 2011) & (df["year"] < 2023)].groupby("country")[["co2_emission_tons"]].sum().sort_values(by=["co2_emission_tons"]).head(20)
    fig = plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    sns.barplot(data=top20_emission_df, x="co2_emission_tons", y=bottom20_emission_df.index, palette="bright")
    plt.title("Bottom 20 CO2 emitting countries from 2012 - 2022")
    plt.xlabel("CO2 emission in tons")
    plt.ylabel("Countries");
    st.pyplot(fig)

with tab4:
    df_co2= get_co2_data_with_loc()
    # st.write(df_co2.head(10))
    #st.write(df_co2.head(10))
    #st.write(df_co2.columns.tolist())
    st.write("")
    st.write("")
    
    select_year = st.slider("Select year to display data from:", int(df_co2['year'].min()),int(df_co2['year'].max()),int(df_co2['year'].max()),10)
    fig = px.choropleth(df_co2[df_co2['year']==select_year], locations="iso_code",
                        color="co2_per_capita",
                        hover_name="country",
                        range_color=(0,25),
                        color_continuous_scale=px.colors.sequential.Reds)
    st.plotly_chart(fig, use_container_width=True)


