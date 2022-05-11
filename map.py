import streamlit as st
import pandas as pd
import numpy as np
import requests
from random import randint, random

@st.cache
def load_data(nrows):
    # Insert Code for Actual Data Source Here
    DATA_URL = 'https://api.data.gov.sg/v1/transport/taxi-availability'
    json = requests.get(DATA_URL).json()
    df = pd.DataFrame(json["features"][0]["geometry"]["coordinates"])
    df['count'] = 1
    df.columns = ['long', 'lat', 'count']
    return df[:nrows]

def predict_lease():
    # Insert Code for Price Prediction Model here. Or Link from external file
    predicted_lease = randint(100000,1000000)
    format_predicted_lease = "$ " + "{:,}".format(predicted_lease)
    lease_change = round(random(),1)
    format_lease_change = str(lease_change) + " %"
    return (format_predicted_lease, format_lease_change)

def validate_postal_code(postal_code):
    # Insert Code for user input validation
    if len(postal_code) == 6:
        return True
    else:
        return False

############################################################
############################################################

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

df = load_data(10000)
sg_lat = 1.3521
sg_long = 103.8198

############################################################
############################################################

# Main Body of Dashboard
st.title('Lease Prediction')

st.header("Explore Lease Prices Here")
st.dataframe(df)

st.header("Lease Prices Prediction")
with st.expander("Input Property Details for Prediction"):
    with st.form(key="predict_form"):
        postal_code = st.text_input('Postal Code?', value = "000000")
        bdrm = st.selectbox('Number of Bedroom?',('1Bdrm', '2Bdrm', '3Bdrm', '4Bdrm', '5Bdrm'))
        prop_type = st.selectbox('Property Type?',('HDB', 'Condo', 'Landed'))
        age = st.number_input("Age of Property?", 0, 50)
        submit_button = st.form_submit_button("Predict")
        if submit_button and validate_postal_code(postal_code):
            st.write('Prediction Completed')
            predicted, delta = predict_lease()
            st.metric('Predicted Lease', predicted, delta = delta, delta_color="normal")
        elif submit_button and not validate_postal_code(postal_code):
            st.error("Please Check Input")
            

############################################################
############################################################
############################################################

# Main Body of Geospatial Maps
import pydeck as pdk
st.header("Look at Map Lease Prices")

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(latitude= sg_lat,longitude= sg_long,zoom= 10),
    layers = [pdk.Layer(
        'ScreenGridLayer',
        df,
        get_position=['long', 'lat'],
        cell_size_pixels=20,
        pickable=True,
        auto_highlight=True,
        get_weight="count"
        ) 
    ],
    # Tooltips works for HeatMap but not for ScreenGridLayer
    tooltip = {
    "style": {"color": "white"},
    "html": "Taxi Count: {colorValue}" 
    }
 ))
