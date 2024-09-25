import streamlit as st
import folium
from streamlit_folium import st_folium

from utils.prediction import make_moscow_map


st.markdown("## Выберите точку на карте или введите ее координаты")

st.caption("Для выбора кликните по карте")
map = make_moscow_map()

out = st_folium(map)


st.write("Координаты точки:")

point = {
    "geo_lat": 55.755864,
    "geo_lng": 37.617698,
}


try:
    lat = st.number_input(
        "Широта",
        value=out["last_clicked"]["lat"],
        placeholder=f"{point["geo_lat"]}",
        key="lat",
        format="%0.6f",
    )
    lng = st.number_input(
        "Долгота",
        value=out["last_clicked"]["lng"],
        placeholder=f"{point["geo_lng"]}",
        key="lng",
        format="%0.6f",
    )
    point["geo_lat"] = lat
    point["geo_lng"] = lng

except Exception:
    lat = st.number_input(
        "Широта",
        value=point["geo_lat"],
        key="lat",
        format="%0.6f",
    )
    lng = st.number_input(
        "Долгота",
        value=point["geo_lng"],
        key="lng",
        format="%0.6f",
    )
    point["geo_lat"] = lat
    point["geo_lng"] = lng

    pass

st.write(point)

st.markdown("### Ближайшая станция метро")
st.write("Metro")

st.markdown("## Площадь")
st.markdown("### Общая")
st.markdown("### Жилая")
st.markdown("### Кухни")

st.markdown("## Высота потолков")

st.markdown("## Количество комнат")
st.markdown("## Этажность")
st.markdown("## Аварийность")
st.markdown("## Тип жилья")
