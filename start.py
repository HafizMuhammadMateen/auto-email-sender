import subprocess
import sys

REQUIRED_PACKAGES = ["pandas", "openpyxl"]

def ensure_pip():
    try:
        import pip
    except ImportError:
        print("⚠️ Pip not found, installing pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        except Exception as e:
            print("❌ Failed to install pip. Please install it manually.")
            sys.exit(1)

def install_missing_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"📦 Installing missing package: {package}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except Exception:
                print(f"❌ Could not install {package}. Please run: pip install {package}")
                sys.exit(1)

def run_main():
    try:
        subprocess.check_call([sys.executable, "auto_email_sender.py"])
    except Exception as e:
        print(f"❌ Failed to run main program: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ensure_pip()
    install_missing_packages()
    run_main()
