import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/App.css';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import SharedArticle from './pages/SharedArticle';
import { articlesAPI } from './services/api';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/share/:token" element={<SharedArticle />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
