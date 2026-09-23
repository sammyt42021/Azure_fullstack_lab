import os

import httpx
import pandas as pd
import streamlit as st

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


@st.cache_data(ttl=300)
def get_eclipses(year_from, year_to, eclipse_type):
    params = {
        "year_from": year_from,
        "year_to": year_to,
    }

    if eclipse_type != "All":
        params["eclipse_type"] = eclipse_type

    response = httpx.get(
        f"{BASE_URL}/eclipses",
        params=params,
        timeout=20,
    )
    response.raise_for_status()

    return response.json()


def main():
    st.set_page_config(
        page_title="eClipseBord",
        page_icon="🌘",
        layout="wide",
    )

    st.title("🌘 eClipseBord")
    st.write("Explore NASA solar eclipse data through FastAPI and Streamlit.")

    st.sidebar.header("Filters")

    year_from, year_to = st.sidebar.slider(
        "Select year range",
        min_value=1900,
        max_value=2100,
        value=(2020, 2030),
    )

    eclipse_type = st.sidebar.selectbox(
        "Select eclipse type",
        ["All", "P", "A", "T", "H"],
        format_func=lambda value: {
            "All": "All eclipse types",
            "P": "Partial",
            "A": "Annular",
            "T": "Total",
            "H": "Hybrid",
        }[value],
    )

    try:
        payload = get_eclipses(year_from, year_to, eclipse_type)
    except httpx.HTTPError as error:
        st.error(f"Could not connect to the backend: {error}")
        st.stop()

    df = pd.DataFrame(payload["items"])

    st.metric("Matching eclipses", payload["total"])

    if df.empty:
        st.info("No eclipses match these filters.")
        return

    st.subheader("Eclipses by type")
    st.bar_chart(df["type"].value_counts())

    st.subheader("Eclipse records")

    display_columns = [
        "Calendar Date",
        "Eclipse Time",
        "type",
        "Eclipse Magnitude",
        "Latitude",
        "Longitude",
        "Path Width (km)",
        "Central Duration",
    ]

    st.dataframe(
    df[display_columns],
    width="stretch",
    hide_index=True,
)


if __name__ == "__main__":
    main()