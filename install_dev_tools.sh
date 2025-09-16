#!/usr/bin/env bash
set -e

LOGFILE="install.log"

echo "=== Starting installation ===" | tee -a $LOGFILE

# Update system
sudo apt-get update -y >> $LOGFILE 2>&1

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "[*] Installing Docker..." | tee -a $LOGFILE
    sudo apt-get install -y docker.io >> $LOGFILE 2>&1
    sudo systemctl enable docker --now
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "[*] Installing Docker Compose..." | tee -a $LOGFILE
    sudo apt-get install -y docker-compose >> $LOGFILE 2>&1
fi

# Install Python >=3.9
if ! command -v python3 &> /dev/null; then
    echo "[*] Installing Python..." | tee -a $LOGFILE
    sudo apt-get install -y python3 python3-pip python3-venv >> $LOGFILE 2>&1
fi

# Upgrade pip
python3 -m pip install --upgrade pip >> $LOGFILE 2>&1

# Install ML dependencies
python3 -m pip install torch torchvision pillow >> $LOGFILE 2>&1

# Verify
echo "=== Versions installed ===" | tee -a $LOGFILE
docker --versi
