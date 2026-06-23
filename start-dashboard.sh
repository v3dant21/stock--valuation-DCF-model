#!/bin/bash

# Stock Valuation Dashboard Startup Script

echo "🚀 Starting Stock Valuation Dashboard..."
echo ""

# Check if we're in the right directory
if [ ! -d "src/stock_valuation" ]; then
    echo "❌ Error: Please run this script from the stock_valuation directory"
    exit 1
fi

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "python -m stock_valuation.api" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
sleep 1

# Start Flask API
echo "📊 Starting Flask API on port 5000..."
PYTHONPATH=src python -m stock_valuation.api &
API_PID=$!
echo "✓ API started (PID: $API_PID)"

# Wait for API to be ready
echo "⏳ Waiting for API to initialize..."
for i in {1..10}; do
    if curl -s http://localhost:5000/api/valuation > /dev/null 2>&1; then
        echo "✓ API is ready!"
        break
    fi
    sleep 1
done

# Start React frontend
echo "🎨 Starting React frontend on port 5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "✓ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "✅ Dashboard is running!"
echo ""
echo "📍 Frontend: http://localhost:5173 (or next available port)"
echo "📍 API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Trap to cleanup on exit
trap "kill $API_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '👋 Servers stopped'; exit" INT TERM

# Wait for both processes
wait
