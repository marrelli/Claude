import React, { useState, useEffect } from 'react';
import { FiPlus, FiX, FiCheckCircle, FiXCircle } from 'react-icons/fi';
import { sourcesAPI } from '../services/api';

function SourcePanel() {
  const [sources, setSources] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newSourceName, setNewSourceName] = useState('');
  const [newSourceUrl, setNewSourceUrl] = useState('');
  const [newSourceDesc, setNewSourceDesc] = useState('');
  const [activeTab, setActiveTab] = useState('sources');

  useEffect(() => {
    loadSourcesAndSuggestions();
  }, []);

  const loadSourcesAndSuggestions = async () => {
    try {
      setLoading(true);
      const data = await sourcesAPI.getAll();
      setSources(data.sources || []);
      setSuggestions(data.suggestions || []);
    } catch (err) {
      setError('Failed to load sources');
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestSource = async (e) => {
    e.preventDefault();
    if (!newSourceName.trim() || !newSourceUrl.trim()) return;

    try {
      await sourcesAPI.suggest(newSourceName, newSourceUrl, newSourceDesc || null);
      setNewSourceName('');
      setNewSourceUrl('');
      setNewSourceDesc('');
      await loadSourcesAndSuggestions();
    } catch (err) {
      setError('Failed to suggest source');
    }
  };

  const handleDeleteSource = async (sourceId) => {
    try {
      await sourcesAPI.delete(sourceId);
      await loadSourcesAndSuggestions();
    } catch (err) {
      setError('Failed to delete source');
    }
  };

  const handleApproveSuggestion = async (suggestionId) => {
    try {
      await sourcesAPI.approveSuggestion(suggestionId);
      await loadSourcesAndSuggestions();
    } catch (err) {
      setError('Failed to approve suggestion');
    }
  };

  const handleRejectSuggestion = async (suggestionId) => {
    try {
      await sourcesAPI.rejectSuggestion(suggestionId);
      await loadSourcesAndSuggestions();
    } catch (err) {
      setError('Failed to reject suggestion');
    }
  };

  if (loading) return <div className="loading">Loading sources...</div>;

  return (
    <div>
      <h4 style={{ marginBottom: '1rem', color: '#8b3a3a' }}>Information Sources</h4>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <button
          onClick={() => setActiveTab('sources')}
          style={{
            flex: 1,
            padding: '0.5rem',
            borderRadius: '4px',
            border: activeTab === 'sources' ? '2px solid #8b3a3a' : '1px solid #bdc3c7',
            background: activeTab === 'sources' ? '#f0f0f0' : 'white',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: 500
          }}
        >
          Active ({sources.length})
        </button>
        <button
          onClick={() => setActiveTab('suggest')}
          style={{
            flex: 1,
            padding: '0.5rem',
            borderRadius: '4px',
            border: activeTab === 'suggest' ? '2px solid #8b3a3a' : '1px solid #bdc3c7',
            background: activeTab === 'suggest' ? '#f0f0f0' : 'white',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: 500
          }}
        >
          Suggest
        </button>
        <button
          onClick={() => setActiveTab('pending')}
          style={{
            flex: 1,
            padding: '0.5rem',
            borderRadius: '4px',
            border: activeTab === 'pending' ? '2px solid #8b3a3a' : '1px solid #bdc3c7',
            background: activeTab === 'pending' ? '#f0f0f0' : 'white',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: 500
          }}
        >
          Pending ({suggestions.filter((s) => s.status === 'pending').length})
        </button>
      </div>

      {activeTab === 'sources' && (
        <div style={{
          maxHeight: '300px',
          overflowY: 'auto',
          border: '1px solid #bdc3c7',
          borderRadius: '4px',
          padding: '0.5rem'
        }}>
          {sources.length === 0 ? (
            <p style={{ color: '#7f8c8d', textAlign: 'center', padding: '1rem' }}>
              No active sources
            </p>
          ) : (
            sources.map((source) => (
              <div
                key={source.id}
                style={{
                  padding: '0.5rem',
                  borderRadius: '4px',
                  marginBottom: '0.5rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  backgroundColor: '#fafafa',
                  border: '1px solid #ecf0f1'
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '0.875rem', fontWeight: 500 }}>{source.name}</div>
                  <div style={{ fontSize: '0.75rem', color: '#7f8c8d' }}>{source.source_type}</div>
                </div>
                <button
                  onClick={() => handleDeleteSource(source.id)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#e74c3c',
                    cursor: 'pointer',
                    padding: 0
                  }}
                >
                  <FiX size={14} />
                </button>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'suggest' && (
        <form onSubmit={handleSuggestSource} style={{ marginBottom: '1rem' }}>
          <div className="form-group" style={{ marginBottom: '0.5rem' }}>
            <input
              type="text"
              className="form-input"
              placeholder="Source name"
              value={newSourceName}
              onChange={(e) => setNewSourceName(e.target.value)}
              style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}
            />
            <input
              type="url"
              className="form-input"
              placeholder="URL"
              value={newSourceUrl}
              onChange={(e) => setNewSourceUrl(e.target.value)}
              style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}
            />
            <textarea
              className="form-textarea"
              placeholder="Description (optional)"
              value={newSourceDesc}
              onChange={(e) => setNewSourceDesc(e.target.value)}
              style={{ marginBottom: '0.5rem', fontSize: '0.875rem', minHeight: '60px' }}
            />
            <button type="submit" className="btn btn-primary btn-sm" style={{ width: '100%' }}>
              <FiPlus /> Suggest Source
            </button>
          </div>
        </form>
      )}

      {activeTab === 'pending' && (
        <div style={{
          maxHeight: '300px',
          overflowY: 'auto',
          border: '1px solid #bdc3c7',
          borderRadius: '4px',
          padding: '0.5rem'
        }}>
          {suggestions.filter((s) => s.status === 'pending').length === 0 ? (
            <p style={{ color: '#7f8c8d', textAlign: 'center', padding: '1rem' }}>
              No pending suggestions
            </p>
          ) : (
            suggestions
              .filter((s) => s.status === 'pending')
              .map((suggestion) => (
                <div
                  key={suggestion.id}
                  style={{
                    padding: '0.5rem',
                    borderRadius: '4px',
                    marginBottom: '0.5rem',
                    backgroundColor: '#fffbea',
                    border: '1px solid #f39c12',
                    fontSize: '0.875rem'
                  }}
                >
                  <div style={{ fontWeight: 500 }}>{suggestion.name}</div>
                  <div style={{ color: '#7f8c8d', fontSize: '0.75rem', marginBottom: '0.5rem' }}>
                    {suggestion.url}
                  </div>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      onClick={() => handleApproveSuggestion(suggestion.id)}
                      style={{
                        flex: 1,
                        padding: '0.25rem 0.5rem',
                        background: '#27ae60',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '0.75rem',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.25rem'
                      }}
                    >
                      <FiCheckCircle size={12} /> Approve
                    </button>
                    <button
                      onClick={() => handleRejectSuggestion(suggestion.id)}
                      style={{
                        flex: 1,
                        padding: '0.25rem 0.5rem',
                        background: '#e74c3c',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '0.75rem',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.25rem'
                      }}
                    >
                      <FiXCircle size={12} /> Reject
                    </button>
                  </div>
                </div>
              ))
          )}
        </div>
      )}

      {error && <div className="notification notification-error" style={{ marginTop: '1rem' }}>{error}</div>}
    </div>
  );
}

export default SourcePanel;
