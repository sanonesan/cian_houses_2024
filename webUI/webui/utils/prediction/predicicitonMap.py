import streamlit as st
import pandas as pd

import folium
from folium.plugins import Draw, MarkerCluster, GroupedLayerControl

__all__ = ["make_moscow_map"]


def make_moscow_map(copy_to_clipboard: bool = False):
    map = folium.Map()
    map = folium.Map(location=(55.751244, 37.618423))
    map.add_child(folium.LatLngPopup())
    if copy_to_clipboard:
        map.add_child(
            folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
        )
    return map
