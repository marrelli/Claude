import React, { useState } from 'react';
import { FiHeart, FiThumbsUp, FiThumbsDown, FiShare2, FiExternalLink, FiChevronDown, FiChevronUp } from 'react-icons/fi';
import { articlesAPI, sharingAPI } from '../services/api';

function ArticleItem({ article, onFeedback, onShare }) {
  const [expanded, setExpanded] = useState(false);
  const [shareLink, setShareLink] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFeedback = async (feedbackType) => {
    try {
      await articlesAPI.addFeedback(article.id, feedbackType);
      onFeedback && onFeedback(article.id, feedbackType);
    } catch (err) {
      setError('Failed to add feedback');
    }
  };

  const handleShare = async () => {
    try {
      setLoading(true);
      const share = await sharingAPI.createShare(article.id);
      const link = `${window.location.origin}/share/${share.unique_token}`;
      setShareLink(link);
      onShare && onShare(article.id, link);
    } catch (err) {
      setError('Failed to create share link');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyLink = () => {
    if (shareLink) {
      navigator.clipboard.writeText(shareLink);
      alert('Link copied to clipboard!');
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

  return (
    <div className="article-item">
      {error && <div className="notification notification-error">{error}</div>}

      <div onClick={() => setExpanded(!expanded)} style={{ cursor: 'pointer' }}>
        <h3 className="article-title">{article.title}</h3>

        <div className="article-meta">
          <span>
            {article.source_count > 1 && (
              <span className="article-source-badge">{article.source_count} sources</span>
            )}
          </span>
          <span>{formatDate(article.fetched_at)}</span>
          <span>Priority: {article.priority_score.toFixed(2)}</span>
        </div>

        {article.domains && article.domains.length > 0 && (
          <div style={{ marginTop: '0.5rem', marginBottom: '0.5rem' }}>
            {article.domains.map((domain) => (
              <span key={domain.id} className="article-source-badge" style={{ backgroundColor: '#1a7f7e' }}>
                {domain.name}
              </span>
            ))}
          </div>
        )}

        <div className="article-summary">{article.summary || 'No summary available'}</div>
      </div>

      {expanded && (
        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #bdc3c7' }}>
          <div style={{ marginBottom: '1rem', color: '#7f8c8d', lineHeight: '1.8' }}>
            {article.content}
          </div>

          {article.contradictions && article.contradictions.length > 0 && (
            <div style={{
              backgroundColor: '#fff3cd',
              border: '1px solid #ffc107',
              padding: '1rem',
              borderRadius: '4px',
              marginBottom: '1rem'
            }}>
              <strong style={{ color: '#856404' }}>⚠ Contradictions Found:</strong>
              <ul style={{ marginTop: '0.5rem' }}>
                {article.contradictions.map((contradiction, idx) => (
                  <li key={idx} style={{ marginBottom: '0.5rem', color: '#856404' }}>
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
            className="btn btn-sm btn-secondary"
            style={{ marginBottom: '1rem' }}
          >
            <FiExternalLink /> View Original Article
          </a>
        </div>
      )}

      <div className="article-actions">
        <button
          onClick={() => setExpanded(!expanded)}
          className="btn btn-sm"
          style={{
            background: 'transparent',
            border: '1px solid #bdc3c7',
            color: '#2c3e50',
            padding: '0.25rem 0.5rem'
          }}
        >
          {expanded ? <FiChevronUp /> : <FiChevronDown />}
          {expanded ? 'Less' : 'More'}
        </button>

        <button
          onClick={() => handleFeedback('heart')}
          className="btn btn-sm"
          style={{
            background: 'transparent',
            border: '1px solid #bdc3c7',
            color: '#e74c3c',
            padding: '0.25rem 0.5rem'
          }}
          title="Love this article"
        >
          <FiHeart /> Love
        </button>

        <button
          onClick={() => handleFeedback('thumbs_up')}
          className="btn btn-sm"
          style={{
            background: 'transparent',
            border: '1px solid #bdc3c7',
            color: '#27ae60',
            padding: '0.25rem 0.5rem'
          }}
          title="Helpful"
        >
          <FiThumbsUp /> Helpful
        </button>

        <button
          onClick={() => handleFeedback('thumbs_down')}
          className="btn btn-sm"
          style={{
            background: 'transparent',
            border: '1px solid #bdc3c7',
            color: '#f39c12',
            padding: '0.25rem 0.5rem'
          }}
          title="Not helpful"
        >
          <FiThumbsDown /> Skip
        </button>

        <button
          onClick={handleShare}
          className="btn btn-sm"
          disabled={loading}
          style={{
            background: 'transparent',
            border: '1px solid #bdc3c7',
            color: '#1a7f7e',
            padding: '0.25rem 0.5rem'
          }}
          title="Share this article"
        >
          <FiShare2 /> {loading ? 'Sharing...' : 'Share'}
        </button>

        {shareLink && (
          <button
            onClick={handleCopyLink}
            className="btn btn-sm"
            style={{
              background: '#d4af37',
              border: '1px solid #d4af37',
              color: '#2c3e50',
              padding: '0.25rem 0.5rem'
            }}
            title="Copy share link"
          >
            Copy Link
          </button>
        )}
      </div>

      {shareLink && (
        <div style={{
          marginTop: '0.5rem',
          padding: '0.5rem',
          backgroundColor: '#ecf0f1',
          borderRadius: '4px',
          fontSize: '0.875rem',
          wordBreak: 'break-all'
        }}>
          <strong>Share link:</strong> {shareLink}
        </div>
      )}
    </div>
  );
}

export default ArticleItem;
