# macOS Setup Guide for Beginners

Complete step-by-step walkthrough. No experience needed! **Total time: ~20 minutes**

---

## What You'll Need First

### 1. Get Your API Keys (5 minutes)

You need two free API keys. Don't worry — this is just copy/paste.

**Anthropic (Claude) API Key:**
1. Go to https://console.anthropic.com
2. Sign in or create account
3. Click "API Keys" on left menu
4. Click "Create Key" button
5. Copy the key (looks like: `sk-ant-abc123...`)
6. Save it somewhere safe (notepad, email, etc.)

**NewsAPI Key:**
1. Go to https://newsapi.org
2. Sign up for free
3. Verify your email
4. Go to "API Keys" dashboard
5. Copy your key
6. Save it somewhere

Keep these keys handy — you'll paste them later.

---

## Step 1: Open Terminal

This is where you'll type commands.

1. Press **Command (⌘) + Space** on your keyboard
2. Type `terminal`
3. Press Enter
4. A window opens — this is Terminal

**Tip:** You can resize and keep Terminal open on the side.

---

## Step 2: Install Homebrew

Homebrew is a tool that installs software for you. Copy and paste this **entire command** into Terminal, then press Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Wait for it to finish (takes 2-5 minutes). You'll see text scrolling.

**Expected output:** "Installation successful!" at the end

---

## Step 3: Install PostgreSQL (Database)

This stores all your articles and preferences.

Copy and paste this into Terminal and press Enter:

```bash
brew install postgresql@15
```

Wait for it to complete.

Then, copy and paste this and press Enter:

```bash
brew services start postgresql@15
```

**What this does:** Starts the database in the background automatically.

---

## Step 4: Create Your Database

Copy and paste this entire block into Terminal and press Enter:

```bash
psql postgres
```

This opens the database prompt. You'll see: `postgres=#`

Now copy and paste each of these commands one at a time, pressing Enter after each:

```sql
CREATE USER daily_curator WITH PASSWORD 'curator123';
CREATE DATABASE daily_news_db OWNER daily_curator;
ALTER ROLE daily_curator CREATEDB;
\q
```

**What each line does:**
- Line 1: Creates a user (username: `daily_curator`, password: `curator123`)
- Line 2: Creates the database
- Line 3: Gives the user permission
- Line 4: Exits the database

You should be back at the regular Terminal prompt (looks like: `YourName@MacBook ~ %`)

---

## Step 5: Install Python & Node.js

Copy and paste each command separately, pressing Enter after each:

```bash
brew install python@3.11
```

Wait for it to finish, then:

```bash
brew install node
```

Wait for it to finish.

**Verify they installed:** Copy and paste each of these:

```bash
python3.11 --version
node --version
```

You should see version numbers appear (like `Python 3.11.0` and `v18.x.x`).

---

## Step 6: Download the Project

If you haven't already, download/clone the project.

**In Terminal**, go to where you want to save it:

```bash
cd ~/Documents
```

Then download the project (ask whoever gave you this if you need the clone command).

Once you have the folder, navigate into it:

```bash
cd Claude
```

You should be in the project folder now.

---

## Step 7: Backend Setup

This is the "brain" of the app.

**Copy and paste each command one at a time:**

```bash
cd backend
```

This takes you to the backend folder.

```bash
python3.11 -m venv venv
```

This creates an isolated environment for the backend (prevents conflicts with other projects).

```bash
source venv/bin/activate
```

This activates the environment. You should see `(venv)` appear at the start of your Terminal line.

```bash
pip install -r requirements.txt
```

This installs all the code dependencies. Takes 2-3 minutes. Lots of text will scroll.

Now, create the settings file:

```bash
cp .env.example .env
```

Now, edit the file to add your API keys. Use this command:

```bash
nano .env
```

A text editor opens. You'll see:

```
DATABASE_URL=postgresql://user:password@localhost:5432/daily_news_db
ANTHROPIC_API_KEY=sk-ant-...
NEWS_API_KEY=your_news_api_key_here
DEBUG=False
```

**Edit it to look like this** (replace the examples with your real keys):

```
DATABASE_URL=postgresql://daily_curator:curator123@localhost:5432/daily_news_db
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
NEWS_API_KEY=YOUR_KEY_HERE
DEBUG=False
```

