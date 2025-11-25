# 🔋 EV Range Estimation & Insights Dashboard

A Streamlit-powered experience focused on estimating the real-world driving range of electric vehicles (EVs) using Washington State registration data.

## 📋 About

This project centers on understanding and forecasting how far EVs can travel under different conditions. It combines the state EV registry with custom analytics to estimate range performance, simulate live driving, and surface actionable insights.

## 🎯 Purpose

Accurate EV range estimates are essential for drivers, planners, and policymakers. This dashboard helps users:

- **Range Forecasting**: Estimate usable range for popular EV makes/models
- **Condition Sensitivity**: See how speed, climate, and terrain impact range
- **Live Range Simulation**: Track battery drain and range in real time
- **Geographic Context**: Understand where range-limited vehicles are concentrated
- **EV Adoption Trends**: Monitor how range improvements influence adoption

## 🚀 Features

### 🏠 Main Dashboard

- **Interactive Filtering**: Real-time data filtering by:
  - Model Year Range
  - Electric Vehicle Type (BEV/PHEV)
  - Manufacturer
  - County
  - Minimum Electric Range
- **GPS Location Features**:
  - 🌐 **Live GPS Location** - Request real-time location from your device
  - 🔐 **Permission-based Access** - Browser prompts for location permission
  - 📍 **High Accuracy Mode** - Uses device GPS for precise positioning
  - 🗺️ Interactive map with vehicle locations
  - 📍 Multiple location modes: Live GPS, Manual Input, or Default
  - 🎯 Nearest EV finder (shows 5 closest vehicles)
  - 🌍 Color-coded markers by type, make, or county
  - 📊 GPS coverage and accuracy statistics
  - 🔍 Adjustable map sample size for performance
  - 🚗 Nearby EVs counter (within 10 miles)
- **Live Range Tracking**:
  - 📡 Real-time battery and range simulation
  - 🚗 Select from top 20 popular EV models
  - ⚡ Adjustable driving parameters (speed, style)
  - 📈 Live charts for battery and range over time
  - 🔄 Configurable refresh rate (1-10 seconds)
  - 📍 GPS-based location tracking
- **Range Prediction Calculator (Sidebar)**:
  - 🔮 **Real-time range prediction** - Calculate remaining range based on conditions
  - 🚗 **Vehicle selection** - Choose from popular EVs or enter custom range
  - 🔋 **Battery level** - Adjust current charge percentage
  - ⚡ **Driving conditions** - Speed, temperature, terrain
  - 🌡️ **Temperature impact** - Cold/hot weather effects on range
  - ⛰️ **Terrain factors** - Flat, rolling, hilly, or mountain
  - ❄️ **Climate control** - AC/heating impact calculation
  - 🛣️ **Highway vs City** - Driving mode efficiency
  - 📊 **Efficiency breakdown** - See impact of each factor
  - ⚠️ **Range alerts** - Low/moderate/good range warnings
- **Live Speed Tracking (GPS-Based)**:
  - 🌐 **Real GPS tracking** - Speed calculated from actual location changes
  - 🛑 **Stationary detection** - Speed = 0 mph when not moving
  - 📏 **Haversine distance** - Accurate distance calculation between GPS points
  - ⚡ **Acceleration tracking** - Green zones show speed increases
  - 🐌 **Deceleration tracking** - Red zones show speed decreases
  - 📊 **Speed statistics** - Avg speed, max speed, variance
  - 🎯 **Smoothness score** - Driving efficiency rating
  - ➡️ **Live speed delta** - Shows acceleration/deceleration in real-time
  - 📈 **Interactive speed chart** - Visual representation of speed changes
  - 🏁 **Performance metrics** - Count of accelerations and decelerations
  - 🛣️ **Actual distance** - Total distance traveled based on GPS coordinates
- **Comprehensive Visualizations**:
  - EV Type Distribution (Pie Chart)
  - Top Manufacturers (Bar Chart)
  - Registration Trends by Year (Line Chart)
  - Electric Range Distribution (Histogram)
  - Geographic Distribution by County
  - Most Popular Models
  - CAFV Eligibility Status
  - Top Cities for EV Adoption
- **Data Export**: Download filtered data as CSV
- **Statistical Summary**: Key metrics and statistics
- **Responsive Design**: Modern, mobile-friendly interface

### 🔮 Predictions Page

- **Machine Learning Models**:
  - 📈 Linear Regression
  - 📊 Polynomial Regression
  - 🌲 Random Forest
- **Prediction Types**:
  - **EV Registration Growth** - Forecast future EV registrations
  - **Market Share by Type** - Predict BEV vs PHEV market share
  - **Geographic Expansion** - County-level growth predictions
  - **Range Evolution** - Electric range improvement forecasts
