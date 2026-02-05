import React, { useState, useEffect } from 'react';
import { FiPlus, FiX } from 'react-icons/fi';
import { domainsAPI } from '../services/api';

function DomainPanel({ onDomainChange }) {
  const [domains, setDomains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newDomain, setNewDomain] = useState('');
  const [newKeywords, setNewKeywords] = useState('');
  const [selectedDomain, setSelectedDomain] = useState(null);

  useEffect(() => {
    loadDomains();
  }, []);

  const loadDomains = async () => {
    try {
      setLoading(true);
      const data = await domainsAPI.getAll();
      setDomains(data);
    } catch (err) {
      setError('Failed to load domains');
    } finally {
      setLoading(false);
    }
  };

  const handleAddDomain = async (e) => {
    e.preventDefault();
    if (!newDomain.trim()) return;

    try {
      const keywords = newKeywords.split(',').map((k) => k.trim()).filter((k) => k);
      await domainsAPI.create(newDomain, keywords.length > 0 ? keywords : null);
      setNewDomain('');
      setNewKeywords('');
      await loadDomains();
    } catch (err) {
      setError('Failed to add domain');
    }
  };

  const handleDeleteDomain = async (domainId) => {
    try {
      await domainsAPI.delete(domainId);
      await loadDomains();
      if (selectedDomain === domainId) {
        setSelectedDomain(null);
        onDomainChange && onDomainChange(null);
      }
    } catch (err) {
      setError('Failed to delete domain');
    }
  };

  const handleSelectDomain = (domainId) => {
    setSelectedDomain(domainId);
    onDomainChange && onDomainChange(domainId);
  };

  if (loading) return <div className="loading">Loading domains...</div>;

  return (
    <div>
      <h4 style={{ marginBottom: '1rem', color: '#8b3a3a' }}>Topics of Interest</h4>

      <form onSubmit={handleAddDomain} style={{ marginBottom: '1rem' }}>
        <div className="form-group" style={{ marginBottom: '0.5rem' }}>
          <input
            type="text"
            className="form-input"
            placeholder="Add new topic"
            value={newDomain}
            onChange={(e) => setNewDomain(e.target.value)}
            style={{ marginBottom: '0.5rem' }}
          />
          <input
            type="text"
            className="form-input"
            placeholder="Keywords (comma-separated)"
            value={newKeywords}
            onChange={(e) => setNewKeywords(e.target.value)}
            style={{ marginBottom: '0.5rem', fontSize: '0.875rem' }}
          />
          <button type="submit" className="btn btn-primary btn-sm" style={{ width: '100%' }}>
            <FiPlus /> Add Topic
          </button>
        </div>
      </form>

      <div style={{
        maxHeight: '300px',
        overflowY: 'auto',
        border: '1px solid #bdc3c7',
        borderRadius: '4px',
        padding: '0.5rem'
      }}>
        {domains.length === 0 ? (
          <p style={{ color: '#7f8c8d', textAlign: 'center', padding: '1rem' }}>
            No topics yet
          </p>
        ) : (
          domains.map((domain) => (
            <div
              key={domain.id}
              onClick={() => handleSelectDomain(domain.id)}
              style={{
                padding: '0.5rem',
                borderRadius: '4px',
                cursor: 'pointer',
                marginBottom: '0.5rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                backgroundColor: selectedDomain === domain.id ? '#f0f0f0' : 'transparent',
                border: selectedDomain === domain.id ? '1px solid #8b3a3a' : 'none',
                transition: 'all 0.2s ease'
              }}
            >
              <span style={{ fontSize: '0.875rem' }}>{domain.name}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteDomain(domain.id);
                }}
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

      {error && <div className="notification notification-error" style={{ marginTop: '1rem' }}>{error}</div>}
    </div>
  );
}

export default DomainPanel;
