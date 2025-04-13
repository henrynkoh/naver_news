import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 7):
        print(f"Error: Python 3.7 or higher is required. You have {major}.{minor}")
        return False
    return True

def install_dependencies():
    """Install the required dependencies"""
    print("Installing dependencies...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error installing dependencies: {result.stderr}")
            return False
        print("Dependencies installed successfully!")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run_app():
    """Run the Streamlit app"""
    print("\nStarting Naver News Downloader web app...")
    try:
        # Get IP address to display
        if platform.system() == "Windows":
            ip_cmd = subprocess.run(["ipconfig"], capture_output=True, text=True)
            for line in ip_cmd.stdout.split('\n'):
                if "IPv4 Address" in line:
                    ip = line.split(":")[-1].strip()
                    break
            else:
                ip = "localhost"
        else:  # Linux/Mac
            try:
                ip_cmd = subprocess.run(["ifconfig"], capture_output=True, text=True)
                for line in ip_cmd.stdout.split('\n'):
                    if "inet " in line and "127.0.0.1" not in line:
                        ip = line.split("inet ")[1].split(" ")[0]
                        break
                else:
                    ip = "localhost"
            except:
                ip = "localhost"
        
        print(f"\nYou can access the app on your mobile device at: http://{ip}:8501")
        print("Starting local server...")
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        return True
    except Exception as e:
        print(f"Error starting app: {str(e)}")
        if "No module named 'streamlit'" in str(e):
            print("Streamlit not found. Please make sure dependencies are installed.")
        return False

def main():
    print("=" * 60)
    print("Naver News Downloader Web App Setup")
    print("=" * 60)
    
    if not check_python_version():
        print("Setup failed: Python version requirement not met")
        return
    
    if not install_dependencies():
        print("Setup failed: Could not install dependencies")
        return
        
    print("\nSetup completed successfully!")
    
    run_app()

if __name__ == "__main__":
    main() 