# 🔋 EV Range Estimation & Insights Dashboard

A Streamlit dashboard for analyzing Washington State EV data and estimating real-world electric vehicle range.

## 📋 What It Does

Understand how far EVs can actually go under different conditions. Combines official registration data with interactive analytics and forecasting.

## 🎯 Features

* Estimate real-world range for popular EV models
* See how speed, temperature, terrain affect range
* Live GPS tracking with battery simulation
* Explore EV adoption by county and city
* Visual breakdowns of types, makes, and trends
* Forecast future EV adoption with ML models

## 📦 Installation & Setup

Run the following commands in your terminal:

**1. Clone the repository**

```bash
git clone https://github.com/Deekshith06/EV-Range-Estimation-Insights-Dashboard.git
cd EV-Range-Estimation-Insights-Dashboard
```

**2. (Optional but recommended) Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the virtual environment**

macOS / Linux
```bash
source .venv/bin/activate
```

Windows (PowerShell)
```bash
.\.venv\Scripts\Activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Ensure the EV dataset is available**

```bash
ls Electric_Vehicle_Population_Data.csv
```

Note: If the dataset file is stored elsewhere, move or link it into the project root so the app can load it.

## 🏃 Running the Application

macOS / Linux
```bash
source .venv/bin/activate
streamlit run app.py
```

Windows (PowerShell)
```powershell
.\.venv\Scripts\Activate
streamlit run app.py
```

## 🛠️ Built With

Streamlit • Pandas • NumPy • Plotly

## 📊 Dataset

Washington State EV Population data with model, make, type, county, year, range, and eligibility info.

## 🤝 Contributing

Issues and pull requests welcome.

## 📫 Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deekshith030206)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Deekshith06)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:seelaboyinadeekshith@gmail.com)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/deekshith06)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/deekshith06)

---

⭐ From [Deekshith06](https://github.com/Deekshith06) | Building the future with AI 🚀
