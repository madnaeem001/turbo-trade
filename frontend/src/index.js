import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';          // use root index.css
import './App.css';     // optional if you use it
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);