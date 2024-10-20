import logging
from finvizfinance.screener.overview import Overview
import pandas as pd
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
FILTERS = {
    'Price': 'Over $5',
    'Market Cap.': '+Mid (over $2bln)',
    'Country': 'USA',
    'Industry': 'Stocks only (ex-Funds)',
}

PARAMETERS = [
    'Ticker', 
    'Exchange', 
    'Sector', 
    'Industry', 
    'Country', 
    'Market Cap.', 
    'closing price',
    'Curncy Name',
    'Exchange 0 (VND)',
    'Latest Price (Closing price)',
    '180Day Annualized Std Dev',
    'Simple Tot Ret (USD) Last Mo',
    'Last 12 Months Total Return',
    'Last 12 Months S&P 500 Total Return',
    'Last 12 Month Excess Return',
    '3y ALPHA Rel to Loc Idx',
    'In Buy List',
    'S&P 500 60 Mo Std Dev',
    'Bid Price',
    'Ask Price',
    '22D ADV ($MM)',
    '5000L by MCAP ($MM)',
    'Max Score',
    'Min Score',
    '1 Mo Fwd Return',
    'V&M Model Score',
    'V&M Score (IQR)',
    'PEG Model Score (W)',
    'PEG Model Score (IQR)',
    'Multi Factor Model Score (W)',
    'Multi Factor Model Score (IQR)',
    'N(0,1) Model Score',
    'N(0,Sigma) Model Score',
    'END OUTPUT',
    'PERFORMANCE',
    'Closing Price 10/31/14',
    'Closing Price 11/28/14',
    'Price Date 11/28/14',
    'Last Traded Price',
    'Price Date (Last)',
    'Closing Price',
    'Closing Price Date (YYMMDD)',
    'Divs Earned over Dates',
    'Calculated 1M Fwd Total Return',
    'MODEL 1: VAL & MOM',
    'Value & Momentum Score (W)',
    'Modified Val & Mom Score (W)',
    'Value & Momentum Score (IQR)',
    'Modified Val & Mom Score (IQR)',
    'MODEL 2: PEG',
    'LTM EPS',
    'Closing Price',
    'FE Eps Mean Annual_Roll',
    'FE Eps Mean Annual_Roll +5Y',
    '5yr Proj EPS growth',
    'PEG NEW 5YR PROJ. GRWTH',
    'PEG NEW 5YR PROJ. GRWTH STDev',
    'PEG New 5 Yr Proj Grth Windsor',
    '1/PEG NEW 5YR PROJ. GRWTH',
    '1/PEG Avail(Est,Hist)',
    'Earns Per Share -5Y',
    'Earns Per Share LTM',
    '5yr Hist Growth',
    'PEG NEW HIST GRWTH',
    'PEG NEW HIST GRWTH STDev',
    'PEG NEW HIST GRWTH Windsor',
    '1/PEG NEW HIST GRWTH',
    'Co Inter- quar- tile',
    '1/PEG New Hist Grth (IQR)',
    'Final 1/PEG (W)',
    'Final 1/PEG (IQR)',
    '1/PEG Score (W)',
    '1/PEG Score (IQR)',
    'Modified PEG Score (W)',
    'Modified PEG Score (IQR)',
    'MODEL 3 FACTOR 1 PEG',
    '1/PEG (W)',
    'PEG Score (W)',
    '1/PEG (IQR)',
    'PEG Score (IQR)',
    'MODEL 3 FACTOR 2 VALUE',
    'BV Per Sh',
    'Closing Price',
    'B/P',
    'B/P STDev',
    'B/P Windsor',
    'Value Score (W)',
    'Co Inter- quar- tile',
    'Value Score (IQR)',
    'MODEL 3 FACTOR 3 MOMENTUM',
    'Compound Tot Ret (LOCAL)',
    'Compound Tot Ret (LOCAL) STDev',
    'Compound Tot Ret (LOCAL) Windsor',
    'Momentum Score (W)',
    'Co Inter- quar- tile',
    'Momentum Score (IQR)',
    'MODEL 3 FACTOR 4 EPS SURPRISE',
    'FE Surp Amount Eps Quarterly_Roll',
    'FE Surp Amount Eps Quarterly_Roll STDev',
    'FE Surp Amount Eps Quarterly_Roll Winsdor',
    'Earnings Surprise Score (W)',
    'Co Inter- quar- tile',
    'Earnings Surprise Score (IQR)',
    'MODEL 3 FACTOR 5 QUALITY',
    'Ret on Avg Total Equity',
    'Ret on Avg Total Assets',
    'Net Income Margin',
    'Ret on Avg Total Equity STDev',
    'Ret on Avg Total Assets STDev',
    'Net Income Margin STDev',
    'Ret on Avg Total Equity (W)',
    'Ret on Avg Total Assets (W)',
    'Net Income Margin (W)',
    'ROE Score',
    'ROA Score',
    'Net Margin Score',
    'Co Inter- quar- tile',
    'Ret on Avg Total Equity (IQR)',
    'Ret on Avg Total Assets (IQR)',
    'Net Income Margin (IQR)',
    'Profitability Score (W)',
    'Profitability Score (IQR)',
    '5 yr Chg GP/Sales',
    '5 yr Chg GP/Sales STDev',
    '5 yr Chg GP/Sales Windsor',
    'Chg in GP/Sales Score (W)',
    'Chg in GP/Sales Score (IQR)',
    '5yr chg Net Inc/BV',
    '5yr chg Net Inc/BV STDev',
    '5yr chg Net Inc/BV Windsor',
    'Chg in NI/BV Score (W)',
    'Chg in NI/BV Score (IQR)',
    '5 yr Chg NI/Assets',
    '5 yr Chg NI/Assets STDev',
    '5 yr Chg NI/Assets Windsor',
    'Chg in NI/Assets Score (W)',
    'Chg in NI/Assets Score (IQR)',
    'Growth Score (W)',
    'Growth Score (IQR)',
    'Cash Divs Pd Cmn CF/NI',
    'Cash Divs Pd Cmn CF/NI STDev',
    'Cash Divs Pd Cmn CF/NI Windsor',
    'Div Pd Score (W)',
    'Common Shares Outstdg Curr',
    'Common Shares Outstdg -1y',
    'Pct Chg Shs Out',
    'Pct Chg Shs Out STDev',
    'Pct Chg Shs Out Windsor',
    'Chg Shs Outstdg Score (W)',
    'Chg Shs Outstdg Score (IQR)',
    'Payout Score (W)',
    'Payout Score (IQR)',
    'Total Debt% Total Equity',
    'Total Debt% Total Equity STDev',
    'Total Debt% Total Equity Windsor',
    'D/E Score (W)',
    'D/E Score (IQR)',
    'Pretax Int Cov',
    'Pretax Int Cov STDev',
    'Pretax Int Cov Windsor',
    'PreTax Int Cov Score (W)',
    'PreTax Int Cov Score (IQR)',
    'Safety Score (W)',
    'Safety Score (IQR)',
    'Quality Score (W)',
    'Quality Score (IQR)',
    'MODEL 3 FACTOR 6 ACCRUAL',
    'Change in Total Current Assets Q',
    'Change in Cash',
    'Change in Total Current Liabs Q',
    'Change in ST Debt Q',
    'Inc/Dec in Taxes Payable CF',
    'Chg in Depr Exp',
    'Accrual/ Total Assets',
    'Accrual STDev',
    'Accrual Windsor',
    'Norm Accrual Score (W)',
    'Norm Accrual Score (IQR)',
    'MODEL 3 FACTOR 7 BETA',
    '5 yr Beta',
    '5 yr Beta STDev',
    '5 yr Beta Windsor',
    'Norm Beta (W)',
    'Norm Beta (IQR)',
    'MODEL 3 FINAL SCORE',
    'Final Model Score (W)',
    'Modified Final Model 3 Score (W)',
    'Final Model Score (IQR)',
    'Modified Final Model 3 Score (IQR)',
    'MODEL N (0 1)',
    'Random',
    'Random -1/2',
    'N(0 1) Score',
    'MODEL N (0 SIGMA)',
    '60 Mo Std Dev',
    'U1',
    'U2',
    'Pi',
    'Theta',
    'R',
    'X',
    'X*Std Dev',
    'X*Std Dev STDev',
    'X*Std Dev Windsor',
    'N(0 sigma) Score',
    'Port_Shares',
    '10 Day Std Dev',
    '10D ADV ($MM)',
    '10D ADV Shares (MM)',
    '22D ADV Shares (MM)',
    'Total Assets',
    'Accruals- Formula'
]
    # More parameters can be added here
]

