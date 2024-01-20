import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import io

st.title('Hello World!!!!')

DATE_COLUMN = 'date/time'
DATA_PATH = ("https://s3-us-west-2.amazonaws.com/"
             "streamlit-demo-data/uber-raw-data-sep14.csv.gz")

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_PATH, nrows=nrows)
    data.rename(lambda x: str(x).lower(), axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data...done!')

#画像加工(gamma)
uploaded_picture = st.file_uploader("Uploade picutre.", type="jpg")
if uploaded_picture:
    gamma = st.slider('Gamma', 0.0, 2.0, 1.0, step=0.1)
    if gamma == 0:
        gamma = 0.01
    img = Image.open(uploaded_picture)
    max_pixel_value = np.amax(img)
    img_gamma = max_pixel_value * (img / max_pixel_value) ** (1 / gamma)
    img_gamma = img_gamma.astype(np.uint8)
    st.image(img_gamma, 
        caption='Uploaded picture', 
        use_column_width="auto")
    
    #ダウンロードボタン
    img_gamma_pillow = Image.fromarray(img_gamma)
    img_bytes = io.BytesIO()
    img_gamma_pillow.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
    st.download_button(
        label="Download gamma picture",
        data=img_bytes,
        file_name="gamma.jpg",
        mime="image/jpg"
    )

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

fig, ax = plt.subplots()
ax.scatter(data.lon, data.lat)
st.pyplot(fig)

with st.sidebar:
    page = st.selectbox("aaaa", ("page1", "page2", "page3"))
