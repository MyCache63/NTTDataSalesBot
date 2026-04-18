#!/bin/bash
# Start the NTT DATA / Trinity Health Sentiment Analytics Demo
# Powered by Kore.ai + Claude AI

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

case "${1}" in
  --stop)
    echo "Stopping sentiment demo server..."
    pkill -f "python3 server.py" 2>/dev/null || echo "No server running."
    exit 0
    ;;
  --restart)
    echo "Restarting..."
    pkill -f "python3 server.py" 2>/dev/null
    sleep 1
    ;;
esac

# Load API key from .env if not already set
if [ -z "$ANTHROPIC_API_KEY" ] && [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠  ANTHROPIC_API_KEY not set."
    echo "   Create a .env file with: ANTHROPIC_API_KEY=your-key-here"
    echo "   The demo will load but analysis won't work without it."
    echo ""
fi

# Check dependencies
python3 -c "import flask, anthropic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install flask anthropic
fi

echo ""
echo "========================================"
echo "  NTT DATA / Trinity Health"
echo "  Sentiment Analytics Demo"
echo "  Powered by Kore.ai + Claude AI"
echo "========================================"
echo ""
echo "  Opening http://localhost:5001"
echo "  Press Ctrl+C to stop"
echo ""

# Open browser after a short delay
(sleep 2 && open http://localhost:5001) &

python3 server.py
