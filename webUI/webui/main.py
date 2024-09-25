import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

PATH_HOUSES = "./data/cian_houses_dataset.csv"


# m1 = folium.Map()
# m1 = folium.Map(location=(55.751244, 37.618423))
# m1.add_child(folium.LatLngPopup())
# m1.add_child(
#     folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
# )

# out = st_folium(m)
# out = st_folium(m1)
#
#
# st.text(out)
# print(out)


if __name__ == "__main__":

    # st.title("Предсказание цены на квартиру в Москве")

    st.set_page_config(layout="wide")

    # sections = st.sidebar.toggle("Sections", value=True, key="use_sections")

    nav = get_nav_from_toml("./streamlit_pages/pages_selections.toml")

    pg = st.navigation(nav)

    add_page_title(pg)

    pg.run()

    # df_cian = pd.read_csv(PATH_HOUSES)

    # tab_analysis, tab_prediction = st.tabs(("Аналитика", "Прогноз"))
    #
    # with tab_analysis:
    #     st.header("Аналитика")
    #
    #     st.subheader("Карта квартир")
    #     m = cian_houses_map(PATH_HOUSES)
    #     st_folium(m)
    #
    # with tab_prediction:
    #     st.header("Прогноз цены")
    #     st.subheader("Карта")

    pass
