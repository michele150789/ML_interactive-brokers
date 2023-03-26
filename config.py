from datetime import datetime, date, timedelta
import os

today = date.today().strftime("%Y%m%d")

#### for testing ######
#today = '20230325'

found_match = False
days_back = 30
max_days_back = 35
file_list = os.listdir(r'C:\Users\Michele\Desktop\ib_code\data')

# take the first data downloaded more than 30 days ago

while not found_match and days_back <= max_days_back:
    # Generate the search string based on the number of days back
    one_month = (datetime.now() - timedelta(days_back)).strftime("%Y%m%d")
    print(one_month)
    
    # Check if any files match the search string
    matching_files = [filename for filename in file_list if one_month in filename]
    print(matching_files)
    
    if matching_files:
        found_match = True
    days_back += 1
    
if not found_match:
    print("No matching files found.")

number_of_stocks = [10,25,40,55,100]

path = r'C:\Users\Michele\Desktop\ib_code\\'
ticker_list = path + '\input\Stock_Universe.xlsx'
dir_control_file = path +'\excel_file_control\\'
dir_output = path +'\data\\'

ml_model_file_10 = path +'\ml_models\finalized_model_10.sav'
ml_model_file_20 = path +'\ml_models\finalized_model_20.sav'
ml_model_file_30 = path +'\ml_models\finalized_model_30.sav'
ml_model_file_40 = path +'\ml_models\finalized_model_40.sav'
ml_model_file_50 = path +'\ml_models\finalized_model_50.sav'


col_list=['Avg Volume','Shs Float', 'Income', 'Shs Outstand', 'Market Cap', 'Sales','Insider Own',	'Perf Week', 
'EPS next Y', 'Insider Trans', 'Perf Month','Inst Own','Perf Quarter','EPS this Y','Inst Trans', 
'Short Float', 'Perf Half Y','ROA', 'Perf Year','EPS next 5Y','ROE','Perf YTD',
'EPS past 5Y','ROI','52W High','Dividend %','Sales past 5Y', 'Gross Margin','52W Low','Sales Q/Q','Oper. Margin',
'Oper. Margin','Volatility W','Volatility M','EPS Q/Q','Profit Margin', 'Payout', 'SMA20','SMA50','SMA200']


col_to_keep = ['Sector', 'Industry', 'P/E', 'EPS (ttm)',
'Insider Own', 'Perf Week', 'Market Cap', 'Forward P/E',
'EPS next Y', 'Insider Trans',  'Perf Month',
'PEG', 'EPS next Q', 'Inst Own', 'Short Float', 'Perf Quarter', 
'P/S', 'EPS this Y', 'Inst Trans',  'Perf Half Y',
'Book/sh', 'P/B', 'ROA',  'Perf Year', 'Cash/sh', 'P/C',
'EPS next 5Y', 'ROE',  'Perf YTD',
'P/FCF', 'EPS past 5Y', 'ROI', '52W High', 'Beta',
'Dividend %', 'Quick Ratio', 'Sales past 5Y', 'Gross Margin', '52W Low',
'ATR',  'Current Ratio', 'Sales Q/Q', 'Oper. Margin',
'RSI (14)', 'Volatility W', 'Volatility M', 'Debt/Eq',
'EPS Q/Q', 'Profit Margin', 'Rel Volume', 
'LT Debt/Eq', 'Payout',  'Price', 'Recom',
'SMA20', 'SMA50', 'SMA200', 'Ticker']

col_to_keep_2 = ['Sector', 'Industry', 'P/E', 'EPS (ttm)',
'Insider Own', 'Perf Week', 'Market Cap', 'Forward P/E',
'EPS next Y', 'Insider Trans',  'Perf Month',
'PEG', 'EPS next Q', 'Inst Own', 'Short Float','Perf Quarter', 
'P/S', 'EPS this Y', 'Inst Trans', 'Perf Half Y',
'Book/sh', 'P/B', 'ROA',  'Perf Year', 'Cash/sh', 'P/C',
'EPS next 5Y', 'ROE',  'Perf YTD',
'P/FCF', 'EPS past 5Y', 'ROI', '52W High', 'Beta',
'Dividend %', 'Quick Ratio', 'Sales past 5Y', 'Gross Margin', '52W Low',
'ATR',  'Current Ratio', 'Sales Q/Q', 'Oper. Margin',
'RSI (14)', 'Volatility W', 'Volatility M', 'Debt/Eq',
'EPS Q/Q', 'Profit Margin', 'Rel Volume', 
'LT Debt/Eq', 'Payout',  'Price', 'Recom',
'SMA20', 'SMA50', 'SMA200', 'Ticker','sharpe_ratio',
'sharpe_ratio_t0','decile']

