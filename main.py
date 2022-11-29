import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import altair as alt
import seaborn as sns # visualization
from io import BytesIO

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

st.sidebar.markdown("# Home")
st.sidebar.markdown("CO2 Emission by Country")

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

tab1, tab2, tab3, tab4 = st.tabs(['Global Warming', 'Yearly CO2 Emission','Contributors','Map'])

with tab1:
    image = Image.open('facecover.jpg')
    st.write("Global warming is the current rise in temperature of the air and ocean. The present global warming is mostly because of people burning things, like gasoline for cars and natural gas to keep houses warm. But the heat from the burning itself only makes the world a tiny bit warmer: it is the carbon dioxide from the burning which is the biggest part of the problem. Among greenhouse gases, the increase of carbon dioxide in the atmosphere is the main cause of global warming.")
    
    st.write("It’s widely recognised that to avoid the worst impacts of climate change, the world needs to urgently reduce emissions. Climate change has happened constantly over the history of the Earth, including the coming and going of ice ages. But modern climate change is different because people are putting carbon dioxide into the atmosphere more quickly than before")
    #st.image(image, caption='World Co2 Emissions Analysis', width= 500)

    st.write("")
    st.image(image, caption='World Co2 Emissions', width= 400)

with tab2:
    col1, col2 = st.columns([1,1])
    with col1:
        # save the top 10 most polluting countries in a new list
        yearly_world_emission_df = df.groupby("year").sum()
        fig = px.line(
        yearly_world_emission_df,
        y='co2_emission_tons',
        template = 'seaborn',
        height= 400,
        width = 200,
        )
        st.plotly_chart(fig, use_container_width=True)

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
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    top20_emission_df = df[(df.year > 2011) & (df["year"] < 2023)].groupby("country")[["co2_emission_tons"]].sum().sort_values(by=["co2_emission_tons"], ascending=False).head(20)
    col1, col2 = st.columns([1,1])
    with col1:
        fig = plt.figure(figsize=(6, 4))
        sns.set_style("whitegrid")
        sns.barplot(data=top20_emission_df, x="co2_emission_tons", y=top20_emission_df.index, palette="bright")
        plt.title("Top 20 CO2 emitting countries from 2012 - 2022")
        plt.xlabel("CO2 emission in tons")
        plt.ylabel("Countries");
        #st.pyplot(fig)

        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)

    with col2:
        bottom20_emission_df = df[(df.year > 2011) & (df["year"] < 2023)].groupby("country")[["co2_emission_tons"]].sum().sort_values(by=["co2_emission_tons"]).head(20)
        fig = plt.figure(figsize=(6, 4))
        sns.set_style("whitegrid")
        sns.barplot(data=top20_emission_df, x="co2_emission_tons", y=bottom20_emission_df.index, palette="bright")
        plt.title("Bottom 20 CO2 emitting countries from 2012 - 2022")
        plt.xlabel("CO2 emission in tons")
        plt.ylabel("Countries");
        #st.pyplot(fig)
        
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)

with tab4:
    df_co2= get_co2_data_with_loc()
    # st.write(df_co2.head(10))
    #st.write(df_co2.head(10))
    #st.write(df_co2.columns.tolist())
    st.write("")
    st.write("")
    
    select_year = st.slider("Select year to display data from:", int(df_co2['year'].min()),int(df_co2['year'].max()),2010,10)

    fig = px.choropleth(df_co2[df_co2['year']==select_year], locations="iso_code",
                        color="co2_per_capita",
                        hover_name="country",
                        height= 700,
                        width = 700,
                        range_color=(0,25),
                        color_continuous_scale=px.colors.sequential.Reds)
    st.plotly_chart(fig, use_container_width=True)
    
