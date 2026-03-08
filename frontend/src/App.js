import React, { useState } from 'react';
import './App.css';
import ModeSelector from './components/ModeSelector';
import Dashboard from './components/Dashboard';

function App() {
  const [mode, setMode] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 TurboTrade - Parallel HFT Backtesting System</h1>
      </header>
      
      {!mode ? (
        <ModeSelector onSelectMode={setMode} />
      ) : (
        <Dashboard mode={mode} onChangeMode={() => setMode(null)} />
      )}
    </div>
  );
}

export default App;
