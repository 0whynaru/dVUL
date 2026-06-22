#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}[!] Error: Please run root. Syntax: 'sudo su' setup only linux${NC}"
    exit 1
fi
echo ""
echo "[+] Installing dVUL in your terminal..."
echo ""
echo "Checking installation (playwright, chromium)..."
pip install requests playwright --break-system-packages
python3 -m playwright install chromium
chmod +x "$(pwd)/dVUL.py"
sudo ln -sf "$(pwd)/dVUL.py" /usr/local/bin/dvul
echo ""
echo "Arigatou Gozaimasu! may u happy to use it! >_<"
echo "[+] Done! Try: dvul -h"
echo ""
