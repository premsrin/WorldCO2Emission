import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import altair as alt
import seaborn as sns # visualization
from io import BytesIO
import numpy as np

from PIL import Image
from skimpy import clean_columns # clean column names

@st.cache
def get_co2_data_with_loc(): 
    co2_data_with_loc = pd.read_csv('./data/CO2DATA.csv', encoding = "ISO-8859-1")
    return co2_data_with_loc

@st.cache
def get_co2(): 
    co2_data = pd.read_csv("./data/CO2_EmissionByCountries.csv", encoding = "ISO-8859-1")
    return co2_data

st.set_page_config(
    page_title="World Co2 Emissions",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://en.wikipedia.org/wiki/Climate_change',
          'About': "# World CO2 Emission Analysis!"
    }
)

st.markdown("# World CO2 Emissions")
#displaying the image on streamlit app

#st.sidebar.markdown("# Home")
#st.sidebar.markdown("CO2 Emission by Country")

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

tab1, tab2, tab3, tab4 = st.tabs(['Global Warming', 'Contributors', 'Yearly CO2 Emission','Map'])

with tab1:
    image = Image.open('facecover.jpg')
    st.write("Global warming is the current rise in temperature of the air and ocean. The present global warming is mostly because of people burning things, like gasoline for cars and natural gas to keep houses warm. But the heat from the burning itself only makes the world a tiny bit warmer: it is the carbon dioxide from the burning which is the biggest part of the problem. Among greenhouse gases, the increase of carbon dioxide in the atmosphere is the main cause of global warming.")
    
    st.write("It’s widely recognised that to avoid the worst impacts of climate change, the world needs to urgently reduce emissions. Climate change has happened constantly over the history of the Earth, including the coming and going of ice ages. But modern climate change is different because people are putting carbon dioxide into the atmosphere more quickly than before")
    #st.image(image, caption='World Co2 Emissions Analysis', width= 500)

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'F-Gases', 'Nitrous Oxide', 'Methane', 'Carbon Dioxide[other land use]', 'Carbon Dioxide [Fossil Fuel and Industrial Process]'
    sizes = [2, 6, 16, 11, 65]
    explode = (0, 0, 0, 0, 0.1)

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.write("")
        st.markdown("<h5 style='text-align: center; color: white;'>Global Greenhouse Gas Emissions by Gas</h5>", unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        #fig1.suptitle('Global Greenhouse Gas Emissions by Gas', fontsize=30)
        patches, texts, autotexts = ax1.pie(sizes, explode=explode, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops=dict(color="w"))
        ax1.axis('equal')
        autotexts[4].set_fontsize(60)
        ax1.legend(labels, loc = 'lower right', bbox_to_anchor=(.6, 0, 0.5, 1))

        buf = BytesIO()
        fig1.savefig(buf, format="png")
        st.image(buf)

    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("#### Among greenhouse gases, the increase of carbon dioxide in the atmosphere is the main cause of global warming")

    with col3:
        #st.write("World Co2 Emissions")
        st.write("")
        st.markdown("<h5 style='text-align: center; color: white;'>World Co2 Emissions</h5>", unsafe_allow_html=True)        
        st.image(image, width= 450)

with tab3:
    col1, col2 = st.columns([1,1])
    with col1:
        # save the top 10 most polluting countries in a new list
        yearly_world_emission_df = df.groupby("year").sum()
        
        fig = px.line(
        yearly_world_emission_df,
        y='co2_emission_tons',
        height= 400,
        width = 200,
        title='World Yearly Co2 Emissions'
        )
        # fig.update_layout( 'plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        st.write("We can see from the graphs that world co2 emission has been increasing rapidly from 1900") 

    with col2:
        # save the top 10 most polluting countries in a new list
        top_10 = df.groupby('country')['co2_emission_tons'].sum().reset_index().sort_values(by=['co2_emission_tons'], ascending=False).head(10)['country'].tolist()
        df_10 = df[df['country'].isin(top_10)]
        fig = px.line(
        df[df['country'].isin(top_10)],
        x='year',
        y='co2_emission_tons',
        color='country',
        height= 400,
        width = 200,
        title='Time progression for top 10 co2 emitting countries'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.write("We can see from the graphs that there is a steep increase in CO2 emission of China from 1980. CO2 emission in United Kingdom is not increasing over the last few years.This reduction in co2 emission seems to be due to the Climate Change Act established by the UK government ") 

with tab2:
    top20_emission_df = df[(df.year > 2011) & (df["year"] < 2023)].groupby("country")[["co2_emission_tons"]].sum().sort_values(by=["co2_emission_tons"], ascending=False).head(20)
    col1, col2 = st.columns([1,1])
    with col1:
        fig = px.bar(
        top20_emission_df,
        x="co2_emission_tons",
        y=top20_emission_df.index,
        height= 500,
        width = 200,
        )
        # fig.update_layout( 'plotly_dark')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        st.write("These countries have emitted the highest amount of co2 in the last decade. United States is the largest emitter of co2 in the world for the last decade.")

    with col2:
        bottom20_emission_df = df[(df.year > 2011) & (df["year"] < 2023)].groupby("country")[["co2_emission_tons"]].sum().sort_values(by=["co2_emission_tons"],ascending=True).head(20)
        #bottom20_emission_df = pd.concat([top20_emission_df.head(1), bottom20_df])
        #st.write(bottom20_emission_df.head())
        fig = px.bar(
        bottom20_emission_df,
        x="co2_emission_tons",
        y=bottom20_emission_df.index,
        height= 500,
        width = 200,
        )

            # fig.update_layout( 'plotly_dark')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        st.write("The plot above shows the 20 countries in the world with the least co2 emission in the world. Antartica has the least c02 emission in the world for the last decade.")

with tab4:
    df_co2= get_co2_data_with_loc()
    # st.write(df_co2.head(10))
    #st.write(df_co2.head(10))
    #st.write(df_co2.columns.tolist())
    st.write("")
    st.write("")
    st.write("""
The graphs below show the CO2 emissions per capita for the entire world and individual countries over time.
__Hover over any of the charts to see more detail__
---
""")
    select_year = st.slider("Select year to display data from:", int(df_co2['year'].min()),int(df_co2['year'].max()),2010,10)

    fig = px.choropleth(df_co2[df_co2['year']==select_year], locations="iso_code",
                        color="co2_per_capita",
                        hover_name="country",
                        height= 700,
                        width = 700,
                        range_color=(0,25),
                        color_continuous_scale=px.colors.sequential.Reds)
    st.plotly_chart(fig, use_container_width=True)
    