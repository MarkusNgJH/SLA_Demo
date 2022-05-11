import streamlit as st
import pandas as pd
import numpy as np
import requests
from random import randint, random


st.title('Lease Prediction')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    DATA_URL = 'https://api.data.gov.sg/v1/transport/taxi-availability'
    json = requests.get(DATA_URL).json()
    df = pd.DataFrame(json["features"][0]["geometry"]["coordinates"])
    df.columns = ['long', 'lat']
    return df[:nrows]

df = load_data(10000)

############################################################
############################################################
############################################################

sg_lat = 1.3521
sg_long = 103.8198

st.header("Explore Lease Prices Here")
st.dataframe(df)

st.header("Lease Prices Prediction")
with st.expander("Input Property Details for Prediction"):
    location = st.text_input('Postal Code?')
    bdrm = st.selectbox('Number of Bedroom?',('1Bdrm', '2Bdrm', '3Bdrm', '4Bdrm', '5Bdrm'))
    prop_type = st.selectbox('Property Type?',('HDB', 'Condo', 'Landed'))
    age = st.number_input("Age of Property?", 0, 50)
    
clicked = st.button("Run Prediction")
if clicked:
    st.write('Prediction Completed')
    predicted = "$ " + "{:,}".format(randint(100000,1000000))
    delta = str(round(random(),1)) + " %"
    st.metric('Predicted Lease', predicted, delta = delta, delta_color="normal")

############################################################
############################################################
############################################################
import pydeck as pdk
st.header("Look at Map Lease Prices")
st.pydeck_chart(pdk.Deck(
     initial_view_state=pdk.ViewState(
        latitude= sg_lat,
        longitude= sg_long,
        zoom= 10
     ),
    layers = [pdk.Layer(
        'ScreenGridLayer',
        df,
        get_position=['long', 'lat'],
        cell_size_pixels=20,
        pickable=True,
        auto_highlight=True     
        ) 
    ]
 ))
