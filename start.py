import subprocess, sys

REQUIRED_PACKAGES = ["pandas", "openpyxl"]

def ensure_pip():
    try:
        import pip
    except ImportError:
        print("Pip not found, installing pip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

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
    ensure_pip()
    install_missing_packages()
    run_main()