sector_map = {'Healthcare': 11, 'Industrials': 1, 'Consumer Cyclical': 2, 'Technology': 3, 'Consumer Defensive': 4, 'Utilities': 5, 'Financial': 6, 
'Basic Materials': 7, 'Real Estate': 8, 'Energy': 9, 'Communication Services': 10 } 

industry_map = {'NA': 0, 'Airlines': 1, 'Specialty Retail': 2, 'Consumer Electronics': 3, 'Drug Manufacturers - General': 4, 
'Medical Distribution': 5, 'Medical Devices': 6, 'Information Technology Services': 7, 'Software - Infrastructure': 8, 
'Semiconductors': 9, 'Farm Products': 10, 'Staffing & Employment Services': 11, 'Software - Application': 12, 'Utilities - Regulated Electric': 13, 
'Utilities - Diversified': 14, 'Insurance - Life': 15, 'Insurance - Diversified': 16, 'Insurance - Specialty': 17, 'Insurance Brokers': 18, 
'Specialty Chemicals': 19, 'Insurance - Property & Casualty': 20, 'Security & Protection Services': 21, 'Semiconductor Equipment & Materials': 22, 
'Packaging & Containers': 23, 'Specialty Industrial Machinery': 24, 'Asset Management': 25, 'REIT - Specialty': 26, 'Internet Retail': 27, 
'Computer Hardware': 28, 'Healthcare Plans': 29, 'Oil & Gas E&P': 30, 'Chemicals': 31, 'Electronic Components': 32, 'Auto Parts': 33, 
'REIT - Office': 34, 'Utilities - Regulated Gas': 35, 'Electronic Gaming & Multimedia': 36, 'REIT - Residential': 37, 'Business Equipment & Supplies': 38,
'Utilities - Regulated Water': 39, 'Credit Services': 40, 'Aerospace & Defense': 41, 'Banks - Diversified': 42, 'Medical Instruments & Supplies': 43,
'Beverages - Wineries & Distilleries': 44, 'Travel Services': 45, 'Oil & Gas Equipment & Services': 46, 'Packaged Foods': 47, 
'Building Products & Equipment': 48, 'Farm & Heavy Construction Machinery': 49, 'Financial Data & Stock Exchanges': 50, 'Real Estate Services': 51, 
'Health Information Services': 52, 'Agricultural Inputs': 53, 'Banks - Regional': 54, 'Household & Personal Products': 55, 'Integrated Freight & Logistics': 56, 
'Entertainment': 57, 'Restaurants': 58, 'Discount Stores': 59, 'Specialty Business Services': 60, 'Communication Equipment': 61, 'Railroads': 62, 
'Drug Manufacturers - Specialty & Generic': 63, 'Oil & Gas Integrated': 64, 'Resorts & Casinos': 65, 'Residential Construction': 66, 'REIT - Industrial': 67,
'Medical Care Facilities': 68, 'Consulting Services': 69, 'Solar': 70, 'Auto Manufacturers': 71, 'Industrial Distribution': 72, 'Internet Content & Information': 73,
'Furnishings, Fixtures & Appliances': 74, 'Copper': 75, 'Broadcasting': 76, 'REIT - Retail': 77, 'Scientific & Technical Instruments': 78, 'Apparel Retail': 79, 
'Capital Markets': 80, 'Leisure': 81, 'Apparel Manufacturing': 82, 'Home Improvement Retail': 83, 'Lodging': 84, 
'REIT - Hotel & Motel': 85, 'Confectioners': 86, 'Biotechnology': 87, 'Advertising Agencies': 88, 'Engineering & Construction': 89,
'Oil & Gas Midstream': 90, 'Auto & Truck Dealerships': 91, 'Beverages - Non-Alcoholic': 92, 'Grocery Stores': 93, 'Telecom Services': 94, 'Building Materials': 95,
'Tobacco': 96, 'Oil & Gas Refining & Marketing': 97, 'Gold': 98, 'Footwear & Accessories': 99, 'Utilities - Independent Power Producers': 100, 'Steel': 101, 
'Trucking': 102, 'REIT - Healthcare Facilities': 103, 'Insurance - Reinsurance': 104, 'Personal Services': 105, 'Waste Management': 106, 'Tools & Accessories': 107, 
'Food Distribution': 108, 'Beverages - Brewers': 109, 'Luxury Goods': 110, 'Rental & Leasing Services': 111, 'Pharmaceutical Retailers': 112, 'Diagnostics & Research': 113,
'Thermal Coal': 114, 'Other Industrial Metals & Mining':115}

