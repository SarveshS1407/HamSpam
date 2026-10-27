import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Dashboard } from './components/Dashboard';
import { Detector } from './components/Detector';
import { ProbabilityLab } from './components/ProbabilityLab';
import { ModelEvaluation } from './components/ModelEvaluation';
import { About } from './components/About';
import { fetchHealth, fetchStats, fetchProbabilities, fetchEvaluation } from './api';
import { DatasetStats, WordProbabilitiesResponse, ModelEvaluation as ModelEvaluationType } from './types';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);

  const [stats, setStats] = useState<DatasetStats | null>(null);
  const [probabilities, setProbabilities] = useState<WordProbabilitiesResponse | null>(null);
  const [evaluation, setEvaluation] = useState<ModelEvaluationType | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadAllData = async () => {
    setLoading(true);
    setError(null);
    try {
      const healthRes = await fetchHealth();
      setIsBackendHealthy(healthRes.status === 'healthy');

      const [statsData, probsData, evalData] = await Promise.all([
        fetchStats(),
        fetchProbabilities(),
        fetchEvaluation(),
      ]);

      setStats(statsData);
      setProbabilities(probsData);
      setEvaluation(evalData);
      setIsBackendHealthy(true);
    } catch (err: any) {
      console.error('Error loading API data:', err);
      setIsBackendHealthy(false);
      setError(err.message || 'Unable to connect to HamSpam backend service.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#070b14] text-slate-100">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isBackendHealthy={isBackendHealthy}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Global Error Banner */}
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={loadAllData}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 text-xs font-mono transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        )}

        {/* Tab Views */}
        {activeTab === 'dashboard' && (
          <Dashboard
            stats={stats}
            evaluation={evaluation}
            setActiveTab={setActiveTab}
            loading={loading}
          />
        )}

        {activeTab === 'detector' && <Detector />}

        {activeTab === 'lab' && (
          <ProbabilityLab
            stats={stats}
            probabilities={probabilities}
            loading={loading}
          />
        )}

        {activeTab === 'evaluation' && (
          <ModelEvaluation
            evaluation={evaluation}
            loading={loading}
          />
        )}

        {activeTab === 'about' && <About />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#080d1a] py-6 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-2 font-mono">
            <span className="text-white font-bold">HamSpam</span>
            <span>·</span>
            <span>BAMAT207 Probability & Statistics</span>
            <span>·</span>
            <span>VIT Vellore</span>
          </div>
          <div className="flex items-center space-x-4">
            <a
              href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-slate-300 transition-colors"
            >
              UCI Dataset 228
            </a>
            <span>·</span>
            <button
              onClick={() => setActiveTab('about')}
              className="hover:text-slate-300 transition-colors"
            >
              Methodology
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
