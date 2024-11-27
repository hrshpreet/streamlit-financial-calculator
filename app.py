import streamlit as st
from scraping import get_company_data
from dcf_model import calculate_intrinsic_pe
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
    
symbol = st.sidebar.text_input("Enter NSE/BSE Symbol:", "NESTLEIND")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ("Current Financial Data", "Intrinsic Calculation"))


if page == "Current Financial Data":
    company_data = get_company_data(symbol)
    if company_data:
        st.title('Company Financial Overview')

        st.subheader("Key Financial Metrics")
        st.write(f"**P/E Ratio**: {company_data['pe_ratio']}")
        st.write(f"**ROCE Median**: {company_data['roce_median']}"+"%")

        st.subheader("Compounded Sales Growth")
        sales_growth_df = pd.DataFrame(company_data["compounded_sales_growth"], columns=["Period", "Growth"])
        st.table(sales_growth_df)

        st.subheader("Compounded Profit Growth")
        profit_growth_df = pd.DataFrame(company_data["compounded_profit_growth"], columns=["Period", "Growth"])
        st.table(profit_growth_df)
    else:
        st.error("Failed to fetch data. Please check the symbol.")


elif page == "Intrinsic Calculation":    
    cost_of_capital = st.slider("Cost of Capital (%)", 8.0, 16.0, 11.0, step=1.0)
    roce = st.slider("ROCE (%)", 10.0, 100.0, 95.0, step=10.0)
    growth_rate = st.slider("Growth Rate (%)", 8.0, 20.0, 15.0, step=2.0)
    high_growth_years = st.slider("High Growth Period (years)", 10, 25, 15, step=2)
    fade_years = st.slider("Fade Period (years)", 5, 20, 15, step=5)
    terminal_growth_rate = st.slider("Terminal Growth Rate (%)", 0.0, 7.5, 5.0, step=0.5)

    cost_of_capital = cost_of_capital/100
    roce = roce/100
    growth_rate = growth_rate/100
    terminal_growth_rate = terminal_growth_rate/100

    tax_rate = 25 / 100  # 25%
    roce_post_tax = roce * (1 - tax_rate)
    reinvestment_rate_1 = growth_rate / roce_post_tax
    reinvestment_rate_2 = terminal_growth_rate / roce_post_tax   
    
    columns = ["Year", "Earnings Growth Rate(%)", "EBT", "NOPAT", "Capital Ending","Investment", "FCF", "Discount Factor", "Discounted FCF"]
    
    capital_ending = 100
    growth = growth_rate
    investment = 0
    data = []
    
    for year in range(-1, high_growth_years+fade_years+1):
        if year == -1:
            capital_ending = 100
            nopat = None
            investment = None
            ebt = None
            fcf = None
            discount_factor = None
            discounted_fcf = None
        else:
            if year <= high_growth_years:
                growth = growth_rate
            else: 
                growth = growth - ((growth_rate - terminal_growth_rate) / fade_years)
            
            nopat = capital_ending * roce_post_tax 
            ebt = nopat / (1 - tax_rate)
            
            if year <= high_growth_years:
                investment = nopat * reinvestment_rate_1 
            else:
                investment = growth / roce_post_tax * nopat

            capital_ending = capital_ending + investment 
            
            fcf = nopat - investment
            discount_factor = 1 / (1 + cost_of_capital) ** year
            discounted_fcf = fcf * discount_factor

            data.append([
                year,
                round(growth*100, 2) if growth is not None else None,
                round(ebt, 2) if ebt is not None else None,
                round(nopat, 2) if nopat is not None else None,
                round(capital_ending, 2),
                round(investment, 2) if investment is not None else None,
                round(fcf, 2) if fcf is not None else None,
                round(discount_factor, 2) if discount_factor is not None else None,
                round(discounted_fcf, 2) if discounted_fcf is not None else None,
            ])
    
    df = pd.DataFrame(data, columns=columns)

    #1. Plotting NOPAT vs Year
    def plot_nopat_vs_year():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Year', y='NOPAT', ax=ax)
        ax.set_title("NOPAT vs Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("NOPAT")
        st.pyplot(fig)

    # 2. Plotting Capital Ending vs Year
    def plot_capital_ending_vs_year():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Year', y='Capital Ending', color='green', ax=ax)
        ax.set_title("Capital Ending vs Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Capital Ending")
        st.pyplot(fig)

    # 3. Plotting FCF vs Year
    def plot_fcf_vs_year():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Year', y='FCF', color='red', ax=ax)
        ax.set_title("FCF vs Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("FCF")
        st.pyplot(fig)

    # 4. Plotting Discounted FCF vs Year
    def plot_discounted_fcf_vs_year():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Year', y='Discounted FCF', color='blue', ax=ax)
        ax.set_title("Discounted FCF vs Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Discounted FCF")
        st.pyplot(fig)

    # 5. Plotting Investment vs Year
    def plot_investment_vs_year():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Year', y='Investment', color='purple', ax=ax)
        ax.set_title("Investment vs Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Investment")
        st.pyplot(fig)

    st.title("Financial Metrics Over Time")
    st.header("Visualizations of Key Metrics")

    plot_nopat_vs_year()
    plot_capital_ending_vs_year()
    plot_fcf_vs_year()
    plot_discounted_fcf_vs_year()
    plot_investment_vs_year()
    
    st.subheader("Discounted Cash Flow Table")
    st.table(df.style.format(precision=2))