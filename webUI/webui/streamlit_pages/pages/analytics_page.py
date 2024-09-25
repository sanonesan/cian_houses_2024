import streamlit as st
from streamlit_folium import st_folium

from utils.analytics import cian_houses_map


PATH_HOUSES = "./data/cian_houses_dataset.csv"

st.header("Аналитика")
st.subheader("Карта квартир")
m = cian_houses_map(PATH_HOUSES)
st_folium(m)
