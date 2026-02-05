# Quick Start Guide

Get Daily Curator running in under 20 minutes.

> **Are you on Mac?** 👉 See [MAC_SETUP.md](MAC_SETUP.md) — it has detailed step-by-step instructions including installing everything you need.
>
> **Windows/Linux?** 👉 Follow this guide, but install PostgreSQL using your system's package manager first.

---

## What You Need Before Starting

1. **Two free API keys** (takes 5 minutes):
   - [Anthropic API Key](https://console.anthropic.com) — for article summaries
   - [NewsAPI Key](https://newsapi.org) — for news articles

2. **Three things installed on your computer**:
   - Python 3.10 or newer
   - Node.js 16 or newer
   - PostgreSQL 12 or newer

**Mac user?** Go to [MAC_SETUP.md](MAC_SETUP.md) — it walks you through installing all of these.

---

## If You Already Have Everything Installed

### Step 1: Get Your API Keys

**Get Anthropic Key:**
1. Visit https://console.anthropic.com
2. Sign up or log in
3. Click "API Keys"
4. Click "Create Key"
5. Copy and save the key

**Get NewsAPI Key:**
1. Visit https://newsapi.org
2. Sign up (free)
3. Verify your email
4. Copy your API key

Keep these keys handy.

---

### Step 2: Backend Setup

Open Terminal and run these commands one at a time:

```bash
cd backend
```

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
cp .env.example .env
```

Now edit the `.env` file. Open it with:

```bash
nano .env
```

Change it to (replace the `YOUR_KEY_HERE` parts with your actual keys):

```
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/daily_news_db
ANTHROPIC_API_KEY=sk-ant-YOUR_ANTHROPIC_KEY_HERE
NEWS_API_KEY=YOUR_NEWSAPI_KEY_HERE
DEBUG=False
```

Save by pressing `Control+X`, then `y`, then `Enter`.

Initialize database:

```bash
python -c "from app.core.database import init_db; init_db()"
```

Start backend:

```bash
uvicorn app.main:app --reload
```

✅ You should see: `Uvicorn running on http://127.0.0.1:8000`

Keep this Terminal window open.

---

### Step 3: Frontend Setup

Open a **NEW Terminal window** and run:

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

✅ Your browser should open automatically at http://localhost:3000

---

## Using the App

1. **Click "Fetch Now"** in the sidebar
2. **Wait** 30-60 seconds (it's fetching and summarizing articles)
3. **Articles appear** in the feed
4. **Click articles to expand** and read full content
5. **Add topics** using the "Domains" panel
6. **Suggest sources** using the "Sources" panel
7. **Use buttons**: Heart articles, mark as helpful, share with others

---

## Troubleshooting

### PostgreSQL not running
```bash
# Mac users:
brew services start postgresql@15

# Others: see your PostgreSQL installation docs
```

### "ModuleNotFoundError"
Make sure `(venv)` shows at the start of your Terminal line. If not:
```bash
source venv/bin/activate
```

### "Port 3000/8000 already in use"
Find and kill the process:
```bash
lsof -i :3000        # for port 3000
lsof -i :8000        # for port 8000
kill -9 <PID>        # replace PID with the number shown
```

### No articles appearing
1. Verify your API keys are correct in `backend/.env`
2. Click "Fetch Now" and wait 30-60 seconds
3. Check browser console (F12) for errors

---

## Next Time You Run the App

**Terminal 1:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2:**
```bash
cd frontend
npm start
```

---

## Need Help?

See [MAC_SETUP.md](MAC_SETUP.md) for detailed troubleshooting and explanations.

Full documentation: [README.md](README.md)

**Happy curating! 🎨📚**
