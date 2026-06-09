#!/bin/bash

echo ""
echo "  Installing dVUL..."
echo ""
sleep(1)
echo "Checking installation (playwright, chromium)"
sleep(1)
# Install dependencies
pip install requests playwright --break-system-packages
# Install Chromium untuk Playwright
python3 -m playwright install chromium

# Kasih permission execute ke main.py
chmod +x "$(pwd)/dvul.py"

# Bikin symlink ke /usr/local/bin biar bisa dipanggil dari mana aja
sudo ln -sf "$(pwd)/dvul.py" /usr/local/bin/dvul

echo ""
echo "  [+] Done! Try: dvul -h"
echo ""