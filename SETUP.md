# Setup Instructions for Team Members

## Prerequisites

Before starting, make sure you have installed:

1. **Node.js 18+** - Download from https://nodejs.org
2. **Python 3.9+** - Download from https://python.org  
3. **Git** - Download from https://git-scm.com

---

## Step 1: Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd olap-assistant
```

---

## Step 2: Backend Setup

Open a terminal and run:

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file in the `backend` folder:

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` and add your API key:
```
LLM_API_KEY=<your-api-key-here>
```

> **Note:** Ask the project owner for the API key, or get your own from https://console.anthropic.com/

---

## Step 3: Frontend Setup

Open a **new terminal** and run:

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install
```

---

## Step 4: Run the Application

### Terminal 1 - Start Backend
```bash
cd backend
# Make sure virtual environment is activated
uvicorn server:app --reload --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

### Terminal 2 - Start Frontend
```bash
cd frontend
npm start
```

The browser will automatically open to http://localhost:3000

---

## Step 5: Verify Everything Works

1. Open http://localhost:3000 in your browser
2. You should see the dashboard with:
   - **11,000 records**
   - **~$224M Total Sales**
3. Try typing a query like: "Show sales by region"
4. The results should appear with a bar chart

---

## Quick Reference

| Component | URL | Port |
|-----------|-----|------|
| Frontend | http://localhost:3000 | 3000 |
| Backend API | http://localhost:8001/api | 8001 |
| API Docs | http://localhost:8001/api/docs | 8001 |

---

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify `.env` file exists with `LLM_API_KEY`

### Frontend won't start
- Make sure Node.js 18+ is installed: `node --version`
- Try deleting `node_modules` and running `npm install` again

### Queries don't work (no results)
- Check that `LLM_API_KEY` is set in `backend/.env`
- Check backend terminal for error messages

### Database is empty (0 records)
- The database auto-initializes on first startup
- Try restarting the backend

---

## Demo Checklist

Before presenting to the professor:

- [ ] Backend running without errors
- [ ] Frontend shows 11,000 records
- [ ] Natural language queries work
- [ ] Charts display correctly (Bar, Pie, Line, Area)
- [ ] Compare feature works
- [ ] Export to PDF works
- [ ] API docs accessible at /api/docs