To save:
1. Press **Control + X** (not Command)
2. Type `y` and press Enter
3. Press Enter again

Now, create the database tables:

```bash
python -c "from app.core.database import init_db; init_db()"
```

This sets up the database. You should see no errors (or just a brief message).

**Start the backend:**

```bash
uvicorn app.main:app --reload
```

Wait for text that says: `Uvicorn running on http://127.0.0.1:8000`

✅ **Backend is running!** Keep this Terminal window open.

---

## Step 8: Frontend Setup

**Open a NEW Terminal window** (Command + T or Command + N).

Copy and paste each command:

```bash
cd ~/Documents/Claude/frontend
```

(or wherever you saved the project)

```bash
npm install
```

Wait for this to complete (takes 1-2 minutes).

Create settings file:

```bash
cp .env.example .env
```

Start the app:

```bash
npm start
```

Wait for text that says: `Compiled successfully!` and `On Your Network: http://...`

✅ **Frontend is running!** A browser window should open automatically.

---

## Step 9: Use the App!

The app should now be running in your browser at http://localhost:3000

1. **Click "Fetch Now"** - Gets articles from the news
2. **Wait** - Takes 30-60 seconds to fetch and summarize
3. **Articles appear** - You'll see news items
4. **Add Topics** - Click the "Domains" sidebar to add topics you care about
5. **Click articles** - Expand them to read full summaries
6. **Like/Share** - Use the buttons to heart articles or share them

---

## Troubleshooting

### "Command not found: psql"

This means Terminal can't find PostgreSQL even though it's installed.

**First, check which shell you're using:**

```bash
echo $SHELL
```

**If it says `/bin/zsh`** (newer Macs), copy and paste this:

```bash
echo 'export PATH="/usr/local/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**If it says `/bin/bash`** (older Macs), copy and paste this instead:

```bash
echo 'export PATH="/usr/local/opt/postgresql@15/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

Then close Terminal completely and open a new Terminal window. Try again:

```bash
psql postgres
```

**If neither works**, try this direct path instead:

```bash
/usr/local/opt/postgresql@15/bin/psql postgres
```

If this works, PostgreSQL is installed correctly — you just need the PATH fix above.

### "Port 3000 already in use"

Another app is using that port. Copy and paste:

```bash
lsof -i :3000
```

Find the number in the PID column, then copy and paste (replacing 12345 with that number):

```bash
kill -9 12345
```

Then try `npm start` again.

### "Port 8000 already in use"

Same fix as above, but use `:8000`:

```bash
lsof -i :8000
kill -9 <PID>
```

### "ModuleNotFoundError" or errors about missing modules

Make sure `(venv)` shows at the start of your Terminal line. If not:

```bash
source venv/bin/activate
```

Then try the backend command again.

### "No articles appearing"

1. Click "Fetch Now" in the app
2. Wait 30-60 seconds
3. Check that your NEWS_API_KEY is correct in `backend/.env`

### "Backend won't start"

1. Check PostgreSQL is running:
   ```bash
   brew services list
   ```
   PostgreSQL should show "started"

2. If not running, start it:
   ```bash
   brew services start postgresql@15
   ```

3. Check your DATABASE_URL is correct in `backend/.env` — it should be:
   ```
   postgresql://daily_curator:curator123@localhost:5432/daily_news_db
   ```

---

## Everyday Use (Next Time)

To run the app again later:

**Terminal 1 (Backend):**
```bash
cd ~/Documents/Claude/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Wait for "Uvicorn running..." message.

**Terminal 2 (Frontend):**
```bash
cd ~/Documents/Claude/frontend
npm start
```

Wait for browser to open.

**That's it!** The app is ready.

---

## Stopping the App

When you're done:
- Press **Control + C** in each Terminal window to stop
- Close Terminal windows

The next time you want to use it, follow "Everyday Use" section above.

---

## Need Help?

If something doesn't work:

1. **Read the error message carefully** - it often says exactly what's wrong
2. **Check the Troubleshooting section above** - fixes most common problems
3. **Try restarting** - close Terminal and start fresh
4. **Check your API keys** - make sure you copied them correctly

---

**Happy curating! 🎨📚**

Questions? Contact the person who gave you this app.
