import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from streamlit.components.v1 import html

from data_utils import get_vehicle_catalog, load_ev_data


# Shared dark theme for the full dashboard surface.
def build_dashboard_theme():
    """Apply custom dark theme styling with improved spacing and readability."""
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-card: #21262d;
    --text-primary: #f0f6fc;
    --text-secondary: #8b949e;
    --accent-blue: #58a6ff;
    --accent-purple: #a371f7;
    --border-subtle: #30363d;
}

.main {
    padding: 1.5rem 2rem 3rem;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-primary) !important;
    line-height: 1.65;
}

[data-testid="stAppViewContainer"] { 
    background-color: #0d1117 !important; 
}

[data-testid="stHeader"], 
[data-testid="stToolbar"] { 
    background-color: #0d1117 !important; 
}

@keyframes fadeInUp {
    from { 
        opacity: 0; 
        transform: translateY(20px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}

@keyframes slideInFromLeft {
    from { 
        opacity: 0; 
        transform: translateX(-30px); 
    }
    to { 
        opacity: 1; 
        transform: translateX(0); 
    }
}

.stMarkdown, 
.stMetric, 
.stDataFrame, 
.stPlotlyChart { 
    animation: fadeInUp 0.6s ease-out forwards; 
}

/* Metric cards with breathing room */
[data-testid="stMetricValue"] { 
    animation: fadeInUp 0.5s ease-out forwards; 
    font-weight: 700 !important; 
    font-size: 1.9rem !important; 
    color: #f0f6fc !important;
    letter-spacing: -0.02em;
}

[data-testid="stMetricLabel"] { 
    font-weight: 500 !important; 
    color: #8b949e !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #21262d 0%, #161b22 100%) !important;
    border-radius: 16px !important;
    padding: 1.5rem 1.25rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    border: 1px solid #30363d !important;
    transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    margin-bottom: 1rem !important;
}

[data-testid="stMetric"]:hover { 
    transform: translateY(-4px) scale(1.02) !important; 
    box-shadow: 0 12px 40px rgba(88,166,255,0.15) !important; 
}

/* Typography with improved hierarchy */
h1 {
    background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    animation: fadeInUp 0.8s ease-out;
    margin-bottom: 1.5rem !important;
    font-size: 2.5rem !important;
}

h2 { 
    color: #f0f6fc !important; 
    font-weight: 600 !important; 
    animation: slideInFromLeft 0.6s ease-out;
    margin-top: 2.5rem !important;
    margin-bottom: 1.25rem !important;
    font-size: 1.75rem !important;
}

h3 { 
    color: #f0f6fc !important; 
    font-weight: 600 !important; 
    animation: slideInFromLeft 0.6s ease-out;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
    font-size: 1.3rem !important;
}

[data-testid="stSidebar"] { 
    background: linear-gradient(180deg, #161b22 0%, #0d1117 100%) !important; 
    border-right: 1px solid #30363d !important;
    padding: 1.5rem 1rem !important;
}

/* Button styles with better interaction feedback */
.stButton > button {
    background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(35,134,54,0.3) !important;
    padding: 0.6rem 1.5rem !important;
}

.stButton > button:hover { 
    transform: translateY(-2px) scale(1.03) !important; 
}

/* Form controls with improved spacing */
[data-testid="stSelectbox"] > div > div { 
    border-radius: 12px !important; 
    border: 2px solid #30363d !important; 
    background: #21262d !important;
    padding: 0.5rem !important;
}

.stAlert { 
    border-radius: 12px !important; 
    border: 1px solid #30363d !important;
    padding: 1rem 1.25rem !important;
    margin: 1rem 0 !important;
}

[data-testid="stDataFrame"] { 
    border-radius: 16px !important; 
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    margin: 1.5rem 0 !important;
}

.js-plotly-plot { 
    border-radius: 16px !important; 
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    margin: 1.5rem 0 !important;
}

[data-testid="stExpander"] { 
    border-radius: 12px !important; 
    border: 1px solid #30363d !important; 
    background: #161b22 !important;
    margin: 1rem 0 !important;
}

[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%) !important;
    border-radius: 12px !important;
    color: white !important;
    padding: 0.6rem 1.5rem !important;
}

hr { 
    background: linear-gradient(90deg, transparent, #30363d, transparent) !important; 
    height: 1px !important; 
    border: none !important;
    margin: 3rem 0 !important;
}

/* Scrollbar styling */
::-webkit-scrollbar { 
    width: 8px; 
    height: 8px; 
}

::-webkit-scrollbar-track { 
    background: #21262d; 
    border-radius: 4px; 
}

::-webkit-scrollbar-thumb { 
    background: linear-gradient(180deg, #58a6ff, #a371f7); 
    border-radius: 4px; 
}

p, span, div { 
    color: #c9d1d9; 
    line-height: 1.65; 
}

/* Add breathing room to charts and sections */
.row-widget.stRadio > div,
.row-widget.stCheckbox > div {
    padding: 0.25rem 0;
}
</style>
"""

st.markdown(build_dashboard_theme(), unsafe_allow_html=True)


def render_location_widget():
    """
    Embed a browser widget that requests GPS access and displays status.
    This allows users to grant location permission if they want location-based features.
    """
    widget_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; 
                padding: 16px; 
                background: transparent;
            }
            
            .location-btn { 
                background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
                color: white; 
                border: none; 
                padding: 14px 28px; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 15px; 
                font-weight: 600;
                width: 100%;
                margin-bottom: 12px;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3);
            }
            
            .location-btn:hover { 
                background: linear-gradient(135deg, #1565C0 0%, #0d47a1 100%);
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
            }
            
            .location-btn:disabled { 
                background: #555; 
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .status-message { 
                padding: 12px 16px; 
                border-radius: 8px; 
                margin: 12px 0; 
                text-align: left;
                font-size: 14px;
                line-height: 1.5;
            }
            
            .status-success { 
                background: #d4edda; 
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .status-error { 
                background: #f8d7da; 
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .status-info { 
                background: #d1ecf1; 
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
        </style>
    </head>
    <body>
        <button id="locationBtn" class="location-btn" onclick="requestLocation()">
            📍 Get My Current Location
        </button>
        <div id="statusDisplay"></div>
        
        <script>
            let currentLocation = null;
            
            function requestLocation() {
                const button = document.getElementById('locationBtn');
                const statusDiv = document.getElementById('statusDisplay');
                
                button.disabled = true;
                button.textContent = '🔄 Requesting location...';
                
                statusDiv.innerHTML = '<div class="status-message status-info">⏳ Waiting for location permission...</div>';
                
                if (!navigator.geolocation) {
                    statusDiv.innerHTML = '<div class="status-message status-error">❌ Your browser doesn\\'t support geolocation.</div>';
                    button.disabled = false;
                    button.textContent = '📍 Get My Current Location';
                    return;
                }
                
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;
                        const accuracy = position.coords.accuracy;
                        
                        currentLocation = {
                            latitude: latitude,
                            longitude: longitude,
                            accuracy: accuracy,
                            timestamp: new Date().toISOString()
                        };
                        
                        // Store for potential Streamlit access
                        try {
                            localStorage.setItem('user_location', JSON.stringify(currentLocation));
                        } catch (e) {
                            console.warn('Could not save to localStorage:', e);
                        }
                        
                        statusDiv.innerHTML = 
                            '<div class="status-message status-success">' +
                            '✅ <strong>Location acquired</strong><br>' +
                            'Latitude: ' + latitude.toFixed(6) + '<br>' +
                            'Longitude: ' + longitude.toFixed(6) + '<br>' +
                            'Accuracy: ±' + accuracy.toFixed(0) + ' meters' +
                            '</div>';
                        
                        button.disabled = false;
                        button.textContent = '✅ Location Saved';
                        
                        setTimeout(() => {
                            button.textContent = '📍 Get My Current Location';
                        }, 3000);
                    },
                    function(error) {
                        let errorMessage = '';
                        
                        switch(error.code) {
                            case error.PERMISSION_DENIED:
                                errorMessage = '❌ Location access was denied. Please allow location in your browser settings.';
                                break;
                            case error.POSITION_UNAVAILABLE:
                                errorMessage = '❌ Location information is unavailable at this time.';
                                break;
                            case error.TIMEOUT:
                                errorMessage = '⏱️ Location request timed out. Please try again.';
                                break;
                            default:
                                errorMessage = '❌ An unknown error occurred while getting your location.';
                        }
                        
                        statusDiv.innerHTML = '<div class="status-message status-error">' + errorMessage + '</div>';
                        button.disabled = false;
                        button.textContent = '📍 Get My Current Location';
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    }
                );
            }
        </script>
    </body>
    </html>
    """
    
    html(widget_html, height=200)


def create_chart_theme():
    """Return consistent Plotly theme settings for all charts."""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(33,38,45,0.3)',
        'font': {'color': '#f0f6fc', 'family': 'Inter, sans-serif'},
        'xaxis': {
            'gridcolor': '#30363d',
            'linecolor': '#30363d'
        },
        'yaxis': {
            'gridcolor': '#30363d',
            'linecolor': '#30363d'
        }
    }


def show_key_metrics(dataframe):
    """Display the main KPI metrics at the top of the dashboard."""
    total_vehicles = len(dataframe)
    
    # Calculate metrics with safe defaults
    avg_range = dataframe[dataframe['Electric Range'] > 0]['Electric Range'].mean() if 'Electric Range' in dataframe.columns else 0
    unique_models = dataframe['Model'].nunique() if 'Model' in dataframe.columns else 0
    unique_makes = dataframe['Make'].nunique() if 'Make' in dataframe.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Vehicles",
            value=f"{total_vehicles:,}"
        )
    
    with col2:
        st.metric(
            label="Average Range",
            value=f"{avg_range:.0f} mi" if avg_range > 0 else "N/A"
        )
    
    with col3:
        st.metric(
            label="Unique Models",
            value=f"{unique_models:,}"
        )
    
    with col4:
        st.metric(
            label="Manufacturers",
            value=f"{unique_makes:,}"
        )


def build_filters(dataframe):
    """
    Build the filter controls and return filtered dataframe.
    Returns the filtered data based on user selections.
    """
    st.sidebar.header("🔍 Filters")
    
    # Model year filter with sensible defaults
    if 'Model Year' in dataframe.columns:
        year_min = int(dataframe['Model Year'].min())
        year_max = int(dataframe['Model Year'].max())
        
        selected_year_range = st.sidebar.slider(
            "Model Year Range",
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
            help="Filter vehicles by their model year"
        )
        
        dataframe = dataframe[
            (dataframe['Model Year'] >= selected_year_range[0]) & 
            (dataframe['Model Year'] <= selected_year_range[1])
        ]
    
    # Make filter with multi-select
    if 'Make' in dataframe.columns:
        available_makes = sorted(dataframe['Make'].dropna().unique())
        
        selected_makes = st.sidebar.multiselect(
            "Vehicle Manufacturers",
            options=available_makes,
            default=[],
            help="Select one or more manufacturers to filter"
        )
        
        if selected_makes:
            dataframe = dataframe[dataframe['Make'].isin(selected_makes)]
    
    # EV type filter
    if 'Electric Vehicle Type' in dataframe.columns:
        ev_types = sorted(dataframe['Electric Vehicle Type'].dropna().unique())
        
        selected_ev_types = st.sidebar.multiselect(
            "Electric Vehicle Type",
            options=ev_types,
            default=[],
            help="Filter by BEV (Battery Electric) or PHEV (Plug-in Hybrid)"
        )
        
        if selected_ev_types:
            dataframe = dataframe[dataframe['Electric Vehicle Type'].isin(selected_ev_types)]
    
    # County filter
    if 'County' in dataframe.columns:
        counties = sorted(dataframe['County'].dropna().unique())
        
        selected_counties = st.sidebar.multiselect(
            "County",
            options=counties,
            default=[],
            help="Filter vehicles by county"
        )
        
        if selected_counties:
            dataframe = dataframe[dataframe['County'].isin(selected_counties)]
    
    # Electric range filter
    if 'Electric Range' in dataframe.columns:
        range_data = dataframe[dataframe['Electric Range'] > 0]['Electric Range']
        
        if len(range_data) > 0:
            range_min = int(range_data.min())
            range_max = int(range_data.max())
            
            selected_range = st.sidebar.slider(
                "Electric Range (miles)",
                min_value=range_min,
                max_value=range_max,
                value=(range_min, range_max),
                help="Filter by electric range capability"
            )
            
            dataframe = dataframe[
                (dataframe['Electric Range'] >= selected_range[0]) & 
                (dataframe['Electric Range'] <= selected_range[1])
            ]
    
    return dataframe


# Main dashboard logic
st.title("⚡ Electric Vehicle Population Dashboard")

st.markdown("""
Explore comprehensive data on electric vehicles registered in Washington State. 
Filter by manufacturer, model year, vehicle type, and location to discover trends and insights.
""")

# Location widget for GPS-based features
with st.expander("📍 Enable Location Features (Optional)", expanded=False):
    st.markdown("""
    Grant location access to see nearby charging stations and local EV statistics.
    Your location data stays in your browser and is never stored on our servers.
    """)
    render_location_widget()

st.markdown("---")

# Load the actual EV dataset
try:
    ev_data = load_ev_data()
    
    if ev_data is None or len(ev_data) == 0:
        st.error("⚠️ Unable to load vehicle data. Please check your data source.")
        st.stop()
    
    # Build filters and get filtered dataset
    filtered_data = build_filters(ev_data)
    
    if len(filtered_data) == 0:
        st.warning("🔍 No vehicles match your current filters. Try adjusting your selections.")
        st.stop()
    
    # Show key metrics
    show_key_metrics(filtered_data)
    
    st.markdown("---")
    
    # Vehicle distribution charts
    st.subheader("📊 Vehicle Distribution")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("##### Distribution by Type")
        
        if 'Electric Vehicle Type' in filtered_data.columns:
            type_counts = filtered_data['Electric Vehicle Type'].value_counts()
            
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.4
            )
            
            theme = create_chart_theme()
            fig.update_layout(
                **theme,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        st.markdown("##### Top 10 Manufacturers")
        
        if 'Make' in filtered_data.columns:
            top_makes = filtered_data['Make'].value_counts().head(10)
            
            fig = px.bar(
                x=top_makes.index,
                y=top_makes.values,
                color=top_makes.values,
                color_continuous_scale='Viridis',
                labels={'x': 'Manufacturer', 'y': 'Number of Vehicles'}
            )
            
            theme = create_chart_theme()
            fig.update_layout(
                **theme,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Temporal and range analysis
    st.subheader("📈 Trends Over Time")
    
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        st.markdown("##### Registrations by Model Year")
        
        if 'Model Year' in filtered_data.columns:
            year_counts = filtered_data['Model Year'].value_counts().sort_index()
            
            fig = px.line(
                x=year_counts.index,
                y=year_counts.values,
                markers=True,
                labels={'x': 'Model Year', 'y': 'Number of Vehicles'}
            )
            
            theme = create_chart_theme()
            fig.update_layout(
                **theme,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            
            fig.update_traces(
                line_color='#58a6ff',
                marker=dict(size=8, color='#a371f7')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with trend_col2:
        st.markdown("##### Electric Range Distribution")
        
        if 'Electric Range' in filtered_data.columns:
            range_data = filtered_data[filtered_data['Electric Range'] > 0]['Electric Range']
            
            fig = px.histogram(
                range_data,
                nbins=30,
                labels={'value': 'Electric Range (miles)', 'count': 'Number of Vehicles'},
                color_discrete_sequence=['#2ea043']
            )
            
            theme = create_chart_theme()
            fig.update_layout(
                **theme,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic distribution
    st.subheader("🌍 Geographic Distribution")
    
    geo_col1, geo_col2 = st.columns(2)
    
    with geo_col1:
        st.markdown("##### Clean Alternative Fuel Vehicle (CAFV) Eligibility")
        
        if 'Clean Alternative Fuel Vehicle (CAFV) Eligibility' in filtered_data.columns:
            cafv_counts = filtered_data['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts()
            
            fig = px.bar(
                x=cafv_counts.index,
                y=cafv_counts.values,
                color=cafv_counts.values,
                color_continuous_scale='Greens',
                labels={'x': 'CAFV Eligibility', 'y': 'Number of Vehicles'}
            )
            
            theme = create_chart_theme()
            fig.update_layout(
                **theme,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with geo_col2:
        st.markdown("##### Top 10 Cities")
        
        if 'City' in filtered_data.columns:
            top_cities = filtered_data['City'].value_counts().head(10)
            
            fig = px.bar(
                x=top_cities.values,
                y=top_cities.index,
                orientation='h',
                color=top_cities.values,
                color_continuous_scale='Oranges',
                labels={'x': 'Number of Vehicles', 'y': 'City'}
            )
            
            theme = create_chart_theme()
            fig.update_layout(
                **theme,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # GPS Location Map
    st.subheader("🗺️ Vehicle Location Map")
    
    if 'Latitude' in filtered_data.columns and 'Longitude' in filtered_data.columns:
        map_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])
        
        if len(map_data) > 0:
            map_col1, map_col2, map_col3 = st.columns([2, 2, 1])
            
            with map_col1:
                max_sample = min(10000, len(map_data))
                min_sample = min(100, len(map_data))
                
                if max_sample > min_sample:
                    sample_size = st.slider(
                        "Number of vehicles to display",
                        min_value=min_sample,
                        max_value=max_sample,
                        value=min(1000, len(map_data)),
                        step=min(100, max(1, (max_sample - min_sample) // 10)),
                        help="Showing fewer vehicles improves map performance"
                    )
                else:
                    sample_size = len(map_data)
                    st.info(f"📊 Displaying all {len(map_data):,} vehicles")
            
            with map_col2:
                color_option = st.selectbox(
                    "Color markers by",
                    options=['Electric Vehicle Type', 'Make', 'County'],
                    help="Choose how to categorize map markers"
                )
            
            with map_col3:
                display_map = st.checkbox(
                    "📍 Show Map", 
                    value=False, 
                    help="Load interactive map"
                )
            
            if display_map:
                sampled_map_data = map_data.sample(
                    n=min(sample_size, len(map_data)), 
                    random_state=42
                ).copy()
                
                # Build hover text for each point
                sampled_map_data['hover_text'] = (
                    sampled_map_data['Make'].astype(str) + ' ' + 
                    sampled_map_data['Model'].astype(str) + '<br>' +
                    'Year: ' + sampled_map_data['Model Year'].astype(str) + '<br>' +
                    'Range: ' + sampled_map_data['Electric Range'].astype(str) + ' mi<br>' +
                    'City: ' + sampled_map_data['City'].astype(str) + ', ' + 
                    sampled_map_data['County'].astype(str)
                )
                
                fig = px.scatter_mapbox(
                    sampled_map_data,
                    lat='Latitude',
                    lon='Longitude',
                    color=color_option,
                    hover_name='hover_text',
                    zoom=7,
                    height=600,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_layout(
                    mapbox_style="open-street-map",
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01,
                        bgcolor="rgba(255, 255, 255, 0.85)"
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Map statistics
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.metric("📍 Displayed", f"{len(sampled_map_data):,}")
                
                with stat_col2:
                    st.metric("🌍 Total with GPS", f"{len(map_data):,}")
                
                with stat_col3:
                    gps_coverage = (len(map_data) / len(filtered_data)) * 100
                    st.metric("📊 GPS Coverage", f"{gps_coverage:.1f}%")
                
                with stat_col4:
                    st.metric("⚡ Map Status", "✅ Active")
        else:
            st.info("ℹ️ No GPS location data available for current filters.")
    else:
        st.warning("⚠️ GPS location data not found in dataset.")
    
    st.markdown("---")
    
    # Detailed data table
    st.subheader("📋 Detailed Vehicle Data")
    
    default_columns = ['Make', 'Model', 'Model Year', 'Electric Vehicle Type', 
                       'Electric Range', 'County', 'City']
    
    # Only show columns that exist
    available_defaults = [col for col in default_columns if col in filtered_data.columns]
    
    selected_columns = st.multiselect(
        "Select columns to display",
        options=filtered_data.columns.tolist(),
        default=available_defaults,
        help="Choose which data fields to show in the table"
    )
    
    if selected_columns:
        st.dataframe(
            filtered_data[selected_columns].head(100),
            use_container_width=True,
            height=400
        )
        
        # Export option
        csv_export = filtered_data[selected_columns].to_csv(index=False)
        
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_export,
            file_name=f"ev_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("👆 Select at least one column to display the data table.")
    
    st.markdown("---")
    
    # Statistical summary
    st.subheader("📊 Statistical Summary")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.markdown("**Electric Range Statistics**")
        
        if 'Electric Range' in filtered_data.columns:
            range_stats = filtered_data[filtered_data['Electric Range'] > 0]['Electric Range']
            
            if len(range_stats) > 0:
                st.write(f"• Mean: {range_stats.mean():.1f} miles")
                st.write(f"• Median: {range_stats.median():.1f} miles")
                st.write(f"• Maximum: {range_stats.max():.0f} miles")
                st.write(f"• Minimum: {range_stats.min():.0f} miles")
            else:
                st.write("No range data available")
    
    with stats_col2:
        st.markdown("**Model Year Statistics**")
        
        if 'Model Year' in filtered_data.columns:
            st.write(f"• Newest: {int(filtered_data['Model Year'].max())}")
            st.write(f"• Oldest: {int(filtered_data['Model Year'].min())}")
            
            mode_year = filtered_data['Model Year'].mode()
            if len(mode_year) > 0:
                st.write(f"• Most Common: {int(mode_year[0])}")
    
    with stats_col3:
        st.markdown("**Dataset Statistics**")
        st.write(f"• Total Records: {len(filtered_data):,}")
        
        if 'Make' in filtered_data.columns:
            st.write(f"• Unique Makes: {filtered_data['Make'].nunique():,}")
        
        if 'Model' in filtered_data.columns:
            st.write(f"• Unique Models: {filtered_data['Model'].nunique():,}")
        
        if 'County' in filtered_data.columns:
            st.write(f"• Unique Counties: {filtered_data['County'].nunique():,}")

except Exception as e:
    st.error(f"⚠️ An error occurred while loading the dashboard: {str(e)}")
    st.stop()


# Footer
st.markdown("---")

st.markdown("""
<div style='
    text-align: center; 
    padding: 2.5rem 1.5rem;
    margin-top: 3rem;
    background: linear-gradient(135deg, rgba(88, 166, 255, 0.05) 0%, rgba(163, 113, 247, 0.05) 100%);
    border-radius: 16px;
    border: 1px solid rgba(88, 166, 255, 0.1);
'>
    <div style='margin-bottom: 1rem;'>
        <span style='font-size: 1.5rem;'>⚡</span>
        <span style='
            font-size: 1.15rem;
            font-weight: 600;
            background: linear-gradient(135deg, #58a6ff, #a371f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-left: 0.5rem;
        '>Electric Vehicle Population Dashboard</span>
    </div>
    
    <p style='
        color: #8b949e; 
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.6;
    '>
        Built with Streamlit & Plotly • Data provided by Washington State Department of Licensing
    </p>
</div>
""", unsafe_allow_html=True)
