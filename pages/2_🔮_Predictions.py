import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="EV Predictions",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stMetric {
        background-color: #0f172a;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and preprocess the EV dataset"""
    try:
        df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Convert Model Year to numeric
        if 'Model Year' in df.columns:
            df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Title and description
st.title("🔮 EV Adoption Predictions & Forecasting")
st.markdown("""
Predict future EV adoption trends using machine learning models. 
Analyze historical data and forecast EV registrations, market share, and growth patterns.
""")

# Load data
df = load_data()

if df is None:
    st.error("Failed to load the dataset.")
    st.stop()

# Sidebar - Prediction Settings
st.sidebar.header("🎛️ Prediction Settings")

prediction_type = st.sidebar.selectbox(
    "Select Prediction Type",
    ["EV Registration Growth", "Market Share by Type", "Geographic Expansion", "Range Evolution"]
)

forecast_years = st.sidebar.slider(
    "Forecast Period (Years)",
    min_value=1,
    max_value=10,
    value=5,
    help="Number of years to forecast into the future"
)

model_type = st.sidebar.selectbox(
    "Prediction Model",
    ["Linear Regression", "Polynomial Regression", "Random Forest"],
    help="Choose the machine learning model for predictions"
)

confidence_interval = st.sidebar.slider(
    "Confidence Interval (%)",
    min_value=80,
    max_value=99,
    value=95,
    help="Confidence level for prediction intervals"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Try different models to compare predictions!")

# Main content
st.markdown("---")

# Prediction Type 1: EV Registration Growth
if prediction_type == "EV Registration Growth":
    st.subheader("📈 EV Registration Growth Forecast")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### 📊 Model Settings")
        include_seasonal = st.checkbox("Include Seasonal Trends", value=True)
        show_confidence = st.checkbox("Show Confidence Intervals", value=True)
    
    with col1:
        # Prepare historical data
        if 'Model Year' in df.columns:
            yearly_counts = df.groupby('Model Year').size().reset_index(name='Count')
            yearly_counts = yearly_counts[yearly_counts['Model Year'] >= 2010]
            yearly_counts = yearly_counts.sort_values('Model Year')
            
            # Train model
            X = yearly_counts['Model Year'].values.reshape(-1, 1)
            y = yearly_counts['Count'].values
            
            if model_type == "Linear Regression":
                model = LinearRegression()
                model.fit(X, y)
            elif model_type == "Polynomial Regression":
                poly = PolynomialFeatures(degree=2)
                X_poly = poly.fit_transform(X)
                model = LinearRegression()
                model.fit(X_poly, y)
            else:  # Random Forest
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X, y)
            
            # Make predictions
            last_year = int(yearly_counts['Model Year'].max())
            future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
            
            if model_type == "Polynomial Regression":
                future_pred = model.predict(poly.transform(future_years))
            else:
                future_pred = model.predict(future_years)
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'Year': future_years.flatten(),
                'Predicted_Count': future_pred
            })
            
            # Calculate confidence intervals (simplified)
            std_error = np.std(y - model.predict(X if model_type != "Polynomial Regression" else X_poly))
            z_score = 1.96 if confidence_interval == 95 else 2.576
            margin = z_score * std_error
            
            forecast_df['Lower_Bound'] = forecast_df['Predicted_Count'] - margin
            forecast_df['Upper_Bound'] = forecast_df['Predicted_Count'] + margin
            
            # Combine historical and forecast
            combined_df = pd.concat([
                yearly_counts.rename(columns={'Model Year': 'Year', 'Count': 'Predicted_Count'}),
                forecast_df
            ])
            
            # Plot
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=yearly_counts['Model Year'],
                y=yearly_counts['Count'],
                mode='lines+markers',
                name='Historical Data',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8)
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['Predicted_Count'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#ff7f0e', width=3, dash='dash'),
                marker=dict(size=8)
            ))
            
            # Confidence interval
            if show_confidence:
                fig.add_trace(go.Scatter(
                    x=forecast_df['Year'].tolist() + forecast_df['Year'].tolist()[::-1],
                    y=forecast_df['Upper_Bound'].tolist() + forecast_df['Lower_Bound'].tolist()[::-1],
                    fill='toself',
                    fillcolor='rgba(255, 127, 14, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name=f'{confidence_interval}% Confidence Interval',
                    showlegend=True
                ))
            
            fig.update_layout(
                title=f"EV Registration Forecast ({model_type})",
                xaxis_title="Year",
                yaxis_title="Number of Registrations",
                height=500,
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    st.markdown("### 📊 Forecast Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_total = len(df)
        st.metric(
            "Current Total EVs",
            f"{current_total:,}",
            delta=None
        )
    
    with col2:
        next_year_pred = int(forecast_df.iloc[0]['Predicted_Count'])
        st.metric(
            f"{int(forecast_df.iloc[0]['Year'])} Forecast",
            f"{next_year_pred:,}",
            delta=f"+{next_year_pred - yearly_counts.iloc[-1]['Count']:,}"
        )
    
    with col3:
        total_forecast = int(forecast_df['Predicted_Count'].sum())
        st.metric(
            f"Total {forecast_years}-Year Forecast",
            f"{total_forecast:,}",
            delta=None
        )
    
    with col4:
        avg_growth = ((forecast_df.iloc[-1]['Predicted_Count'] / yearly_counts.iloc[-1]['Count']) ** (1/forecast_years) - 1) * 100
        st.metric(
            "Avg Annual Growth",
            f"{avg_growth:.1f}%",
            delta=None
        )
    
    # Detailed forecast table
    st.markdown("### 📋 Detailed Forecast Table")
    display_df = forecast_df.copy()
    display_df['Year'] = display_df['Year'].astype(int)
    display_df['Predicted_Count'] = display_df['Predicted_Count'].astype(int)
    display_df['Lower_Bound'] = display_df['Lower_Bound'].astype(int)
    display_df['Upper_Bound'] = display_df['Upper_Bound'].astype(int)
    display_df.columns = ['Year', 'Predicted Registrations', 'Lower Bound', 'Upper Bound']
    st.dataframe(display_df, use_container_width=True)

# Prediction Type 2: Market Share by Type
elif prediction_type == "Market Share by Type":
    st.subheader("🔋 EV Type Market Share Prediction")
    
    if 'Electric Vehicle Type' in df.columns and 'Model Year' in df.columns:
        # Historical market share
        yearly_type = df.groupby(['Model Year', 'Electric Vehicle Type']).size().reset_index(name='Count')
        yearly_type = yearly_type[yearly_type['Model Year'] >= 2015]
        
        # Calculate percentages
        yearly_totals = yearly_type.groupby('Model Year')['Count'].sum().reset_index(name='Total')
        yearly_type = yearly_type.merge(yearly_totals, on='Model Year')
        yearly_type['Percentage'] = (yearly_type['Count'] / yearly_type['Total']) * 100
        
        # Plot historical trends
        fig = px.line(
            yearly_type,
            x='Model Year',
            y='Percentage',
            color='Electric Vehicle Type',
            title='Historical Market Share by EV Type',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Market Share (%)",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Predict future market share
        st.markdown("### 🔮 Future Market Share Prediction")
        
        col1, col2 = st.columns(2)
        
        for ev_type in yearly_type['Electric Vehicle Type'].unique():
            type_data = yearly_type[yearly_type['Electric Vehicle Type'] == ev_type]
            
            X = type_data['Model Year'].values.reshape(-1, 1)
            y = type_data['Percentage'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            last_year = int(type_data['Model Year'].max())
            future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
            future_pred = model.predict(future_years)
            
            # Ensure percentages are between 0 and 100
            future_pred = np.clip(future_pred, 0, 100)
            
            forecast_type_df = pd.DataFrame({
                'Year': future_years.flatten(),
                'Type': ev_type,
                'Predicted_Share': future_pred
            })
            
            with col1 if ev_type == yearly_type['Electric Vehicle Type'].unique()[0] else col2:
                st.markdown(f"#### {ev_type}")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=type_data['Model Year'],
                    y=type_data['Percentage'],
                    mode='lines+markers',
                    name='Historical',
                    line=dict(width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast_type_df['Year'],
                    y=forecast_type_df['Predicted_Share'],
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(width=3, dash='dash')
                ))
                
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Market Share (%)",
                    height=300,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show prediction for next year
                next_year_share = forecast_type_df.iloc[0]['Predicted_Share']
                current_share = type_data.iloc[-1]['Percentage']
                st.metric(
                    f"{int(forecast_type_df.iloc[0]['Year'])} Prediction",
                    f"{next_year_share:.1f}%",
                    delta=f"{next_year_share - current_share:+.1f}%"
                )

# Prediction Type 3: Geographic Expansion
elif prediction_type == "Geographic Expansion":
    st.subheader("🗺️ Geographic Expansion Forecast")
    
    if 'County' in df.columns and 'Model Year' in df.columns:
        # Top counties by current EV count
        top_counties = df['County'].value_counts().head(10).index.tolist()
        
        # Historical growth by county
        county_yearly = df[df['County'].isin(top_counties)].groupby(['Model Year', 'County']).size().reset_index(name='Count')
        county_yearly = county_yearly[county_yearly['Model Year'] >= 2015]
        
        # Plot historical trends
        fig = px.line(
            county_yearly,
            x='Model Year',
            y='Count',
            color='County',
            title='EV Growth by Top 10 Counties',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of EVs",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Predict future growth for selected county
        st.markdown("### 🎯 County-Specific Forecast")
        
        selected_county = st.selectbox("Select County for Detailed Forecast", top_counties)
        
        county_data = county_yearly[county_yearly['County'] == selected_county]
        
        X = county_data['Model Year'].values.reshape(-1, 1)
        y = county_data['Count'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        last_year = int(county_data['Model Year'].max())
        future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
        future_pred = model.predict(future_years)
        
        forecast_county_df = pd.DataFrame({
            'Year': future_years.flatten(),
            'Predicted_Count': future_pred
        })
        
        # Plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=county_data['Model Year'],
            y=county_data['Count'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_county_df['Year'],
            y=forecast_county_df['Predicted_Count'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f"EV Growth Forecast - {selected_county}",
            xaxis_title="Year",
            yaxis_title="Number of EVs",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_count = int(county_data.iloc[-1]['Count'])
            st.metric("Current EVs", f"{current_count:,}")
        
        with col2:
            next_year_pred = int(forecast_county_df.iloc[0]['Predicted_Count'])
            st.metric(
                f"{int(forecast_county_df.iloc[0]['Year'])} Forecast",
                f"{next_year_pred:,}",
                delta=f"+{next_year_pred - current_count:,}"
            )
        
        with col3:
            growth_rate = ((forecast_county_df.iloc[-1]['Predicted_Count'] / current_count) ** (1/forecast_years) - 1) * 100
            st.metric("Avg Annual Growth", f"{growth_rate:.1f}%")

# Prediction Type 4: Range Evolution
elif prediction_type == "Range Evolution":
    st.subheader("🔋 Electric Range Evolution Forecast")
    
    if 'Electric Range' in df.columns and 'Model Year' in df.columns:
        # Historical average range by year
        range_yearly = df[df['Electric Range'] > 0].groupby('Model Year')['Electric Range'].mean().reset_index()
        range_yearly = range_yearly[range_yearly['Model Year'] >= 2012]
        range_yearly.columns = ['Year', 'Avg_Range']
        
        # Train model
        X = range_yearly['Year'].values.reshape(-1, 1)
        y = range_yearly['Avg_Range'].values
        
        if model_type == "Polynomial Regression":
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
        else:
            model = LinearRegression()
            model.fit(X, y)
        
        # Predict future
        last_year = int(range_yearly['Year'].max())
        future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
        
        if model_type == "Polynomial Regression":
            future_pred = model.predict(poly.transform(future_years))
        else:
            future_pred = model.predict(future_years)
        
        forecast_range_df = pd.DataFrame({
            'Year': future_years.flatten(),
            'Predicted_Range': future_pred
        })
        
        # Plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=range_yearly['Year'],
            y=range_yearly['Avg_Range'],
            mode='lines+markers',
            name='Historical Avg Range',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_range_df['Year'],
            y=forecast_range_df['Predicted_Range'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#e74c3c', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Average Electric Range Evolution & Forecast",
            xaxis_title="Year",
            yaxis_title="Average Range (miles)",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_avg = range_yearly.iloc[-1]['Avg_Range']
            st.metric("Current Avg Range", f"{current_avg:.0f} mi")
        
        with col2:
            next_year_pred = forecast_range_df.iloc[0]['Predicted_Range']
            st.metric(
                f"{int(forecast_range_df.iloc[0]['Year'])} Forecast",
                f"{next_year_pred:.0f} mi",
                delta=f"+{next_year_pred - current_avg:.0f} mi"
            )
        
        with col3:
            final_year_pred = forecast_range_df.iloc[-1]['Predicted_Range']
            st.metric(
                f"{int(forecast_range_df.iloc[-1]['Year'])} Forecast",
                f"{final_year_pred:.0f} mi",
                delta=f"+{final_year_pred - current_avg:.0f} mi"
            )
        
        with col4:
            improvement = ((final_year_pred / current_avg - 1) * 100)
            st.metric(
                f"{forecast_years}-Year Improvement",
                f"{improvement:.1f}%"
            )
        
        # Range distribution forecast
        st.markdown("### 📊 Range Distribution Forecast")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Current distribution
            fig = px.histogram(
                df[df['Electric Range'] > 0],
                x='Electric Range',
                nbins=30,
                title='Current Range Distribution'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Predicted distribution (shifted by average improvement)
            shift = next_year_pred - current_avg
            predicted_ranges = df[df['Electric Range'] > 0]['Electric Range'] + shift
            
            fig = px.histogram(
                predicted_ranges,
                nbins=30,
                title=f'Predicted {int(forecast_range_df.iloc[0]["Year"])} Range Distribution'
            )
            fig.update_layout(height=300, xaxis_title="Electric Range (miles)")
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**📝 Note:** These predictions are based on historical trends and machine learning models. 
Actual future values may vary due to technological advances, policy changes, and market dynamics.
""")

st.info("💡 **Tip:** Use different models and compare results to understand prediction uncertainty!")
