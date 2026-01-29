# OLAP Assistant - Local Setup Guide (Step-by-Step)

This guide will help you run the OLAP Assistant on your local computer. Follow each step carefully.

---

## PART 1: INSTALL REQUIRED SOFTWARE

### 1.1 Install Node.js

1. Open your browser and go to: **https://nodejs.org/**
2. Click the **LTS** version (recommended) - should say something like "20.x LTS"
3. Download and run the installer
4. Click "Next" through all the steps, keep default options
5. Click "Install" and wait for it to finish
6. Click "Finish"

**To verify it worked:**
- Open Command Prompt (press Windows key, type "cmd", press Enter)
- Type: `node --version`
- You should see something like: `v20.10.0`

---

### 1.2 Install Python

1. Go to: **https://www.python.org/downloads/**
2. Click "Download Python 3.x.x" (the big yellow button)
3. Run the installer
4. **IMPORTANT:** Check the box that says **"Add Python to PATH"** at the bottom!
5. Click "Install Now"
6. Wait for it to finish, click "Close"

**To verify it worked:**
- Open a NEW Command Prompt
- Type: `python --version`
- You should see something like: `Python 3.11.5`

---

### 1.3 Install Git

1. Go to: **https://git-scm.com/download/win**
2. The download should start automatically
3. Run the installer
4. Click "Next" through all steps (keep all default options)
5. Click "Install" and wait
6. Click "Finish"

**To verify it worked:**
- Open a NEW Command Prompt
- Type: `git --version`
- You should see something like: `git version 2.42.0`

---

## PART 2: GET AN ANTHROPIC API KEY

The app needs an API key to process natural language queries.

1. Go to: **https://console.anthropic.com/**
2. Click "Sign Up" and create an account (it's free)
3. Verify your email
4. Log in to your account
5. Click on **"API Keys"** in the left sidebar
6. Click **"Create Key"**
7. Give it a name like "OLAP Assistant"
8. **COPY THE KEY** - it starts with `sk-ant-...`
9. Save it somewhere safe (you'll need it later)

**IMPORTANT:** You only see the key once! If you lose it, you'll need to create a new one.

---

## PART 3: DOWNLOAD THE PROJECT

### 3.1 Open Command Prompt

1. Press the **Windows key** on your keyboard
2. Type **cmd**
3. Press **Enter**

### 3.2 Navigate to where you want the project

Type this and press Enter:
```
cd C:\Users\User
```

(Replace "User" with your actual Windows username if different)

### 3.3 Clone the repository

Type this and press Enter:
```
git clone https://github.com/emergent-agent-e1/olap-assistant.git
```

Wait for it to download (about 30 seconds).

### 3.4 Go into the project folder

```
cd olap-assistant
```

Then:
```
cd OLAP-Assistant
```

(Note: The folder might be named differently. Type `dir` to see what folders exist)

---

## PART 4: SETUP THE BACKEND

### 4.1 Go to backend folder

```
cd backend
```

### 4.2 Create a virtual environment

```
python -m venv venv
```

Wait about 30 seconds for it to finish.

### 4.3 Activate the virtual environment

```
venv\Scripts\activate
```

You should now see `(venv)` at the beginning of your command line.

### 4.4 Install Python packages

```
pip install -r requirements.txt
```

Wait for all packages to install (2-3 minutes).

Then install one more:
```
pip install anthropic
```

### 4.5 Create the .env file

```
notepad .env
```

Notepad will open. If it asks "Do you want to create a new file?" click **Yes**.

Type this content (replace YOUR_API_KEY with your actual Anthropic key):

```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="olap_assistant"
CORS_ORIGINS="*"
LLM_API_KEY=sk-ant-YOUR_API_KEY_HERE
```

**Example with a real key (yours will be different):**
```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="olap_assistant"
CORS_ORIGINS="*"
LLM_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Now save the file:
- Click **File** → **Save** (or press Ctrl+S)
- Close Notepad

### 4.6 Start the backend server

```
uvicorn server:app --reload --port 8001
```

You should see:
```
INFO:     Database initialized with 11000 records
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**KEEP THIS TERMINAL WINDOW OPEN!** The backend needs to keep running.

---

## PART 5: SETUP THE FRONTEND

### 5.1 Open a NEW Command Prompt

- Press **Windows key**
- Type **cmd**
- Press **Enter**

(Keep the backend terminal open!)

### 5.2 Go to frontend folder

```
cd C:\Users\User\olap-assistant\OLAP-Assistant\frontend
```

### 5.3 Install packages

```
npm install --legacy-peer-deps
```

Wait 2-3 minutes for it to finish. You'll see some warnings - that's normal.

### 5.4 Create the frontend .env file

```
notepad .env
```

If it asks to create a new file, click **Yes**.

Type this single line:
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

Save the file (Ctrl+S) and close Notepad.

### 5.5 Start the frontend

```
npm start
```

Wait about 30 seconds. Your browser should automatically open to **http://localhost:3000**

If it doesn't open automatically, open your browser and go to: **http://localhost:3000**

---

## PART 6: USING THE APP

### 6.1 You should see:
- Dashboard with **11,000 records**
- Total Sales around **$224 million**
- A query input box on the left

### 6.2 Try a query:
Type in the query box:
```
Show sales by region
```

Press **Enter** or click the send button.

You should see a chart with sales data for North, South, East, West, and Central regions!

### 6.3 More queries to try:
- `Break down Q4 sales by region`
- `Show total sales by category`
- `Compare North and South regions`
- `Drill into 2024 by quarter`

---

## PART 7: STOPPING AND RESTARTING

### To stop the app:
- Go to each terminal window
- Press **Ctrl+C**

### To restart later:

**Terminal 1 - Backend:**
```
cd C:\Users\User\olap-assistant\OLAP-Assistant\backend
venv\Scripts\activate
uvicorn server:app --reload --port 8001
```

**Terminal 2 - Frontend:**
```
cd C:\Users\User\olap-assistant\OLAP-Assistant\frontend
npm start
```

---

## TROUBLESHOOTING

### "python is not recognized"
- You didn't check "Add Python to PATH" during installation
- Reinstall Python and make sure to check that box

### "npm is not recognized"
- Node.js is not installed properly
- Reinstall Node.js from nodejs.org

### "Cannot find module" errors
- Run `npm install --legacy-peer-deps` again

### Backend shows "LLM API key not configured"
- Your .env file is missing or doesn't have the API key
- Make sure the .env file is in the `backend` folder
- Make sure it contains `LLM_API_KEY=sk-ant-your-key`

### Queries return errors
- Check that your Anthropic API key is valid
- Check the backend terminal for error messages

### Port already in use
- Another program is using port 8001 or 3000
- Close other applications or restart your computer

### Frontend shows "Network Error"
- The backend is not running
- Make sure the backend terminal shows "Application startup complete"

---

## QUICK REFERENCE

| What | URL |
|------|-----|
| Frontend (UI) | http://localhost:3000 |
| Backend API | http://localhost:8001/api |
| API Documentation | http://localhost:8001/api/docs |

---

## NEED HELP?

If you're stuck:
1. Read the error message carefully
2. Check the troubleshooting section above
3. Make sure both terminals (backend AND frontend) are running
4. Try restarting both services

---

## CHECKLIST BEFORE DEMO

- [ ] Backend terminal shows "11000 records" and "startup complete"
- [ ] Frontend opens in browser at localhost:3000
- [ ] Dashboard shows 11,000 records and ~$224M sales
- [ ] Query "Show sales by region" returns results with chart
- [ ] Charts work (Bar, Pie, Line, Area)
- [ ] Compare feature works
- [ ] Export to PDF works
