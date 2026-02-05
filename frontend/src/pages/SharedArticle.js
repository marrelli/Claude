import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FiArrowLeft, FiExternalLink } from 'react-icons/fi';
import { sharingAPI } from '../services/api';

function SharedArticle() {
  const { token } = useParams();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSharedArticle();
  }, [token]);

  const loadSharedArticle = async () => {
    try {
      setLoading(true);
      const data = await sharingAPI.getSharedArticle(token);
      setArticle(data.article);
    } catch (err) {
      setError('Article not found or share has expired');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="container">
        <div style={{ paddingTop: '3rem', textAlign: 'center' }}>
          <div className="spinner"></div>
          <p style={{ marginTop: '1rem', color: '#7f8c8d' }}>Loading article...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div style={{ paddingTop: '3rem', textAlign: 'center' }}>
          <h2 style={{ color: '#e74c3c' }}>Error</h2>
          <p style={{ color: '#7f8c8d', marginBottom: '2rem' }}>{error}</p>
          <Link to="/" className="btn btn-primary">
            <FiArrowLeft /> Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ maxWidth: '800px', margin: '0 auto', paddingTop: '2rem' }}>
        <Link to="/" className="btn btn-outline btn-sm" style={{ marginBottom: '2rem' }}>
          <FiArrowLeft /> Back to Dashboard
        </Link>

        <article className="card" style={{ marginBottom: '2rem' }}>
          <div className="card-header">
            <h1>{article.title}</h1>
          </div>

          <div className="article-meta" style={{ marginBottom: '2rem' }}>
            {article.source_count > 1 && (
              <span className="article-source-badge">{article.source_count} sources</span>
            )}
            <span>{formatDate(article.fetched_at)}</span>
            <span>Priority: {article.priority_score.toFixed(2)}</span>
          </div>

          {article.domains && article.domains.length > 0 && (
            <div style={{ marginBottom: '1.5rem' }}>
              {article.domains.map((domain) => (
                <span key={domain.id} className="article-source-badge" style={{ backgroundColor: '#1a7f7e' }}>
                  {domain.name}
                </span>
              ))}
            </div>
          )}

          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ color: '#8b3a3a', marginBottom: '1rem' }}>Summary</h3>
            <div className="article-summary">{article.summary || 'No summary available'}</div>
          </div>

          {article.content && (
            <div style={{ marginBottom: '2rem' }}>
              <h3 style={{ color: '#8b3a3a', marginBottom: '1rem' }}>Full Content</h3>
              <div style={{ color: '#7f8c8d', lineHeight: '1.8' }}>{article.content}</div>
            </div>
          )}

          {article.contradictions && article.contradictions.length > 0 && (
            <div style={{
              backgroundColor: '#fff3cd',
              border: '2px solid #ffc107',
              padding: '1.5rem',
              borderRadius: '8px',
              marginBottom: '2rem'
            }}>
              <h3 style={{ color: '#856404', marginBottom: '1rem' }}>⚠ Contradictions Found</h3>
              <ul>
                {article.contradictions.map((contradiction, idx) => (
                  <li key={idx} style={{ marginBottom: '1rem', color: '#856404', lineHeight: '1.6' }}>
                    {contradiction.conflict_description}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <a
            href={article.original_url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary"
          >
            <FiExternalLink /> Read Full Article
          </a>
        </article>

        <div style={{ textAlign: 'center', color: '#7f8c8d', marginBottom: '2rem' }}>
          <p style={{ fontSize: '0.875rem' }}>
            Curated with ❤️ by Daily Curator
          </p>
        </div>
      </div>
    </div>
  );
}

export default SharedArticle;
