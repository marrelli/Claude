import React, { useState } from 'react';
import { FiRefreshCw, FiX } from 'react-icons/fi';
import DomainPanel from './DomainPanel';
import SourcePanel from './SourcePanel';

function Sidebar({ onFetchNow, onDomainChange, loading }) {
  const [activePanel, setActivePanel] = useState('domains');

  return (
    <div className="sidebar">
      <button
        onClick={onFetchNow}
        disabled={loading}
        className="btn btn-primary"
        style={{ width: '100%' }}
      >
        <FiRefreshCw /> {loading ? 'Fetching...' : 'Fetch Now'}
      </button>

      <div style={{
        background: 'white',
        borderRadius: '8px',
        border: '1px solid #bdc3c7',
        overflow: 'hidden'
      }}>
        <div style={{ display: 'flex', borderBottom: '1px solid #bdc3c7' }}>
          <button
            onClick={() => setActivePanel('domains')}
            className={activePanel === 'domains' ? 'btn' : 'btn btn-outline'}
            style={{
              flex: 1,
              borderRadius: 0,
              backgroundColor: activePanel === 'domains' ? '#8b3a3a' : 'transparent',
              color: activePanel === 'domains' ? 'white' : '#8b3a3a',
              border: 'none',
              padding: '0.75rem',
              fontSize: '0.875rem',
              fontWeight: 500
            }}
          >
            Domains
          </button>
          <button
            onClick={() => setActivePanel('sources')}
            className={activePanel === 'sources' ? 'btn' : 'btn btn-outline'}
            style={{
              flex: 1,
              borderRadius: 0,
              backgroundColor: activePanel === 'sources' ? '#8b3a3a' : 'transparent',
              color: activePanel === 'sources' ? 'white' : '#8b3a3a',
              border: 'none',
              padding: '0.75rem',
              fontSize: '0.875rem',
              fontWeight: 500
            }}
          >
            Sources
          </button>
        </div>

        <div style={{ padding: '1rem' }}>
          {activePanel === 'domains' && <DomainPanel onDomainChange={onDomainChange} />}
          {activePanel === 'sources' && <SourcePanel />}
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
