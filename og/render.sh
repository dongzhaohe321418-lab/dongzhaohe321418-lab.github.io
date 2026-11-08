#!/bin/sh
# Render og/og.html to og.png (2400x1254, i.e. 1200x627 at 2x) with headless Chrome.
cd "$(dirname "$0")" && python3 make_og.py && \
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1200,627 --virtual-time-budget=6000 \
  --screenshot="$PWD/../og.png" "file://$PWD/og.html" 2>/dev/null
sips -g pixelWidth -g pixelHeight ../og.png | tail -2