def get_stocks() -> pd.DataFrame:
    """
    Fetches stock data based on filters and returns it as a DataFrame.
    """
    foverview = Overview()

    try:
        foverview.set_filter(filters_dict=FILTERS)
        df_overview = foverview.screener_view(columns=PARAMETERS)
    except Exception as e:
        logger.error(f"Error retrieving data: {e}")
        return pd.DataFrame()

    return df_overview

def get_tickers():
    """
    Retrieves the list of tickers from the most recent stock data.
    """
    df_stocks = get_stocks()
    if not df_stocks.empty and 'Ticker' in df_stocks.columns:
        return df_stocks['Ticker'].tolist()
    else:
        logger.warning("No tickers found or 'Ticker' column missing.")
        return []

def main():
    st.title("Stock Screener App")
    st.write("This app retrieves stocks based on filters and displays them.")

    # Add filter description
    st.sidebar.header('Filters')
    selected_price = st.sidebar.selectbox('Price', ['Over $5', 'Over $10', 'Over $20'])
    selected_market_cap = st.sidebar.selectbox('Market Cap', ['+Mid (over $2bln)', '+Large (over $10bln)'])

    FILTERS['Price'] = selected_price
    FILTERS['Market Cap.'] = selected_market_cap

    if st.button('Get Stocks'):
        df_stocks = get_stocks()

        if not df_stocks.empty:
            st.success(f"Retrieved {len(df_stocks)} stocks")
            st.dataframe(df_stocks)

            # Allow downloading as CSV
            csv = df_stocks.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name='Overview.csv', mime='text/csv')
        else:
            st.error("No data retrieved. Try changing filters.")

if __name__ == "__main__":
    main()
