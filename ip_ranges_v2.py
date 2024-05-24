import requests
import pandas as pd
import ipaddress
from io import StringIO


def get_ip_ranges(country_url, owners):
    # Fetch the IP ranges for the given country
    response = requests.get(f"https://www.nirsoft.net/countryip/{country_url}")
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    isp_data = tables[-1]  # Assuming the last table contains the IP data
    print(f"Columns in ISP DataFrame: {isp_data.columns}")

    # Ensure correct column names and data filtering
    owner_column = next(col for col in isp_data.columns if 'owner' in col.lower())

    filtered_isp_data = isp_data[isp_data[owner_column].str.contains('|'.join(owners), case=False, na=False)]

    if filtered_isp_data.empty:
        print("No IP ranges found for the specified owners.")
        return

    # Determine the combined start and end IP addresses
    start_ip = min(filtered_isp_data['From IP'], key=lambda ip: ipaddress.ip_address(ip))
    end_ip = max(filtered_isp_data['To IP'], key=lambda ip: ipaddress.ip_address(ip))

    print(f"Start IP: {start_ip}")
    print(f"End IP: {end_ip}")
