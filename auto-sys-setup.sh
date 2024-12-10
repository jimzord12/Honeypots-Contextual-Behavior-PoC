#!/bin/bash

# Define colors for output
GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${GREEN}Starting project setup...${RESET}"

# Step 1: Update and Install Linux Dependencies
echo -e "${GREEN}Installing Linux dependencies...${RESET}"
sudo apt update && sudo apt upgrade -y

# Python 3.11
echo -e "${GREEN}Installing Python 3.11...${RESET}"
sudo apt install -y python3.11 python3.11-venv python3.11-distutils

# tmux
echo -e "${GREEN}Installing tmux...${RESET}"
sudo apt install -y tmux

# Node.js (LTS)
echo -e "${GREEN}Installing Node.js LTS...${RESET}"
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Go Programming Language
echo -e "${GREEN}Installing Go...${RESET}"
GO_VERSION="1.23.4" # Replace with the desired version
wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz
rm go${GO_VERSION}.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.bashrc

# Step 2: Node.js Dependencies
echo -e "${GREEN}Installing Node.js dependencies...${RESET}"
npm install

# Step 3: Go Dependencies
echo -e "${GREEN}Installing Go dependencies...${RESET}"
cd apiserver || exit 1
go mod tidy
cd ..

# Step 4: Python Dependencies
echo -e "${GREEN}Installing Python dependencies...${RESET}"
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r combined-requirements.txt
deactivate

# Step 5: Create Required Directories
echo -e "${GREEN}Creating required directories...${RESET}"
mkdir -p logs

# Step 6: Verify Installation
echo -e "${GREEN}Verifying installations...${RESET}"
python3 --version || { echo -e "${RED}Python installation failed!${RESET}"; exit 1; }
node --version || { echo -e "${RED}Node.js installation failed!${RESET}"; exit 1; }
go version || { echo -e "${RED}Go installation failed!${RESET}"; exit 1; }
tmux -V || { echo -e "${RED}tmux installation failed!${RESET}"; exit 1; }

echo -e "${GREEN}Setup complete! You can now run the project.${RESET}"
