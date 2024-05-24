import requests
import pandas as pd
import ipaddress
from io import StringIO
from bs4 import BeautifulSoup
import sys


def get_country_url(country_code):
    url = "https://www.nirsoft.net/countryip/"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    soup = BeautifulSoup(response.text, "html.parser")
    country_links = {a['href'].split('.')[0].strip().lower(): a['href'] for a in soup.find_all('a') if
                     a['href'].endswith('.html')}
    return country_links.get(country_code, None)


def get_ip_ranges(country_url, owners):
    # Fetch the IP ranges for the given country
    response = requests.get(f"https://www.nirsoft.net/countryip/{country_url}")
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    isp_data = tables[-1]  # Assuming the last table contains the IP data
    # Debug
    # print(f"Columns in ISP DataFrame: {isp_data.columns}")

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


def main():
    country = input("Enter the country code (e.g., nl for Netherlands): ").strip().lower()
    owner = input("Enter the IP address owners to filter (comma-separated, e.g., Ziggo, KPN, Odido): ").strip().lower()
    owners_list = [o.strip() for o in owner.split(',')]

    country_url = get_country_url(country)
    if not country_url:
        print(f"Country code '{country}' not found on the website. Please enter a valid country code.")
        sys.exit(1)

    print("Note: This script is specifically made for: https://www.nirsoft.net/countryip/")
    get_ip_ranges(country_url, owners_list)
