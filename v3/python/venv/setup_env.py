import os
import platform
import subprocess
import sys

# Function to install python3-venv if not already installed (for Unix-based systems)
def install_venv():
    if platform.system() == "Linux":
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install", "python3-venv", "-y"])
    elif platform.system() == "Darwin":
        subprocess.run(["brew", "update"])
        subprocess.run(["brew", "install", "python3"])
    else:
        try:
            import venv  # Check if venv module is available
        except ImportError:
            print("venv module not found. Installing 'virtualenv' package using pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "virtualenv"])


# Check if venv module is installed
try:
    from venv import EnvBuilder
except ImportError:
    print("'venv' module not found. Installing 'python3-venv'...")
    install_venv()

# Define the name of the virtual environment
venv_name = "fyers_env"

# Create virtual environment
builder = subprocess.run([sys.executable, "-m", "venv", venv_name], capture_output=True)

# Handle potential permission issues
if builder.returncode != 0:
    print("Error creating virtual environment. Trying to resolve permissions...")
    if platform.system() == "Windows":
        os.chmod(venv_name, 0o755)  # Set the virtual environment directory to have read, write, and execute permissions
    else:
        os.chmod(venv_name, 0o700)  # Set the virtual environment directory to have read, write, and execute permissions only for the owner
    builder = subprocess.run([sys.executable, "-m", "venv", venv_name], capture_output=True)

if builder.returncode != 0:
    print("Error creating virtual environment. Please check permissions and try again.")
    exit(1)


# Activate the virtual environment
activate_script = "activate.bat" if platform.system() == "Windows" else "activate"
activate_path = os.path.join(venv_name, "Scripts" if platform.system() == "Windows" else "bin", activate_script)
subprocess.run([activate_path], shell=True)

# Install fyers-api package (use pip in the virtual environment)
subprocess.run([os.path.join(venv_name, "Scripts" if platform.system() == "Windows" else "bin", "pip"), "install", "fyers-sdk"])

# Deactivate the virtual environment (only for Windows)
if platform.system() == "Windows":
    subprocess.run(["deactivate"], shell=True)
