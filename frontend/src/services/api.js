import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Articles API
export const articlesAPI = {
  getFeed: async (domainId = null, limit = 20, offset = 0) => {
    const params = { limit, offset };
    if (domainId) params.domain_id = domainId;
    const response = await api.get('/articles/feed', { params });
    return response.data;
  },

  getArticle: async (articleId) => {
    const response = await api.get(`/articles/${articleId}`);
    return response.data;
  },

  addFeedback: async (articleId, feedbackType) => {
    const response = await api.post(`/articles/feedback/${articleId}`, null, {
      params: { feedback_type: feedbackType },
    });
    return response.data;
  },

  fetchNow: async () => {
    const response = await api.post('/articles/fetch-now');
    return response.data;
  },
};

// Domains API
export const domainsAPI = {
  getAll: async () => {
    const response = await api.get('/domains');
    return response.data;
  },

  create: async (name, keywords = null) => {
    const response = await api.post('/domains', { name, keywords });
    return response.data;
  },

  delete: async (domainId) => {
    const response = await api.delete(`/domains/${domainId}`);
    return response.data;
  },

  update: async (domainId, name, keywords = null) => {
    const response = await api.put(`/domains/${domainId}`, null, {
      params: { name, keywords: keywords ? keywords.join(',') : null },
    });
    return response.data;
  },
};

// Sources API
export const sourcesAPI = {
  getAll: async () => {
    const response = await api.get('/sources');
    return response.data;
  },

  create: async (name, url, sourceType) => {
    const response = await api.post('/sources', { name, url, source_type: sourceType });
    return response.data;
  },

  delete: async (sourceId) => {
    const response = await api.delete(`/sources/${sourceId}`);
    return response.data;
  },

  suggest: async (name, url, description = null) => {
    const response = await api.post('/sources/suggest', { name, url, description });
    return response.data;
  },

  getPendingSuggestions: async () => {
    const response = await api.get('/sources/suggestions/pending');
    return response.data;
  },

  approveSuggestion: async (suggestionId) => {
    const response = await api.post(`/sources/suggestions/${suggestionId}/approve`);
    return response.data;
  },

  rejectSuggestion: async (suggestionId) => {
    const response = await api.post(`/sources/suggestions/${suggestionId}/reject`);
    return response.data;
  },
};

// Sharing API
export const sharingAPI = {
  createShare: async (articleId) => {
    const response = await api.post(`/share/${articleId}`);
    return response.data;
  },

  getSharedArticle: async (token) => {
    const response = await api.get(`/share/${token}`);
    return response.data;
  },

  deleteShare: async (shareId) => {
    const response = await api.delete(`/share/${shareId}`);
    return response.data;
  },
};

export default api;
