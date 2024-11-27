# Financial Analysis & Intrinsic Value Calculator

This Streamlit app fetches financial data for companies from Screener.in and calculates intrinsic value using a discounted cash flow (DCF) model. It provides a user-friendly interface with visualizations and detailed metrics.

---

## Features

### 1. **Current Financial Data**
- Fetches P/E ratio, ROCE Median, and other financial metrics for a given company.
- Displays Compounded Sales Growth and Profit Growth in a tabular format.

### 2. **Intrinsic Value Calculation**
- Calculates intrinsic P/E and value using the DCF model based on:
  - Cost of capital
  - ROCE
  - Growth rate
  - High-growth years
  - Fade period
  - Terminal growth rate
- Generates visualizations for key metrics:
  - NOPAT vs Year
  - Capital Ending vs Year
  - Free Cash Flow (FCF) vs Year
  - Discounted FCF vs Year
  - Investment vs Year
- Provides a comprehensive DCF table.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Streamlit installed (`pip install streamlit`)
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `matplotlib`
  - `seaborn`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/hrshpreet/streamlit-financial-calculator
   cd streamlit-financial-calculator

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

