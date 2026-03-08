import React, { useState, useEffect } from 'react';
import ModeSelector from './components/ModeSelector';
import Dashboard from './components/Dashboard';
import './styles/App.css';

function App() {
  const [mode, setMode] = useState(null);
  const [isSimulationRunning, setIsSimulationRunning] = useState(false);

  const handleModeSelect = (selectedMode) => {
    setMode(selectedMode);
    setIsSimulationRunning(false);
  };

  const handleSimulationStart = () => {
    setIsSimulationRunning(true);
  };

  const handleSimulationStop = () => {
    setIsSimulationRunning(false);
  };

  return (
    <div className="App min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Header */}
      <header className="bg-slate-900 shadow-lg border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <i className="fas fa-rocket text-2xl text-cyan-400"></i>
            <h1 className="text-3xl font-bold text-white">TurboTrade</h1>
            <span className="text-sm text-slate-400">v1.0 - Parallel HFT Engine</span>
          </div>
          <div className="text-right">
            <p className="text-slate-400 text-sm">
              {isSimulationRunning ? (
                <span className="text-green-400 font-semibold">
                  <i className="fas fa-circle-notch animate-spin mr-2"></i>
                  Simulation Running
                </span>
              ) : (
                <span>Ready</span>
              )}
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {!mode ? (
          <ModeSelector onModeSelect={handleModeSelect} />
        ) : (
          <Dashboard
            mode={mode}
            onBack={() => setMode(null)}
            isRunning={isSimulationRunning}
            onSimulationStart={handleSimulationStart}
            onSimulationStop={handleSimulationStop}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-700 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-slate-400 text-sm">
          <p>TurboTrade &copy; 2024 - Parallel & Distributed Computing Project</p>
        </div>
      </footer>
    </div>
  );
}

export default App;