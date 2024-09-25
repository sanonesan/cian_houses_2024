import streamlit as st
import pandas as pd

import folium
from folium.plugins import Draw, MarkerCluster, GroupedLayerControl

__all__ = ["cian_houses_map"]


@st.cache_data
def room_color(room):
    return "red" if room % 2 == 0 else "blue"


@st.cache_data
def read_cian_houses_data(path):
    return pd.read_csv(path)


@st.cache_data
def make_cian_houses_map(df_cian):
    return folium.Map(
        location=(
            df_cian["geo_lat"].mean(),
            df_cian["geo_lng"].mean(),
        ),
    )


def make_folium_groups(df_cian, map):

    return {
        i: MarkerCluster(
            name=f"{i}-комнaтные",
            show=(True if i == 1 else False),
        ).add_to(map)
        for i in range(1, df_cian["room_count"].max() + 1)
    }


def fill_folium_groups(df_cian, folium_groups):
    # Fill clustes
    for i in range(1, df_cian["room_count"].max() + 1):
        for _, row in df_cian[df_cian["room_count"] == i].iterrows():
            folium.Marker(
                location=(
                    row["geo_lat"],
                    row["geo_lng"],
                ),
                icon=folium.Icon(
                    color=room_color(i),
                    control=True,
                    # icon="ok-sign",
                ),
            ).add_to(folium_groups[i])

    return folium_groups


def cian_houses_map(
    path: str,
    draw: bool = False,
):

    df_cian = read_cian_houses_data(path)

    map = make_cian_houses_map(df_cian)

    if draw:
        Draw(export=True).add_to(map)

    folium_groups = make_folium_groups(df_cian, map)
    folium_groups = fill_folium_groups(df_cian, folium_groups)

    GroupedLayerControl(
        groups={"Квартиры": list(folium_groups.values())},
        exclusive_groups=False,
        collapsed=False,
    ).add_to(map)

    return map
