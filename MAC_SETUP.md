# macOS Setup Guide

Complete walkthrough for running Daily Curator on Mac.

## Prerequisites on Mac

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install PostgreSQL via Homebrew
```bash
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Verify it's running
brew services list
```

### 3. Create Database and User
```bash
# Connect to PostgreSQL
psql postgres

# In the PostgreSQL prompt, run:
CREATE USER daily_curator WITH PASSWORD 'your_password_here';
CREATE DATABASE daily_news_db OWNER daily_curator;
ALTER ROLE daily_curator CREATEDB;
\q

# Test connection
psql -U daily_curator -d daily_news_db -h localhost
\q
```

### 4. Install Python 3.10+ (if needed)
```bash
# Check current Python version
python3 --version

# If you need a specific version, use Homebrew
brew install python@3.11

# Verify
python3.11 --version

# You can also use pyenv for multiple Python versions:
brew install pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

### 5. Install Node.js
```bash
brew install node

# Verify
node --version
npm --version
```

## Setup Instructions

### Terminal Setup (Do This First)

```bash
# Open Terminal and navigate to the project
cd /path/to/Claude

# Create a .env file for shell variables (optional but helpful)
cat > backend/.env << EOF
DATABASE_URL=postgresql://daily_curator:your_password_here@localhost:5432/daily_news_db
ANTHROPIC_API_KEY=sk-ant-your_key_here
NEWS_API_KEY=your_news_api_key_here
DEBUG=False
EOF
```

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.core.database import init_db; init_db()"

# Start backend server
uvicorn app.main:app --reload
```

✅ Backend running at http://localhost:8000

### 2. Frontend Setup (New Terminal Window)

```bash
# Open a new Terminal tab/window
# Navigate to project
cd /path/to/Claude/frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start frontend
npm start
```

✅ Frontend running at http://localhost:3000

## Common Mac Issues & Fixes

### "PostgreSQL command not found"
```bash
# If brew services says it's running but psql doesn't work:
echo 'export PATH="/usr/local/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Then try again
psql -U daily_curator -d daily_news_db
```

### "Port 3000 already in use"
```bash
# Find what's using port 3000
lsof -i :3000

# Kill process (replace PID with the number shown)
kill -9 <PID>

# Or just use different port
npm start -- --port 3001
```

### "Port 8000 already in use"
```bash
# Find what's using port 8000
lsof -i :8000

# Kill it or run on different port
uvicorn app.main:app --reload --port 8001
```

### "ModuleNotFoundError: No module named 'app'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# If already activated, try installing again
pip install -r requirements.txt
```

### "psycopg2 build failed"
```bash
# Common Mac issue - install build tools first
xcode-select --install

# Then reinstall requirements
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

### "Connection refused to PostgreSQL"
```bash
# Verify PostgreSQL is running
brew services list

# If not running, start it
brew services start postgresql@15

# Check connection string in .env matches:
# postgresql://daily_curator:your_password@localhost:5432/daily_news_db
```

## Useful Mac Commands

### Manage PostgreSQL
```bash
# Start/stop PostgreSQL
brew services start postgresql@15
brew services stop postgresql@15

# Check status
brew services list

# Connect to database
psql -U daily_curator -d daily_news_db

# View databases
psql postgres -c "SELECT datname FROM pg_database;"
```

### Manage Virtual Environment
```bash
# Activate venv
source backend/venv/bin/activate

# Deactivate venv
deactivate

# Remove venv to start fresh
rm -rf backend/venv
```

### Kill Stuck Processes
```bash
# Find process on port
lsof -i :8000
lsof -i :3000

# Kill it
kill -9 <PID>
```

### View API Docs
Open browser to: http://localhost:8000/docs

## Quick Restart

Once everything is installed, for future sessions:

**Terminal 1 (Backend):**
```bash
cd /path/to/Claude/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd /path/to/Claude/frontend
npm start
```

**Open browser:** http://localhost:3000

## Mac-Specific Tips

1. **Use iTerm2** instead of Terminal for better workflow (optional)
2. **Use VS Code** for editing - works great with Python/React debugging
3. **Keep PostgreSQL in Services**: Won't stop on restart with `brew services`
4. **Python Versions**: If issues, try `python3.11` explicitly instead of `python3`
5. **npm issues**: If stuck, try `npm cache clean --force`

## Performance Notes

- M1/M2 Macs: Everything runs great, use arm64 compatible packages
- Intel Macs: Make sure Homebrew is installed for x86_64 compatibility
- 8GB+ RAM recommended for comfortable local development

## Next Steps

1. Visit http://localhost:3000
2. Click "Fetch Now" to populate articles
3. Add your topics
4. Suggest new sources
5. Enjoy your curated news!

## Getting Help

Check these if something fails:

1. Backend logs in terminal (look for red errors)
2. Browser console (F12 → Console tab)
3. PostgreSQL connection with: `psql -U daily_curator -d daily_news_db`
4. API docs at http://localhost:8000/docs for testing endpoints

Happy curating! 🎨📚
