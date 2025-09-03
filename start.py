import subprocess
import sys

REQUIRED_PACKAGES = ["pandas", "openpyxl"]

def install_missing_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_main():
    subprocess.check_call([sys.executable, "auto_email_sender.py"])

if __name__ == "__main__":
    install_missing_packages()
    run_main()
