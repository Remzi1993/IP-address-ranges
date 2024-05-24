import sys
import subprocess

# Function to check and install required packages
def install(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

required_packages = ["requests", "pandas", "ipaddress", "html5lib", "beautifulsoup4"]

# Check for each required package and install if not present
for package_name in required_packages:
    try:
        __import__(package_name)
    except ImportError:
        print(f"Package '{package_name}' not found. Installing...")
        install(package_name)

# Import the script with the main functionality
import ip_ranges_v2
import requests
from bs4 import BeautifulSoup

def get_country_url(country_code):
    url = "https://www.nirsoft.net/countryip/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    country_links = {a['href'].split('.')[0].strip().lower(): a['href'] for a in soup.find_all('a') if a['href'].endswith('.html')}
    return country_links.get(country_code, None)

if __name__ == "__main__":
    country = input("Enter the country code (e.g., nl for Netherlands): ").strip().lower()
    owner = input("Enter the IP address owners to filter (comma-separated, e.g., Ziggo, KPN, Odido): ").strip().lower()
    owners_list = [o.strip() for o in owner.split(',')]

    country_url = get_country_url(country)
    if not country_url:
        print(f"Country code '{country}' not found on the website. Please enter a valid country code.")
        sys.exit(1)

    print("Note: This script is specifically made for https://www.nirsoft.net/countryip/ for a table with 5 columns.")
    ip_ranges_v2.get_ip_ranges(country_url, owners_list)
