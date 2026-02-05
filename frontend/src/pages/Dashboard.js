import React, { useState, useEffect } from 'react';
import ArticleItem from '../components/ArticleItem';
import Sidebar from '../components/Sidebar';
import { articlesAPI } from '../services/api';

function Dashboard() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDomain, setSelectedDomain] = useState(null);
  const [fetchingNow, setFetchingNow] = useState(false);
  const [fetchResult, setFetchResult] = useState(null);
  const [limit] = useState(20);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadArticles();
  }, [selectedDomain, offset]);

  const loadArticles = async () => {
    try {
      setLoading(true);
      const data = await articlesAPI.getFeed(selectedDomain, limit, offset);
      setArticles(data.articles);
      setTotal(data.total);
    } catch (err) {
      setError('Failed to load articles');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchNow = async () => {
    try {
      setFetchingNow(true);
      setError(null);
      const result = await articlesAPI.fetchNow();
      setFetchResult(result);

      // Reload articles
      await loadArticles();

      // Clear result after 3 seconds
      setTimeout(() => setFetchResult(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch articles');
    } finally {
      setFetchingNow(false);
    }
  };

  const handleDomainChange = (domainId) => {
    setSelectedDomain(domainId);
    setOffset(0);
  };

  const handleFeedback = async (articleId, feedbackType) => {
    // Refetch to update priority scores
    await loadArticles();
  };

  const handleShare = (articleId, link) => {
    // Show success notification
    console.log('Share created:', link);
  };

  return (
    <div className="container">
      <div className="main-layout">
        <div className="feed-container">
          {error && (
            <div className="notification notification-error" style={{ margin: '1rem' }}>
              {error}
            </div>
          )}

          {fetchResult && (
            <div className="notification notification-success" style={{ margin: '1rem' }}>
              Found {fetchResult.articles_found} articles, added {fetchResult.articles_added} new items
            </div>
          )}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Loading articles...</p>
            </div>
          )}

          {!loading && articles.length === 0 && (
            <div
              style={{
                padding: '3rem',
                textAlign: 'center',
                color: '#7f8c8d'
              }}
            >
              <p style={{ fontSize: '1.125rem', marginBottom: '1rem' }}>
                No articles found yet
              </p>
              <p style={{ fontSize: '0.875rem' }}>
                Click "Fetch Now" to retrieve the latest articles
              </p>
            </div>
          )}

          {!loading &&
            articles.map((article) => (
              <ArticleItem
                key={article.id}
                article={article}
                onFeedback={handleFeedback}
                onShare={handleShare}
              />
            ))}

          {!loading && articles.length > 0 && (
            <div
              style={{
                padding: '1rem',
                textAlign: 'center',
                borderTop: '1px solid #bdc3c7',
                color: '#7f8c8d'
              }}
            >
              <p style={{ fontSize: '0.875rem' }}>
                Showing {offset + 1}-{Math.min(offset + limit, total)} of {total} articles
              </p>
              <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                <button
                  onClick={() => setOffset(Math.max(0, offset - limit))}
                  disabled={offset === 0}
                  className="btn btn-sm btn-outline"
                >
                  Previous
                </button>
                <button
                  onClick={() => setOffset(offset + limit)}
                  disabled={offset + limit >= total}
                  className="btn btn-sm btn-outline"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>

        <Sidebar
          onFetchNow={handleFetchNow}
          onDomainChange={handleDomainChange}
          loading={fetchingNow}
        />
      </div>
    </div>
  );
}

export default Dashboard;
