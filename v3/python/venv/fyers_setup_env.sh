#!/bin/bash

# Function to install python3-venv if not already installed
install_venv() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install python3-venv -y
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew update
        brew install python3
    else
        echo "Error: Unsupported operating system. Please install 'python3-venv' manually."
        exit 1
    fi
}

# Check if venv module is installed
if ! python3 -m venv --help &>/dev/null; then
    echo "'venv' module not found. Installing 'python3-venv'..."
    install_venv
fi

# Define the name of the virtual environment
venv_name="fyers_env"

# Create virtual environment
python3 -m venv "$venv_name"

# Activate the virtual environment
source "$venv_name/bin/activate"

# Install fyers-api package
pip install fyers-sdk

# Deactivate the virtual environment (optional)
# deactivate
