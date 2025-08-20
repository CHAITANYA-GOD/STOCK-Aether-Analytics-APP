⚡ Aether AnalyticsAn AI-Powered Stock Market Analysis & Prediction Platform with a Cyberpunk UIAether Analytics is an interactive web application built with Streamlit designed for stock market enthusiasts, researchers, and data scientists. It provides a sleek, cyberpunk-themed interface for analyzing historical stock data, performing technical analysis, and generating price predictions using a machine learning model.🚀 Key FeaturesMulti-Source Data Fetching: Seamlessly fetches data from popular financial APIs, including yfinance and Alpha Vantage, with an automatic fallback to sample data if APIs are unavailable.AI-Powered Price Forecasting: Utilizes a Random Forest Regressor model to forecast future stock prices based on historical trends and technical indicators.Comprehensive Technical Analysis: Automatically calculates and visualizes key technical indicators, including Moving Averages (MA) and the Relative Strength Index (RSI).Interactive Visualizations: Displays beautiful and customizable charts for price, volume, and RSI using Plotly, allowing for an in-depth view of market movements.Unique Thematic UI: Features a custom cyberpunk user interface with dynamic elements, neon colors, and a futuristic "terminal" output for displaying AI predictions.Detailed Model Performance: Provides key metrics such as R², RMSE, and MAE to evaluate the model's accuracy, along with a feature importance chart.🛠️ How to UseFollow these steps to set up and run the application on your local machine.PrerequisitesPython 3.8 or higherGit (for cloning the repository)Step 1: Clone the Repositorygit clone <your_repository_url>
cd <your_repository_name>
Step 2: Create and Activate a Virtual EnvironmentIt is highly recommended to use a virtual environment to manage dependencies.# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
Step 3: Install DependenciesAll required Python libraries are listed in the requirements.txt file.pip install -r requirements.txt
requirements.txtstreamlit
pandas
yfinance
plotly
scikit-learn
numpy
alpha_vantage
Step 4: Set up Your Alpha Vantage API Key (Optional but Recommended)For full functionality and to avoid rate limits with the "Auto" data source, you should get a free API key from Alpha Vantage and set it as an environment variable.Get a free API key from Alpha Vantage.Set the environment variable ALPHA_VANTAGE_API_KEY in your terminal.# For macOS / Linux
export ALPHA_VANTAGE_API_KEY="YOUR_API_KEY"

# For Windows
set ALPHA_VANTAGE_API_KEY="YOUR_API_KEY"
Note: You must run the streamlit run command from the same terminal session where you set the environment variable.Step 5: Run the ApplicationNow you can start the Streamlit application.streamlit run main_app.py
The application will automatically open in your web browser.📂 Project Structure.
├── main_app.py           # The main Streamlit application file
├── modules/              # Folder for custom Python modules
│   ├── __init__.py
│   ├── processing.py     # Data fetching, technical analysis, and ML model logic
│   └── ui.py             # UI components and styling
├── data/                 # Folder for sample data (used as a fallback)
│   └── sample_data.csv
└── requirements.txt      # List of project dependencies
⚠️ DisclaimerThis application is for educational and research purposes only. Stock price predictions are inherently uncertain and should never be used as the sole basis for investment decisions.Past performance does not guarantee future results.Market conditions can change rapidly and unpredictably.Always consult with qualified financial advisors.Conduct your own thorough research before making any investment decisions.Only invest what you can afford to lose.By using this application, you agree to these terms.📄 LicenseThis project is licensed under the MIT License.
