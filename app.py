import streamlit as st
from dashboards.routing_dashboard import show_routing_dashboard

st.set_page_config(
    page_title="YottaFlex Support AI",
    page_icon="🎧",
    layout="wide"
)

show_routing_dashboard()