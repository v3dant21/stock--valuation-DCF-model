# Troubleshooting CORS Issues

## Problem: CORS Request Did Not Succeed

### Solution 1: Ensure Backend is Running

Check if Flask API is running:
```bash
curl http://localhost:5000/api/valuation
```

If connection fails, start the backend:
```bash
cd stock_valuation
PYTHONPATH=src python -m stock_valuation.api
```

### Solution 2: Use the Startup Script

The script ensures proper startup order:
```bash
./start-dashboard.sh
```

### Solution 3: Manual Startup (Recommended)

**Terminal 1 - Start Backend First:**
```bash
cd stock_valuation
PYTHONPATH=src python -m stock_valuation.api
```

Wait for message: `Running on http://127.0.0.1:5000`

**Terminal 2 - Then Start Frontend:**
```bash
cd stock_valuation/frontend
npm run dev
```

### Solution 4: Check if Port 5000 is Busy

```bash
# Linux/Mac
lsof -i :5000

# If something is using it, kill it
kill -9 <PID>
```

### Solution 5: Test API Directly

```bash
curl -X POST http://localhost:5000/api/valuation \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","revenueGrowth":0.10,"terminalGrowth":0.025}'
```

Should return JSON with valuation data.

## Common Issues

### Issue: Flask Not Installing Dependencies
```bash
pip install -r requirements.txt
```

### Issue: Frontend Can't Find API
Check the API URL in Dashboard.jsx (line ~20):
```javascript
const response = await fetch('http://localhost:5000/api/valuation', {
```

Make sure it matches where Flask is running.

### Issue: CORS Policy Error Even with Backend Running

This usually means Flask crashed. Check for errors:
```bash
# Look at Flask console output for Python errors
# Common: Missing dependencies, import errors
```

## Verification Checklist

- [ ] Flask API running on port 5000
- [ ] React dev server running on port 5173 (or next available)
- [ ] Can access http://localhost:5000 in browser
- [ ] curl command returns JSON (not HTML error)
- [ ] No Python errors in Flask terminal
- [ ] Browser console shows network request to /api/valuation

## Still Not Working?

Try restarting both servers:
```bash
# Kill all processes
pkill -f "python -m stock_valuation.api"
pkill -f "vite"

# Start fresh
./start-dashboard.sh
```
