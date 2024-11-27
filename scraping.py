import requests
from bs4 import BeautifulSoup

def get_company_data(symbol, consolidated=False):
    base_url = "https://www.screener.in/company/"
    url = f"{base_url}{symbol}/{'consolidated/' if consolidated else ''}"

    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    company_data = {
        'pe_ratio': None,
        'roce_median': None,
        'compounded_sales_growth': None,
        'compounded_profit_growth': None
    }

    li_elements = soup.find_all('li', class_='flex flex-space-between', attrs={'data-source': 'default'})

    for li_element in li_elements:
        name_span = li_element.find('span', class_='name')

        if name_span and name_span.text.strip() == 'Stock P/E':
            pe_value = li_element.find('span', class_='number').text.strip()
            company_data['pe_ratio'] = pe_value

        elif name_span and name_span.text.strip() == 'ROCE':
            roce_value = li_element.find('span', class_='number').text.strip()
            company_data['roce_median'] = roce_value


    sales_growth_table = None
    profit_growth_table = None

    tables = soup.find_all('table', class_='ranges-table')
    for table in tables:
        rows = table.find_all('tr')
        
        first_row = rows[0]
        if first_row and "Compounded Sales Growth" in first_row.text:
            # print("Found Compounded Sales Growth")
            sales_growth_table = extract_table_data(rows)
        elif first_row and "Compounded Profit Growth" in first_row.text:
            # print("Found Compounded Profit Growth")
            profit_growth_table = extract_table_data(rows)

    # Store extracted data
    company_data['compounded_sales_growth'] = sales_growth_table
    company_data['compounded_profit_growth'] = profit_growth_table

    return company_data

def extract_table_data(rows):
    """
    Extracts data from a table by processing each row (tr) and returning a list of values.
    """
    data = []
    for row in rows[1:]:
        tds = row.find_all('td')
        if tds:
            row_data = [td.text.strip() for td in tds]
            data.append(row_data)
    return data