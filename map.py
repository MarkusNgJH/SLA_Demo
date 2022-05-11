import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title('Default StreamLit ST GeoMaps')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

############################################################
############################################################
############################################################

sg_lat = 1.3521
sg_long = 103.8198

DATA_URL = 'https://api.data.gov.sg/v1/transport/taxi-availability'
json = requests.get(DATA_URL).json()
df = pd.DataFrame(json["features"][0]["geometry"]["coordinates"])
df['third'] = 0
df.columns = ['long', 'lat', 'extra']
df['long'] = pd.to_numeric(df.long, errors='coerce')
df['lat'] = pd.to_numeric(df.lat, errors='coerce')
st.write(df.head())

############################################################
############################################################
############################################################

# from streamlit_keplergl import keplergl_static
# from keplergl import KeplerGl

# st.title('KeplerGl Maps')
# map_1 = KeplerGl(data={'Data': df})
# config = {
# 'version': 'v1',
# 'config': {
#     'mapState': {
#         'latitude': sg_lat,
#         'longitude': sg_long,
#         'zoom': 10
#     	}
# 	}
# }

# map_1.config = config
# map_1.add_data(data=df, name="extra")
# keplergl_static(map_1)

############################################################
############################################################
############################################################
import pydeck as pdk
st.title('PyDeck Maps')
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
