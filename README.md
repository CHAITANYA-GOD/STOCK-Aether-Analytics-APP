<!-- PROJECT LOGO -->
<p align="center">
  <img src="assets/logo.png" alt="Aether Analytics Logo" width="200">
</p>

<h1 align="center">⚡ Aether Analytics</h1>
<p align="center">
  <b>An AI-Powered Stock Market Analysis & Prediction Platform with a Cyberpunk UI</b>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.8%2B-green.svg" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/github/stars/yourusername/aether-analytics?style=social" alt="GitHub stars"></a>
</p>

---

> **Aether Analytics** is an interactive web app built with **Streamlit** for stock market enthusiasts, researchers, and data scientists. It features a **cyberpunk-themed UI** for analyzing historical stock data, performing technical analysis, and generating **AI-driven predictions**.

---

## 📖 Table of Contents
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Disclaimer](#-disclaimer)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Key Features

- **Multi-Source Data Fetching:** Fetch from **yfinance**, **Alpha Vantage**, or fallback sample data.
- **AI-Powered Forecasting:** Uses **Random Forest Regressor** to predict future prices.
- **Comprehensive Technical Indicators:** Includes **MA** and **RSI**.
- **Interactive Visuals:** Beautiful **Plotly** charts for price, volume, and RSI.
- **Cyberpunk UI:** Neon futuristic interface.
- **Model Metrics:** Displays **R², RMSE, MAE**, and feature importance.

---

## 📸 Screenshots

<p align="center">
  <img src="assets/screenshot1.png" alt="Dashboard Screenshot" width="600">
</p>

<p align="center">
  <img src="assets/screenshot2.png" alt="Prediction Example" width="600">
</p>

> Replace the images in the `assets/` folder with your actual screenshots.

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the Repository
```bash
git clone <[https://github.com/CHAITANYA-GOD/STOCK-Aether-Analytics-APP]>
cd <STOCK-Aether-Analytics-APP>
```

### 2. Create and Activate Virtual Environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt**
```
streamlit
pandas
yfinance
plotly
scikit-learn
numpy
alpha_vantage
```

### 4. (Optional) Set Up Alpha Vantage API Key
```bash
# macOS / Linux
export ALPHA_VANTAGE_API_KEY="YOUR_API_KEY"

# Windows
set ALPHA_VANTAGE_API_KEY="YOUR_API_KEY"
```

---

## ▶ Usage
Run the app:
```bash
streamlit run main_app.py
```
It will open in your default browser.

---

## 📂 Project Structure
```plaintext
.
├── main_app.py
├── modules/
│   ├── __init__.py
│   ├── processing.py
│   └── ui.py
├── data/
│   └── sample_data.csv
└── requirements.txt
```

---

## ⚠ Disclaimer
- For **educational & research use only**.
- Predictions are **not financial advice**.
- Market conditions change unpredictably.
- Always consult a **licensed financial advisor**.

---

## 🤝 Contributing
Contributions are welcome!  
1. Fork the repo  
2. Create a feature branch: `git checkout -b feature-name`  
3. Commit changes: `git commit -m 'Added new feature'`  
4. Push to branch: `git push origin feature-name`  
5. Open a Pull Request  

---

## 📄 License
Licensed under the **MIT License**.
