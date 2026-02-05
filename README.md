# Daily Curator - Daily News Curation App

A modern, clean web application that helps you stay informed with curated news, articles, and topics relevant to your work and interests. Built with a Renaissance-inspired aesthetic and powered by AI-generated summaries and contradiction detection.

## Features

✨ **Core Features**
- 📰 Curated news dashboard with AI-generated summaries
- 🎯 Multiple domains/topics configuration (Technology, AI, Future of Work, etc.)
- 🔄 Scheduled fetching (5am and 5pm Eastern Time)
- 🚀 On-demand fetch for manual updates
- 💎 Favorite/heart articles
- 📤 Shareable links for articles
- 👍 Thumbs up/down feedback system
- 🌐 Multiple source management
- 💡 Source suggestions from users
- ⚠️ Contradiction detection across sources
- 🎨 Modern, clean UI with Renaissance design elements

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI**: Anthropic Claude API
- **Scheduling**: APScheduler
- **Data Fetching**: NewsAPI, RSS feeds, custom sources

### Frontend
- **Framework**: React 18
- **Styling**: Modern CSS with Renaissance aesthetic
- **HTTP Client**: Axios
- **Routing**: React Router v6

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── core/          # Configuration & database
│   │   ├── models.py      # SQLAlchemy models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── main.py        # FastAPI application
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   ├── styles/        # CSS styling
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   └── .env.example
│
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL 12+
- API Keys:
  - Anthropic API Key (for Claude)
  - NewsAPI Key (for news articles)
  - (Optional) Twitter API credentials

### Backend Setup

1. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/daily_news_db
   ANTHROPIC_API_KEY=sk-ant-...
   NEWS_API_KEY=your_news_api_key_here
   DEBUG=False
   ```

5. **Initialize database**
   ```bash
   python -c "from app.core.database import init_db; init_db()"
   ```

6. **Run backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Run development server**
   ```bash
   npm start
   ```
   Frontend will be available at `http://localhost:3000`

## Usage

### Dashboard
- **Main Feed**: Displays articles prioritized by source count, domain relevance, and engagement
- **Fetch Now**: Manually trigger article fetching from all sources
- **Article Actions**:
  - ❤️ **Love**: Heart your favorite articles
  - 👍 **Helpful**: Mark articles as helpful
  - 👎 **Skip**: Provide negative feedback (helps auto-remove poor sources)
  - 📤 **Share**: Generate shareable link
  - 📖 **Details**: Expand for full content and contradiction detection

### Domain Management
- **Add Topics**: Create custom domains for news curation
- **Keywords**: Add keywords for matching articles
- **Manage**: Remove domains you're no longer interested in

### Source Management
- **Active Sources**: View and manage active news sources
- **Suggest New Sources**: Submit new sources for curation
  - Name, URL, and optional description
  - Pending suggestions can be reviewed and approved
- **Quality Tracking**: Sources with multiple thumbs-down are automatically removed

### Sharing
- Generate unique shareable links for articles
- Share with colleagues or friends
- Public viewing (no authentication required)

## API Endpoints

### Articles
- `GET /articles/feed?domain_id=X&limit=20&offset=0` - Get prioritized feed
- `POST /articles/feedback/{id}` - Add feedback (heart/thumbs_up/thumbs_down)
- `GET /articles/{id}` - Get article details
- `POST /articles/fetch-now` - Trigger manual fetch

### Domains
- `GET /domains` - List all domains
- `POST /domains` - Create new domain
- `PUT /domains/{id}` - Update domain
- `DELETE /domains/{id}` - Delete domain

### Sources
- `GET /sources` - List sources and suggestions
- `POST /sources` - Create new source
- `DELETE /sources/{id}` - Delete source
- `POST /sources/suggest` - Suggest new source
- `POST /sources/suggestions/{id}/approve` - Approve suggestion
- `POST /sources/suggestions/{id}/reject` - Reject suggestion

### Sharing
- `POST /share/{article_id}` - Create share link
- `GET /share/{token}` - Get shared article (public)
- `DELETE /share/{id}` - Delete share link

## Design Philosophy

### Knowledge-First Curation
The app emphasizes continuous learning and intellectual growth, actively filtering out gossip and low-value content through AI quality assessment.

### Renaissance Aesthetic
The design includes:
- Serif typography (Georgia) for headings
- Warm color palette: burgundy, gold, teal, cream
- Subtle shadows and refined spacing
- Clean, organized layout inspired by classical design

### Prioritization Algorithm
```
priority_score = (
    source_count * 0.4 +           # Consensus across sources
    domain_relevance * 0.3 +        # Matches your interests
    freshness_factor * 0.2 +        # Recency
    engagement_score * 0.1          # Your feedback
)
```

## Scheduled Operations

### Automatic Fetching
- **5am ET**: Morning briefing fetch
- **5pm ET**: Evening update fetch

### Automatic Cleanup
- Articles older than 30 days are removed
- Sources with 5+ thumbs-down become inactive

## Development

### Adding New Features

1. **Backend**: Add routes in `app/api/`, update services, and models
2. **Frontend**: Create components in `src/components/` or pages in `src/pages/`
3. **API Client**: Update `src/services/api.js`
4. **Styling**: Extend `src/styles/App.css` using CSS variables

### Database Migrations

For schema changes:
1. Modify models in `app/models.py`
2. Recreate database: `python -c "from app.core.database import init_db; init_db()"`

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env`
- Verify user/password credentials

### API Key Errors
- Verify ANTHROPIC_API_KEY and NEWS_API_KEY in `.env`
- Check key validity on provider websites

### Frontend Not Connecting
- Ensure backend is running on localhost:8000
- Check REACT_APP_API_URL in frontend `.env`
- Check browser console for CORS errors

### No Articles Appearing
- Run "Fetch Now" manually
- Check NEWS_API_KEY validity
- Review backend logs for fetch errors

## Future Enhancements

- 🔐 User authentication and accounts
- 📧 Email digest summaries
- 📱 Mobile app
- 🤖 Advanced NLP for better contradiction detection
- 🔔 Real-time notifications
- 📊 Analytics dashboard
- 🌍 Multi-language support
- 🎨 Customizable themes

## Contributing

This is a personal project. Feel free to fork and customize for your needs!

## License

MIT

## Contact & Support

For issues or questions, please check the repository or refer to the documentation above.

---

**Made with ❤️ for continuous learning and intellectual growth**
