import sys
import subprocess
import importlib.util


# Function to check and install required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


required_packages = ["requests", "pandas", "ipaddress", "html5lib", "beautifulsoup4"]

# Check for each required package and install if not present
for package_name in required_packages:
    if importlib.util.find_spec(package_name) is None:
        print(f"Package '{package_name}' not found. Installing...")
        install(package_name)

# Import the script with the main functionality
import ip_ranges_v2

if __name__ == "__main__":
    ip_ranges_v2.main()
