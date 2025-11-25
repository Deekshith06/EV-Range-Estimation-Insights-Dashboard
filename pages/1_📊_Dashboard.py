import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from streamlit.components.v1 import html

# Page config
st.set_page_config(
    page_title="EV Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 EV Population Dashboard")
st.info("👈 Use the sidebar to navigate between pages")

# Redirect message
st.markdown("""
This page has been moved to the main dashboard.
Please go back to the **Home** page to access the full dashboard.
""")

st.markdown("---")
st.markdown("**Navigation:**")
st.markdown("- 🏠 **Home** - Main EV Dashboard with all visualizations")
st.markdown("- 🔮 **Predictions** - EV adoption forecasting and predictions")
