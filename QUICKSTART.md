# Quick Start Guide

Get the Daily Curator app running in minutes!

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 16+ installed
- [ ] PostgreSQL 12+ installed and running
- [ ] Anthropic API Key (get at https://console.anthropic.com)
- [ ] NewsAPI Key (free tier at https://newsapi.org)

## Step-by-Step Setup

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your keys:
# ANTHROPIC_API_KEY=your_key_here
# NEWS_API_KEY=your_key_here
# DATABASE_URL=postgresql://user:password@localhost:5432/daily_news_db
```

**Start the backend:**
```bash
uvicorn app.main:app --reload
```
✅ Backend running at http://localhost:8000

### 2. Frontend Setup (3 minutes)

```bash
# In another terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start the app
npm start
```
✅ Frontend running at http://localhost:3000

## First Steps

1. **Visit Dashboard**: Open http://localhost:3000
2. **Click "Fetch Now"**: Manually trigger article fetching
3. **Add Topics**: Click "Domains" panel to customize your interests
4. **Suggest Sources**: Add your preferred news sources
5. **Read Articles**: Expand articles to see full content and summaries
6. **Provide Feedback**: Use heart, helpful, or skip buttons

## Common Issues

### Backend won't start
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Try rebuilding database:
python -c "from app.core.database import init_db; init_db()"
```

### No articles appearing
- Verify NEWS_API_KEY is valid
- Check API quota hasn't been exceeded
- Try clicking "Fetch Now"

### Frontend can't reach backend
- Ensure backend is running on port 8000
- Check REACT_APP_API_URL in frontend/.env
- Check browser console for CORS errors

## What's Next?

- ✅ Default domains are auto-created
- ✅ Default sources are initialized
- ✅ Scheduler will fetch at 5am and 5pm ET daily
- 🔄 Articles auto-prioritize based on relevance
- 🤖 Summaries generated via Claude AI

## Default Domains

The app comes with 5 default topics:
- Technology Industry
- Artificial Intelligence
- Future of Work
- Entertainment and Media Industry
- Data Management

Add/remove topics in the sidebar!

## API Documentation

Full API docs available at: http://localhost:8000/docs

## Learn More

See [README.md](README.md) for comprehensive documentation, feature details, and deployment instructions.

Happy curating! 🎨📚
