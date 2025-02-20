import sys
import subprocess
import importlib.util
import platform

# Function to check and install required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# List of packages to check and install if necessary
required_packages = ["requests", "pandas", "bs4", "html5lib"]

# Check for each required package and install if not present
for package_name in required_packages:
    if importlib.util.find_spec(package_name) is None:
        print(f"Package '{package_name}' not found. Installing...")
        install(package_name)

# Import the script with the main functionality
import ip_ranges_v2

if __name__ == "__main__":
    ip_ranges_v2.main()

    # Add this block to wait for the user to press any key before closing
    if platform.system() == "Windows" and hasattr(sys, 'frozen'):
        print("Press any key to exit...")
        import msvcrt

        msvcrt.getch()
    else:
        input("Press Enter to exit...")
