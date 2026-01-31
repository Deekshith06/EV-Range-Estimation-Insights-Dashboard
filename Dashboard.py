import streamlit as st
import pandas as pd
import plotly.express as px
from data_utils import load_ev_data
from improved_ev_advisor import create_improved_ev_advisor


# Configure page settings
st.set_page_config(
    page_title="EV Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Maintain dark theme preference
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True


def apply_landing_styles():
    """Apply styling for the landing page with improved spacing and readability."""
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

[data-testid="stAppViewContainer"] { 
    background-color: #0d1117 !important; 
    padding-top: 2rem !important; 
}

[data-testid="stHeader"] { 
    background-color: #0d1117 !important; 
}

[data-testid="stSidebar"] { 
    background: linear-gradient(180deg, #161b22 0%, #0d1117 100%) !important; 
    border-right: 1px solid #30363d !important;
    padding: 1.5rem 1rem !important;
}

.main { 
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
    line-height: 1.65;
    padding: 1.5rem 2rem 3rem;
}

h1 { 
    background: linear-gradient(135deg, #58a6ff, #a371f7); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; 
    margin-bottom: 1rem !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

h2 { 
    color: #f0f6fc !important;
    font-weight: 600 !important;
    margin-top: 2.5rem !important;
    margin-bottom: 1.25rem !important;
    font-size: 1.75rem !important;
}

h3 { 
    color: #f0f6fc !important;
    font-weight: 600 !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
    font-size: 1.3rem !important;
}

p, span, label { 
    color: #c9d1d9 !important;
    line-height: 1.65;
}

[data-testid="stMetric"] { 
    background: linear-gradient(135deg, #21262d 0%, #161b22 100%) !important; 
    border: 1px solid #30363d !important; 
    border-radius: 16px !important; 
    padding: 1.5rem 1.25rem !important; 
    margin-bottom: 1rem !important;
    min-height: 120px !important;
}

[data-testid="stMetricValue"] { 
    color: #f0f6fc !important; 
    font-weight: 700 !important;
    font-size: 1.9rem !important;
    letter-spacing: -0.02em;
}

[data-testid="stMetricLabel"] { 
    color: #8b949e !important; 
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

.stButton > button { 
    background: linear-gradient(135deg, #238636, #2ea043) !important; 
    color: white !important; 
    border-radius: 12px !important; 
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.03) !important;
}

[data-testid="stSelectbox"] > div > div { 
    border-radius: 12px !important; 
    border: 2px solid #30363d !important; 
    background: #21262d !important;
    padding: 0.5rem !important;
}

.js-plotly-plot { 
    border-radius: 16px !important; 
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    margin: 1.5rem 0 !important;
}

hr { 
    background: linear-gradient(90deg, transparent, #30363d, transparent) !important; 
    height: 1px !important; 
    border: none !important;
    margin: 3rem 0 !important;
}

::-webkit-scrollbar { 
    width: 8px; 
}

::-webkit-scrollbar-track { 
    background: #21262d; 
}

::-webkit-scrollbar-thumb { 
    background: linear-gradient(180deg, #58a6ff, #a371f7); 
    border-radius: 4px; 
}
</style>
"""

st.markdown(apply_landing_styles(), unsafe_allow_html=True)


st.sidebar.markdown("---")


# Load the dataset
try:
    ev_data = load_ev_data()
except FileNotFoundError as error:
    st.error(str(error))
    ev_data = None

if ev_data is not None:
    # Page header
    st.title("📊 EV Population Dashboard")
    st.markdown("### Washington State Electric Vehicle Registration Analysis")
    
    st.markdown("""
    Welcome to the EV Population Dashboard. This overview provides a high-level snapshot 
    of the electric vehicle landscape in Washington State.
    
    **👈 Navigate using the sidebar:**
    - **🏠 Home** — Interactive data exploration with mapping and advanced filters
    - **🔮 Predictions** — Machine learning forecasts for adoption trends and market evolution
    
    ---
    
    ### ⚡ Quick Overview
    
    The metrics and visualizations below update dynamically based on your filter selections.
    """)
    
    # Sidebar filter controls
    st.sidebar.header("🔍 Filter Options")
    
    # Manufacturer filter
    all_makes = ['All'] + sorted(ev_data['Make'].dropna().unique().tolist())
    selected_manufacturer = st.sidebar.selectbox("Manufacturer", all_makes)
    
    filtered_data = ev_data.copy()
    
    if selected_manufacturer != 'All':
        filtered_data = filtered_data[filtered_data['Make'] == selected_manufacturer]
    
    # Model year range filter
    if 'Model Year' in ev_data.columns:
        earliest_year = int(ev_data['Model Year'].min())
        latest_year = int(ev_data['Model Year'].max())
        
        if earliest_year == latest_year:
            st.sidebar.info(f"📅 All vehicles are from {earliest_year}.")
        else:
            year_selection = st.sidebar.slider(
                "Model Year Range",
                min_value=earliest_year,
                max_value=latest_year,
                value=(earliest_year, latest_year)
            )
            
            filtered_data = filtered_data[
                (filtered_data['Model Year'] >= year_selection[0]) &
                (filtered_data['Model Year'] <= year_selection[1])
            ]
    
    # Key performance metrics
    st.markdown("---")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            "🚗 Total Vehicles",
            f"{len(filtered_data):,}"
        )
    
    with metric_col2:
        unique_manufacturers = filtered_data['Make'].nunique()
        st.metric(
            "🏭 Manufacturers",
            f"{unique_manufacturers:,}"
        )
    
    with metric_col3:
        if 'Electric Range' in filtered_data.columns:
            average_range = filtered_data['Electric Range'].mean()
            st.metric(
                "⚡ Average Range",
                f"{average_range:.0f} mi"
            )
        else:
            st.metric("⚡ Average Range", "N/A")
    
    with metric_col4:
        unique_counties = filtered_data['County'].nunique()
        st.metric(
            "📍 Counties",
            f"{unique_counties:,}"
        )
    
    # EV Recommendation System
    create_improved_ev_advisor(filtered_data)
    
    # Data visualizations
    st.markdown("---")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("🔋 Vehicle Type Distribution")
        
        if 'Electric Vehicle Type' in filtered_data.columns:
            type_distribution = filtered_data['Electric Vehicle Type'].value_counts()
            
            type_chart = px.pie(
                values=type_distribution.values,
                names=type_distribution.index,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            type_chart.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f0f6fc', family='Inter, sans-serif')
            )
            
            st.plotly_chart(type_chart, use_container_width=True)
    
    with chart_col2:
        st.subheader("🏭 Top 10 Manufacturers")
        
        if 'Make' in filtered_data.columns:
            top_manufacturers = filtered_data['Make'].value_counts().head(10)
            
            manufacturer_chart = px.bar(
                x=top_manufacturers.values,
                y=top_manufacturers.index,
                orientation='h',
                color=top_manufacturers.values,
                color_continuous_scale='Blues',
                labels={'x': 'Number of Vehicles', 'y': 'Manufacturer'}
            )
            
            manufacturer_chart.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                yaxis={'categoryorder': 'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f0f6fc', family='Inter, sans-serif'),
                xaxis=dict(gridcolor='#30363d'),
                showlegend=False
            )
            
            st.plotly_chart(manufacturer_chart, use_container_width=True)
    
    # Temporal trend analysis
    st.markdown("---")
    st.subheader("📈 Registration Trends by Model Year")
    
    if 'Model Year' in filtered_data.columns:
        yearly_registrations = filtered_data['Model Year'].value_counts().sort_index()
        
        trend_chart = px.line(
            x=yearly_registrations.index,
            y=yearly_registrations.values,
            markers=True,
            labels={'x': 'Model Year', 'y': 'Number of Vehicles'}
        )
        
        trend_chart.update_layout(
            xaxis_title="Model Year",
            yaxis_title="Number of Vehicles",
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f0f6fc', family='Inter, sans-serif'),
            xaxis=dict(gridcolor='#30363d', linecolor='#30363d'),
            yaxis=dict(gridcolor='#30363d', linecolor='#30363d')
        )
        
        trend_chart.update_traces(
            line_color='#58a6ff',
            marker=dict(size=8, color='#a371f7')
        )
        
        st.plotly_chart(trend_chart, use_container_width=True)
    
    # Footer
    st.markdown("---")
    
    st.markdown("""
    <div style='
        text-align: center; 
        padding: 2.5rem 1.5rem;
        background: linear-gradient(135deg, rgba(88, 166, 255, 0.05) 0%, rgba(163, 113, 247, 0.05) 100%);
        border-radius: 16px;
        border: 1px solid rgba(88, 166, 255, 0.1);
    '>
        <div style='margin-bottom: 1rem;'>
            <span style='font-size: 1.5rem;'>📊</span>
            <span style='
                font-size: 1.15rem;
                font-weight: 600;
                background: linear-gradient(135deg, #58a6ff, #a371f7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-left: 0.5rem;
            '>EV Population Dashboard</span>
        </div>
        
        <p style='
            color: #8b949e; 
            font-size: 0.9rem;
            margin: 0.75rem 0 0 0;
            line-height: 1.6;
        '>
            Built with Streamlit & Plotly • Data: Washington State Department of Licensing
        </p>
        
        <p style='
            color: #8b949e; 
            font-size: 0.85rem;
            margin: 0.75rem 0 0 0;
        '>
            Navigate to <strong style='color: #58a6ff;'>🏠 Home</strong> for complete features 
            or <strong style='color: #a371f7;'>🔮 Predictions</strong> for ML forecasting
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("⚠️ Unable to load EV dataset. Please verify that the data source exists and is accessible.")
    
    st.info("""
    **Troubleshooting:**
    - Ensure the CSV file is in the correct location
    - Check file permissions
    - Verify data format compatibility
    """)