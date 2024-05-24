import requests
import pandas as pd
import ipaddress
from io import StringIO

# Fetch the webpage
url = "https://www.nirsoft.net/countryip/nl.html"
response = requests.get(url)
response.raise_for_status()

# Parse the HTML tables
tables = pd.read_html(StringIO(response.text))

# Identify the correct table by checking its contents
isp_data = None
for table in tables:
    if 'From IP' in table.columns and 'To IP' in table.columns:
        isp_data = table
        break

if isp_data is None:
    raise ValueError("Relevant table not found")

# Print the columns to debug
print("Columns in ISP DataFrame:", isp_data.columns)

# Define the allowed ISPs
allowed_isps = ["Ziggo", "KPN", "Odido"]

# Assuming the 'Owner' column might have different capitalization or extra spaces
owner_column = None
for column in isp_data.columns:
    if 'owner' in column.lower():
        owner_column = column
        break

if owner_column is None:
    raise ValueError("Owner column not found in the ISP data")

# Filter the dataframe for the allowed ISPs
filtered_isp_data = isp_data[isp_data[owner_column].str.contains('|'.join(allowed_isps), case=False, na=False)]


# Function to convert IP range to CIDR
def ip_range_to_cidr(start_ip, end_ip):
    start = ipaddress.ip_address(start_ip)
    end = ipaddress.ip_address(end_ip)
    return [str(c) for c in ipaddress.summarize_address_range(start, end)]


filtered_cidrs = []
for _, row in filtered_isp_data.iterrows():
    start_ip = row["From IP"]
    end_ip = row["To IP"]
    cidrs = ip_range_to_cidr(start_ip, end_ip)
    filtered_cidrs.extend(cidrs)

# Find the overall start and end IP addresses
all_start_ips = []
all_end_ips = []

for cidr in filtered_cidrs:
    network = ipaddress.ip_network(cidr)
    all_start_ips.append(network[0])
    all_end_ips.append(network[-1])

# Calculate the minimum start IP and maximum end IP
overall_start_ip = min(all_start_ips)
overall_end_ip = max(all_end_ips)

# Print the overall start and end IP addresses
print(f"Start IP: {overall_start_ip}")
print(f"End IP: {overall_end_ip}")