- **Advanced Features**:
  - 📅 Configurable forecast period (1-10 years)
  - 📊 Confidence intervals (80-99%)
  - 📈 Interactive visualizations
  - 📋 Detailed forecast tables
  - 🎯 Model comparison capabilities
  - 📉 Historical trend analysis

## 📦 Installation & Setup

Run the following commands in your terminal:

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-folder>
```
```bash
# 2. (Optional but recommended) Create a virtual environment
python -m venv .venv
```
```bash
# 3. Activate the virtual environment
# macOS / Linux
source .venv/bin/activate
```
```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate
```
```bash
# 4. Install dependencies
pip install -r requirements.txt
```
```bash
# 5. Ensure the EV dataset is available
ls Electric_Vehicle_Population_Data.csv
```

> **Note:** If the dataset file is stored elsewhere, move or link it into the project root so the app can load it.

## 🏃 Running the Application

With the virtual environment activated, start Streamlit using the commands for your OS:

**macOS / Linux**
```bash
source .venv/bin/activate
streamlit run app.py
```

**Windows (PowerShell)**
```powershell
.\.venv\Scripts\Activate
streamlit run app.py
```

Then open `http://localhost:8501` in your browser (Streamlit also auto-opens a tab by default).

## 🧭 Navigation

The dashboard now features **multiple pages** accessible from the sidebar:

### 🏠 Home (Main Dashboard)
- Complete EV population analysis
- Interactive filtering and visualizations
- Live GPS tracking and range simulation
- Geographic distribution maps
- Statistical summaries

### 🔮 Predictions
- Machine learning-based forecasting
- Multiple prediction models
- Configurable forecast periods
- Confidence intervals
- Detailed forecast tables

**To navigate:** Click on the page names in the sidebar (left side of the screen)

## 🌐 Using Live GPS Location

### How to Enable Live GPS:

1. **Enable Live Tracking** in the sidebar
2. Select **"Use Live GPS"** from Location Source options
3. Click the **"🌐 Enable Live GPS"** button
4. **Allow location access** when your browser prompts you
5. Your live coordinates will be displayed automatically

### Browser Permissions:
- The app requests location permission through your browser
- You can allow or deny the request
- Location data is only used within the app session
- No location data is stored or transmitted externally

### Fallback Options:
- If GPS fails, manually enter coordinates
- Use default Seattle location
- Switch between modes anytime

### What You Get:
- ✅ Real-time latitude/longitude display
- 🎯 GPS accuracy in meters
- 🚗 Count of nearby EVs (within 10 miles)
- 📍 Your location shown on interactive map
- 🗺️ Distance calculations to all EVs in dataset

## 📊 Dashboard Sections

### Key Metrics
- **Total EVs**: Number of vehicles in filtered dataset
- **Manufacturers**: Count of unique EV manufacturers
- **Average Range**: Mean electric range across all vehicles
- **Counties**: Number of counties with EV registrations

### Visualizations
1. **EV Type Distribution**: Breakdown of Battery Electric Vehicles (BEV) vs Plug-in Hybrid Electric Vehicles (PHEV)
2. **Top Manufacturers**: Leading EV manufacturers by registration count
3. **Registration Trends**: Year-over-year EV adoption patterns
4. **Range Distribution**: Electric range capabilities histogram
5. **Geographic Analysis**: County and city-level distribution
6. **Popular Models**: Most registered EV models
7. **CAFV Eligibility**: Clean Alternative Fuel Vehicle eligibility status

### Data Table
- Customizable column selection
- View up to 100 records
- Export filtered data to CSV

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly Express & Plotly Graph Objects
- **Styling**: Custom CSS

## 📈 Dataset Details

- **Source**: Washington State Electric Vehicle Population Data
- **Columns Include**:
  - VIN (1-10)
  - County, City, State, Postal Code
  - Model Year, Make, Model
  - Electric Vehicle Type
  - Clean Alternative Fuel Vehicle (CAFV) Eligibility
  - Electric Range
  - Base MSRP
  - Legislative District
  - Vehicle Location
  - Electric Utility
  - 2020 Census Tract

## 🎨 UI Highlights

- Modern, clean design with custom color schemes
- Interactive filters in sidebar
- Real-time data updates
- Responsive charts and visualizations
- Mobile-friendly layout
- Intuitive navigation

## 🔮 Future Enhancements

- Geographic map visualization with coordinates
- Time-series forecasting for EV adoption
- Utility company analysis
- Legislative district insights
- Price analysis (MSRP trends)
- Comparison tools between manufacturers
- Advanced filtering options

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Built with ❤️ using Streamlit, Pandas, and Plotly**
