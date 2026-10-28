import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Home } from './components/Home';
import { Detector } from './components/Detector';
import { DatasetMethodology } from './components/DatasetMethodology';
import { ModelInsights } from './components/ModelInsights';
import { About } from './components/About';
import { fetchHealth, fetchStats, fetchProbabilities, fetchEvaluation } from './api';
import { DatasetStats, WordProbabilitiesResponse, ModelEvaluation as ModelEvaluationType } from './types';
import { AlertCircle, RefreshCw, FileText, Sparkles, ExternalLink } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('home');
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);

  const [stats, setStats] = useState<DatasetStats | null>(null);
  const [probabilities, setProbabilities] = useState<WordProbabilitiesResponse | null>(null);
  const [evaluation, setEvaluation] = useState<ModelEvaluationType | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Theme state: dark (default) or light
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    const savedTheme = localStorage.getItem('hamspam_theme');
    if (savedTheme === 'light' || savedTheme === 'dark') {
      return savedTheme;
    }
    return 'dark';
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('hamspam_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

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
      console.warn('Backend unavailable, using pre-computed verified dataset stats & evaluation:', err);
      setIsBackendHealthy(false);
      // In static frontend deployment, we use pre-computed authentic metrics
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  const colabUrl = "https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb";
  const reportPdfUrl = "/HamSpam_Project_Report.pdf";

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-[#070b14] text-slate-800 dark:text-slate-100 transition-colors duration-200">
      {/* Top Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isBackendHealthy={isBackendHealthy}
        theme={theme}
        toggleTheme={toggleTheme}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        {/* Error notification banner if backend has critical issue */}
        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-700 dark:text-rose-300 text-sm flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <AlertCircle className="w-5 h-5 text-rose-500 flex-shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={loadAllData}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-800 dark:text-rose-200 text-xs font-mono transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        )}

        {/* 5 Views */}
        {activeTab === 'home' && (
          <Home
            stats={stats}
            evaluation={evaluation}
            setActiveTab={setActiveTab}
            loading={loading}
          />
        )}

        {activeTab === 'detector' && <Detector />}

        {activeTab === 'methodology' && (
          <DatasetMethodology
            stats={stats}
            probabilities={probabilities}
            setActiveTab={setActiveTab}
            loading={loading}
          />
        )}

        {activeTab === 'insights' && (
          <ModelInsights
            evaluation={evaluation}
            loading={loading}
          />
        )}

        {activeTab === 'about' && <About />}
      </main>

      {/* Global Academic Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800/80 bg-white dark:bg-[#080d1a] py-8 text-xs text-slate-500 dark:text-slate-400 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-2 font-mono">
            <span className="text-slate-900 dark:text-white font-bold">HamSpam</span>
            <span>·</span>
            <span>BAMAT207 Probability & Statistics</span>
            <span>·</span>
            <span>VIT Vellore</span>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-4">
            <a
              href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-slate-900 dark:hover:text-slate-200 transition-colors"
            >
              UCI Dataset 228
            </a>
            <span>·</span>
            <a
              href={colabUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-slate-900 dark:hover:text-slate-200 transition-colors inline-flex items-center space-x-1 text-amber-600 dark:text-amber-400"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Google Colab</span>
            </a>
            <span>·</span>
            <a
              href={reportPdfUrl}
              download="HamSpam_Project_Report.pdf"
              className="hover:text-slate-900 dark:hover:text-slate-200 transition-colors inline-flex items-center space-x-1 text-indigo-600 dark:text-indigo-400"
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Report PDF</span>
            </a>
            <span>·</span>
            <button
              onClick={() => setActiveTab('about')}
              className="hover:text-slate-900 dark:hover:text-slate-200 transition-colors"
            >
              About & Scope
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
