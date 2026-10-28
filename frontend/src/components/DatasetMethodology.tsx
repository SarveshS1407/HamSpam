import React, { useState } from 'react';
import { DatasetStats, WordProbabilitiesResponse, DatasetMeta } from '../types';
import datasetMetaRaw from '../dataset_meta.json';
import { 
  Database, 
  Layers, 
  Workflow, 
  Sliders, 
  BarChart2, 
  Calculator, 
  CheckCircle2, 
  AlertTriangle, 
  Search, 
  ExternalLink, 
  ArrowRight, 
  Sparkles,
  Info,
  Shield,
  HelpCircle
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend, 
  Cell 
} from 'recharts';

interface DatasetMethodologyProps {
  stats: DatasetStats | null;
  probabilities: WordProbabilitiesResponse | null;
  setActiveTab: (tab: string) => void;
  loading: boolean;
}

export const DatasetMethodology: React.FC<DatasetMethodologyProps> = ({
  stats,
  probabilities,
  setActiveTab,
  loading
}) => {
  const meta: DatasetMeta = datasetMetaRaw as DatasetMeta;
  const [activeSection, setActiveSection] = useState<string>('overview');

  // Section C Explorer state
  const [metricView, setMetricView] = useState<'counts' | 'percentages'>('counts');
  const [sampleFilter, setSampleFilter] = useState<'all' | 'ham' | 'spam'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Section D Preprocessing Interactive Demo state
  const [demoInput, setDemoInput] = useState(
    "FREE entry in 2 a weekly competition! WIN £1,000 cash prize. Call urgent 0800123456 now."
  );

  // Section E Feature Extraction Sandbox state
  const [featureInput, setFeatureInput] = useState("Win a free cash prize now");

  const sections = [
    { id: 'overview', label: 'A. Dataset Overview' },
    { id: 'provenance', label: 'B. Provenance Flow' },
    { id: 'explorer', label: 'C. Dataset Explorer' },
    { id: 'preprocessing', label: 'D. Data Preprocessing' },
    { id: 'features', label: 'E. Feature Extraction' },
    { id: 'training', label: 'F. Training & Testing' },
    { id: 'math', label: 'G. Probability & Statistics' },
    { id: 'limitations', label: 'H. Limitations & Ethics' },
  ];

  // Class distribution data based on toggle
  const classDistData = [
    {
      category: 'Ham (Legitimate)',
      count: meta.overview.ham_count,
      percentage: meta.overview.ham_pct,
      fill: '#10b981',
    },
    {
      category: 'Spam (Unsolicited)',
      count: meta.overview.spam_count,
      percentage: meta.overview.spam_pct,
      fill: '#ef4444',
    },
  ];

  // Length distribution chart data
  const lengthDistData = meta.length_stats.distribution.map(b => ({
    bin: b.bin,
    ham: metricView === 'counts' ? b.ham : b.ham_pct,
    spam: metricView === 'counts' ? b.spam : b.spam_pct,
  }));

  // Filtered samples for Section C
  const allSamples = [...meta.samples.ham, ...meta.samples.spam];
  const filteredSamples = allSamples.filter(s => {
    if (sampleFilter !== 'all' && s.label !== sampleFilter) return false;
    if (searchQuery.trim() && !s.message.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  // Preprocessing interactive demo logic
  const normalizedDemo = demoInput.toLowerCase();
  const tokensDemo = normalizedDemo.match(/\b\w\w+\b/g) || [];
  const keywordMatches = ['free', 'prize', 'win', 'urgent', 'offer'].filter(kw => 
    new RegExp(`\\b${kw}\\b`, 'i').test(demoInput)
  );

  // Feature vector extraction demo logic
  const featureTokens = featureInput.toLowerCase().match(/\b\w\w+\b/g) || [];
  const tokenFreqMap: Record<string, number> = {};
  featureTokens.forEach(t => {
    tokenFreqMap[t] = (tokenFreqMap[t] || 0) + 1;
  });

  return (
    <div className="space-y-10 animate-fadeIn">
      {/* Section Header */}
      <div className="space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-100 dark:bg-indigo-500/10 border border-indigo-200 dark:border-indigo-500/20 text-indigo-700 dark:text-indigo-400 text-xs font-mono">
          <Database className="w-3.5 h-3.5" />
          <span>Curriculum Methodology Hub · BAMAT207</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Dataset Provenance, Preprocessing & Probability Theory
        </h1>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">
          An interactive academic guide exploring where the <strong>UCI SMS Spam Collection</strong> originates, 
          how it is audited and transformed, the mathematical proof of <strong>Bayes' Theorem</strong>, and how text 
          becomes numerical inputs for <strong>Multinomial Naive Bayes</strong>.
        </p>
      </div>

      {/* Section Navigation Tabs */}
      <div className="flex flex-wrap gap-2 p-1.5 bg-slate-100 dark:bg-[#0b1324] rounded-2xl border border-slate-200 dark:border-slate-800">
        {sections.map(sec => (
          <button
            key={sec.id}
            onClick={() => setActiveSection(sec.id)}
            className={`px-3.5 py-2 rounded-xl text-xs sm:text-sm font-medium transition-all ${
              activeSection === sec.id
                ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-white shadow-sm border border-slate-200 dark:border-slate-700'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/50 dark:hover:bg-slate-800/40'
            }`}
          >
            {sec.label}
          </button>
        ))}
      </div>

      {/* ==================================================================== */}
      {/* SECTION A: DATASET OVERVIEW */}
      {/* ==================================================================== */}
      {activeSection === 'overview' && (
        <div className="space-y-8 animate-fadeIn">
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-5">
              <div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                  {meta.overview.name}
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                  Hosted by the <strong>UCI Machine Learning Repository</strong> (Dataset ID: <strong>228</strong>)
                </p>
              </div>
              <a
                href={meta.overview.uci_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-indigo-50 dark:bg-indigo-500/10 text-indigo-700 dark:text-indigo-400 text-xs font-medium border border-indigo-200 dark:border-indigo-500/20 hover:bg-indigo-100 dark:hover:bg-indigo-500/20 transition-all self-start sm:self-auto"
              >
                <span>View UCI Repository Page</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>

            {/* Metadata Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block mb-1">AUTHORS / DONORS</span>
                <span className="font-bold text-slate-900 dark:text-white">{meta.overview.authors}</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block mb-1">LICENSE</span>
                <span className="font-bold text-slate-900 dark:text-white">CC BY 4.0 / Open Academic</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block mb-1">FILE FORMAT</span>
                <span className="font-bold text-slate-900 dark:text-white">{meta.overview.format}</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block mb-1">DIGITAL OBJECT IDENTIFIER</span>
                <span className="font-bold text-slate-900 dark:text-white">{meta.overview.doi}</span>
              </div>
            </div>

            {/* What is a Labeled Dataset? */}
            <div className="p-5 rounded-xl bg-indigo-50/50 dark:bg-indigo-500/5 border border-indigo-200 dark:border-indigo-500/10 space-y-2 text-sm text-slate-700 dark:text-slate-300">
              <h3 className="font-bold text-slate-900 dark:text-white flex items-center space-x-2">
                <Info className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                <span>Why Labeled Examples are Necessary for Supervised Classification</span>
              </h3>
              <p className="leading-relaxed">
                In supervised probabilistic learning, the algorithm requires ground-truth labels (<em>Spam = 1</em> or <em>Ham = 0</em>) 
                paired with each message text. This allows the model to compute empirical frequencies: 
                P(W | Spam) (the likelihood of observing token W in spam) versus P(W | Ham) (the likelihood of 
                observing token W in legitimate messages). Without verified labels, class priors and token conditional likelihoods cannot be estimated.
              </p>
            </div>

            {/* Schema Table */}
            <div className="space-y-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">
                Dataset Column Schema
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
                  <thead className="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 uppercase">
                    <tr>
                      <th className="p-3">Column Name</th>
                      <th className="p-3">Data Type</th>
                      <th className="p-3">Encoding & Values</th>
                      <th className="p-3">Description</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                    {meta.overview.columns.map((col, i) => (
                      <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                        <td className="p-3 font-bold text-indigo-600 dark:text-indigo-400">{col.name}</td>
                        <td className="p-3 text-slate-500">{col.type}</td>
                        <td className="p-3 text-slate-900 dark:text-white">{col.values}</td>
                        <td className="p-3 text-slate-600 dark:text-slate-400">{col.description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* SECTION B: PROVENANCE FLOW */}
      {/* ==================================================================== */}
      {activeSection === 'provenance' && (
        <div className="space-y-8 animate-fadeIn">
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="space-y-1">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Dataset Provenance & Transformation Journey
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
                Tracking every transformation step from the original UCI repository download to production deployment:
              </p>
            </div>

            <div className="space-y-4">
              {[
                {
                  step: '1. Upstream Acquisition',
                  source: 'UCI Machine Learning Repository (ID: 228)',
                  details: 'Downloaded via ucimlrepo API into local cached directory `data/SMSSpamCollection` (TSV format, UTF-8 encoded).',
                },
                {
                  step: '2. Missing Value Audit',
                  source: 'Null Value Inspection',
                  details: 'Exact verification of 5,574 rows: confirmed 0 null values across both label and message columns.',
                },
                {
                  step: '3. Deduplication Protocol',
                  source: 'Pruning 403 Duplicate Messages',
                  details: 'Repeated broadcast SMS messages removed (-7.23%), resulting in a distinct cleaned corpus of 5,171 messages.',
                },
                {
                  step: '4. Binary Label Encoding',
                  source: 'Target Normalization',
                  details: 'Labels converted to integers: `ham` -> 0 (4,518 messages), `spam` -> 1 (653 messages).',
                },
                {
                  step: '5. Train/Test Stratification',
                  source: '80:20 Stratified Partition',
                  details: 'Partitioned with random_state=42: 4,136 training messages and 1,035 held-out testing messages preserving exact 87.34% : 12.66% ratio.',
                },
                {
                  step: '6. Zero Data-Leakage Vectorization',
                  source: 'CountVectorizer Fitting',
                  details: 'Vocabulary of 7,297 words fit strictly on training messages; test messages transformed using training vocabulary.',
                },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="flex items-start space-x-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800"
                >
                  <span className="w-8 h-8 rounded-lg bg-indigo-100 dark:bg-indigo-500/20 text-indigo-700 dark:text-indigo-400 font-bold font-mono text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                    {idx + 1}
                  </span>
                  <div className="space-y-0.5">
                    <div className="flex items-center space-x-2">
                      <h3 className="font-bold text-sm text-slate-900 dark:text-white">{item.step}</h3>
                      <span className="text-[11px] font-mono text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-500/10 px-2 py-0.5 rounded">
                        {item.source}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                      {item.details}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Privacy & No Live Logging Guarantee */}
            <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-xs text-emerald-800 dark:text-emerald-300 flex items-start space-x-3">
              <Shield className="w-5 h-5 flex-shrink-0 text-emerald-600 dark:text-emerald-400 mt-0.5" />
              <div>
                <h4 className="font-bold">Strict User Privacy Guarantee:</h4>
                <p className="mt-0.5 leading-relaxed">
                  Messages tested in the live website console or Colab interface are classified on-the-fly and 
                  <strong> NEVER stored, logged, transmitted to third parties, or used to retrain the model</strong>. 
                  HamSpam operates strictly on pre-computed parameters derived from the historical public benchmark.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* SECTION C: DATASET EXPLORER */}
      {/* ==================================================================== */}
      {activeSection === 'explorer' && (
        <div className="space-y-8 animate-fadeIn">
          {/* Controls: Counts vs Percentages */}
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                  Interactive Dataset Statistics
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
                  Visualizing class distribution and message length metrics from the 5,171 cleaned records.
                </p>
              </div>

              {/* Toggle Buttons */}
              <div className="flex items-center space-x-1 p-1 bg-slate-100 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 self-start sm:self-auto">
                <button
                  onClick={() => setMetricView('counts')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                    metricView === 'counts'
                      ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-white shadow-sm'
                      : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  Raw Counts
                </button>
                <button
                  onClick={() => setMetricView('percentages')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                    metricView === 'percentages'
                      ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-white shadow-sm'
                      : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
                  }`}
                >
                  Percentages (%)
                </button>
              </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Class Distribution Chart */}
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-3">
                <span className="text-xs font-mono uppercase text-slate-500 dark:text-slate-400 font-bold block">
                  Class Distribution ({metricView === 'counts' ? 'Messages' : '% Share'})
                </span>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={classDistData} margin={{ top: 20, right: 20, left: 0, bottom: 20 }}>
                      <XAxis dataKey="category" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                      <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                        formatter={(val: any) => [metricView === 'counts' ? `${Number(val).toLocaleString()} msgs` : `${val}%`, 'Value']}
                      />
                      <Bar dataKey={metricView === 'counts' ? 'count' : 'percentage'} radius={[6, 6, 0, 0]}>
                        {classDistData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Length Distribution Chart */}
              <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-3">
                <span className="text-xs font-mono uppercase text-slate-500 dark:text-slate-400 font-bold block">
                  Message Length Profile (Character Buckets)
                </span>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={lengthDistData} margin={{ top: 20, right: 20, left: 0, bottom: 20 }}>
                      <XAxis dataKey="bin" tick={{ fill: '#94a3b8', fontSize: 10 }} />
                      <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                        formatter={(val: any) => [metricView === 'counts' ? `${Number(val).toLocaleString()} msgs` : `${val}%`, 'Count']}
                      />
                      <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                      <Bar dataKey="ham" name="Ham" fill="#10b981" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="spam" name="Spam" fill="#ef4444" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Length Averages Card */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
              <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block">HAM AVG CHARS</span>
                <span className="text-base font-bold text-emerald-600 dark:text-emerald-400">70.9 chars</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block">SPAM AVG CHARS</span>
                <span className="text-base font-bold text-rose-600 dark:text-rose-400">137.7 chars</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block">HAM MEDIAN WORDS</span>
                <span className="text-base font-bold text-emerald-600 dark:text-emerald-400">11 words</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <span className="text-slate-400 block">SPAM MEDIAN WORDS</span>
                <span className="text-base font-bold text-rose-600 dark:text-rose-400">25 words</span>
              </div>
            </div>

            {/* Representative Sample Explorer */}
            <div className="space-y-3 pt-4 border-t border-slate-200 dark:border-slate-800">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Representative Dataset Records
                </h3>
                <div className="flex items-center space-x-2">
                  <div className="relative">
                    <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Search messages..."
                      className="pl-8 pr-3 py-1.5 rounded-lg text-xs bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none"
                    />
                  </div>
                  <div className="flex rounded-lg bg-slate-100 dark:bg-slate-900 p-1 border border-slate-200 dark:border-slate-700 text-xs">
                    {(['all', 'ham', 'spam'] as const).map(f => (
                      <button
                        key={f}
                        onClick={() => setSampleFilter(f)}
                        className={`px-2.5 py-1 rounded text-xs uppercase font-mono ${
                          sampleFilter === f ? 'bg-white dark:bg-slate-800 font-bold text-indigo-600 dark:text-white' : 'text-slate-400'
                        }`}
                      >
                        {f}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Sample Messages Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
                  <thead className="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 uppercase">
                    <tr>
                      <th className="p-2.5 w-16">ID</th>
                      <th className="p-2.5 w-24">Class</th>
                      <th className="p-2.5">Message Content</th>
                      <th className="p-2.5 w-20">Length</th>
                      <th className="p-2.5 w-24">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                    {filteredSamples.slice(0, 8).map((s) => (
                      <tr key={s.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                        <td className="p-2.5 text-slate-400">#{s.id}</td>
                        <td className="p-2.5 font-bold">
                          {s.label === 'spam' ? (
                            <span className="text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-500/10 px-2 py-0.5 rounded">SPAM</span>
                          ) : (
                            <span className="text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-2 py-0.5 rounded">HAM</span>
                          )}
                        </td>
                        <td className="p-2.5 text-slate-700 dark:text-slate-300 max-w-md truncate font-sans text-xs">
                          {s.message}
                        </td>
                        <td className="p-2.5 text-slate-400">{s.length}c / {s.words}w</td>
                        <td className="p-2.5">
                          <button
                            onClick={() => {
                              setActiveTab('detector');
                            }}
                            className="inline-flex items-center space-x-1 text-[11px] text-indigo-600 dark:text-indigo-400 hover:underline"
                          >
                            <span>Test</span>
                            <ArrowRight className="w-3 h-3" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* SECTION D: DATA PREPROCESSING */}
      {/* ==================================================================== */}
      {activeSection === 'preprocessing' && (
        <div className="space-y-8 animate-fadeIn">
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="space-y-1">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Interactive Preprocessing Pipeline
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
                See exactly how raw SMS strings are cleaned and normalized before entering the Naive Bayes vectorizer:
              </p>
            </div>

            {/* Interactive Transformer Input */}
            <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-mono uppercase text-slate-500 dark:text-slate-400 font-bold">
                  Type or modify an SMS message to preview preprocessing transformations:
                </label>
                <input
                  type="text"
                  value={demoInput}
                  onChange={(e) => setDemoInput(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              {/* Before and After Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
                {/* Step 1: Lowercase */}
                <div className="p-3.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1">
                  <span className="text-slate-400 block text-[10px]">1. CASE NORMALIZATION</span>
                  <p className="text-slate-900 dark:text-white truncate font-sans text-xs">{normalizedDemo}</p>
                  <span className="text-[10px] text-slate-400 block pt-1">Prevents case-sensitive duplicates</span>
                </div>

                {/* Step 2: Tokens */}
                <div className="p-3.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1">
                  <span className="text-slate-400 block text-[10px]">2. REGEX TOKENIZATION (\b\w\w+\b)</span>
                  <div className="flex flex-wrap gap-1 max-h-16 overflow-y-auto">
                    {tokensDemo.map((t, idx) => (
                      <span key={idx} className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 text-[10px]">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Step 3: Trigger Word Check */}
                <div className="p-3.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1">
                  <span className="text-slate-400 block text-[10px]">3. SPAM TRIGGER WORDS DETECTED</span>
                  {keywordMatches.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {keywordMatches.map((kw, i) => (
                        <span key={i} className="px-2 py-0.5 rounded bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-300 font-bold text-[11px]">
                          {kw}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-slate-400 italic">No suspicious triggers</span>
                  )}
                </div>
              </div>
            </div>

            {/* Code Locations Table */}
            <div className="space-y-3 pt-2">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">
                Preprocessing Operations in Codebase
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-indigo-600 dark:text-indigo-400 font-bold">
                    <span>clean_dataset()</span>
                    <span className="text-[11px] text-slate-400">src/data_loader.py</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-400 font-sans text-xs">
                    Audits missing rows, prunes exact duplicates (403 dropped), and encodes categorical labels to 0 and 1.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-indigo-600 dark:text-indigo-400 font-bold">
                    <span>CountVectorizer(lowercase=True)</span>
                    <span className="text-[11px] text-slate-400">src/train_model.py</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-400 font-sans text-xs">
                    Converts text messages into sparse document-term frequency matrices over the 7,297-word vocabulary.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* SECTION E: FEATURE EXTRACTION */}
      {/* ==================================================================== */}
      {activeSection === 'features' && (
        <div className="space-y-8 animate-fadeIn">
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="space-y-1">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Feature Extraction: Bag-of-Words Representation
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
                How textual SMS messages become discrete numerical feature vectors for probabilistic Naive Bayes:
              </p>
            </div>

            {/* Interactive Vectorizer Sandbox */}
            <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-mono uppercase text-slate-500 dark:text-slate-400 font-bold">
                  Interactive Vectorizer Sandbox: Enter any short sentence:
                </label>
                <input
                  type="text"
                  value={featureInput}
                  onChange={(e) => setFeatureInput(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              {/* Vector representation display */}
              <div className="space-y-2 font-mono text-xs">
                <span className="text-slate-400 block text-[11px]">ACTIVE FEATURE VECTOR COORDINATES:</span>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(tokenFreqMap).map(([token, count], idx) => (
                    <div key={idx} className="p-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center space-x-2">
                      <span className="text-indigo-600 dark:text-indigo-400 font-bold">"{token}"</span>
                      <span className="text-slate-400">&rarr;</span>
                      <span className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-900 font-bold text-slate-900 dark:text-white">
                        count = {count}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Mathematical Bag-of-Words Explanation */}
            <div className="p-5 rounded-xl bg-indigo-50/50 dark:bg-indigo-500/5 border border-indigo-200 dark:border-indigo-500/10 space-y-3 text-sm text-slate-700 dark:text-slate-300">
              <h3 className="font-bold text-slate-900 dark:text-white">
                Why Bag-of-Words with CountVectorizer?
              </h3>
              <p className="leading-relaxed">
                Multinomial Naive Bayes models text messages as outcomes of a multinomial distribution over a discrete vocabulary 
                V of size |V| = 7,297. Each word count xᵢ acts as the exponent of token likelihood P(wᵢ | c)^(xᵢ). 
                Unlike TF-IDF, which produces continuous real-valued weights, raw token counts directly preserve discrete multinomial probability theory.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* SECTION F: TRAINING AND TESTING */}
      {/* ==================================================================== */}
      {activeSection === 'training' && (
        <div className="space-y-8 animate-fadeIn">
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="space-y-1">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Training, Testing & Data Leakage Prevention
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
                Ensuring unbiased model generalization through strict stratified partitioning:
              </p>
            </div>

            {/* Split Breakdown Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 font-mono text-xs">
              <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-indigo-600 dark:text-indigo-400 font-bold">
                  <span>TRAINING SET (80%)</span>
                  <span>4,136 messages</span>
                </div>
                <div className="space-y-1 text-slate-600 dark:text-slate-400 text-xs font-sans">
                  <p>• Ham: 3,614 messages (87.38%)</p>
                  <p>• Spam: 522 messages (12.62%)</p>
                  <p>• <code>CountVectorizer</code> vocabulary fit strictly on this partition.</p>
                </div>
              </div>

              <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-emerald-600 dark:text-emerald-400 font-bold">
                  <span>HELD-OUT TEST SET (20%)</span>
                  <span>1,035 messages</span>
                </div>
                <div className="space-y-1 text-slate-600 dark:text-slate-400 text-xs font-sans">
                  <p>• Ham: 904 messages (87.34%)</p>
                  <p>• Spam: 131 messages (12.66%)</p>
                  <p>• Completely withheld from vocabulary building to prevent leakage.</p>
                </div>
              </div>
            </div>

            {/* Data Leakage Warning */}
            <div className="p-4 rounded-xl bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/20 text-xs text-amber-800 dark:text-amber-300 flex items-start space-x-3">
              <AlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-600 dark:text-amber-400 mt-0.5" />
              <div>
                <h4 className="font-bold">What is Data Leakage and Why Does It Matter?</h4>
                <p className="mt-0.5 leading-relaxed">
                  Data leakage occurs if the text vectorizer is fitted on the whole dataset before splitting into train/test sets. 
                  This leaks test vocabulary frequencies into the training phase, artificially inflating accuracy scores. 
                  HamSpam guarantees zero data leakage: vocabulary discovery is strictly confined to <code>X_train</code>.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* SECTION G: PROBABILITY & STATISTICS */}
      {/* ==================================================================== */}
      {activeSection === 'math' && (
        <div className="space-y-8 animate-fadeIn">
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="space-y-1">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Mathematical Foundations & Bayes' Theorem Proof
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
                Rigorous mathematical derivations bridging BAMAT207 curriculum concepts with empirical results:
              </p>
            </div>

            {/* Mathematical Derivations Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
              {/* Bernoulli Random Variable Card */}
              <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-3">
                <h3 className="font-bold text-sm text-slate-900 dark:text-white">
                  1. Bernoulli Random Variable Y &isin; &#123;0, 1&#125;
                </h3>
                <div className="space-y-1.5 text-slate-700 dark:text-slate-300">
                  <p>• P(Spam) = p = 653 / 5171 = <strong>0.126281</strong></p>
                  <p>• P(Ham) = q = 1 - p = <strong>0.873719</strong></p>
                  <p>• E(Y) = &sum; y &middot; P(y) = 0(q) + 1(p) = <strong>p = 0.126281</strong></p>
                  <p>• Var(Y) = E(Y<sup>2</sup>) - [E(Y)]<sup>2</sup> = p(1 - p) = <strong>0.110334</strong></p>
                  <p>• &sigma;(Y) = &radic;Var(Y) = <strong>0.332166</strong></p>
                </div>
              </div>

              {/* Bayes' Theorem Statement Card */}
              <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-3">
                <h3 className="font-bold text-sm text-slate-900 dark:text-white">
                  2. Bayes' Law & Total Probability
                </h3>
                <div className="space-y-1.5 text-slate-700 dark:text-slate-300">
                  <p className="font-bold text-indigo-600 dark:text-indigo-400">
                    P(Spam | W) = [ P(W | Spam) &middot; P(Spam) ] / P(W)
                  </p>
                  <p className="text-slate-500 text-[11px] font-sans">Expanding denominator via Law of Total Probability:</p>
                  <p>P(W) = P(W | Spam)P(Spam) + P(W | Ham)P(Ham)</p>
                  <p className="text-[11px] text-slate-500 font-sans pt-1">
                    Confirmed across all keywords to within machine epsilon (&le; 2.22e-16).
                  </p>
                </div>
              </div>
            </div>

            {/* Keyword Contingency Table */}
            {probabilities && (
              <div className="space-y-3 pt-2">
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Empirical Bayes' Verification Table
                </h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-mono border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
                    <thead className="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 uppercase">
                      <tr>
                        <th className="p-2.5">Word (W)</th>
                        <th className="p-2.5">Spam Count</th>
                        <th className="p-2.5">Ham Count</th>
                        <th className="p-2.5">P(W|Spam)</th>
                        <th className="p-2.5">P(W|Ham)</th>
                        <th className="p-2.5">P(Spam|W) Dir</th>
                        <th className="p-2.5">P(Spam|W) Bayes</th>
                        <th className="p-2.5">Difference</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                      {probabilities.words.map((w, idx) => (
                        <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                          <td className="p-2.5 font-bold text-slate-900 dark:text-white uppercase">{w.word}</td>
                          <td className="p-2.5 text-slate-700 dark:text-slate-300">{w.spam_messages}</td>
                          <td className="p-2.5 text-slate-700 dark:text-slate-300">{w.ham_messages}</td>
                          <td className="p-2.5 text-slate-600 dark:text-slate-400">{w.p_word_given_spam.toFixed(4)}</td>
                          <td className="p-2.5 text-slate-600 dark:text-slate-400">{w.p_word_given_ham.toFixed(4)}</td>
                          <td className="p-2.5 font-bold text-indigo-600 dark:text-indigo-400">{w.p_spam_given_word_direct.toFixed(4)}</td>
                          <td className="p-2.5 font-bold text-indigo-600 dark:text-indigo-400">{w.p_spam_given_word_bayes.toFixed(4)}</td>
                          <td className="p-2.5 text-emerald-600 dark:text-emerald-400">{w.bayes_direct_diff.toExponential(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* SECTION I: LIMITATIONS & ETHICS */}
      {/* ==================================================================== */}
      {activeSection === 'limitations' && (
        <div className="space-y-8 animate-fadeIn">
          <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
            <div className="space-y-1">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                Model Limitations & Responsible AI Use
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
                Critical academic analysis of boundaries, potential failure modes, and ethical considerations:
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-2">
                <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4 text-amber-500" />
                  <span>Vocabulary Drift & Adversarial Evasion</span>
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Spammers continually evolve evasion strategies, using unicode homoglyphs, intentional misspellings 
                  (<em>'fr33'</em>, <em>'w!n'</em>), and zero-width spaces. Out-of-vocabulary tokens rely entirely on Laplace smoothing.
                </p>
              </div>

              <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-2">
                <h3 className="font-bold text-sm text-slate-900 dark:text-white flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4 text-amber-500" />
                  <span>Loss of Syntactic Context & Negation</span>
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  Bag-of-words ignores word order: <em>'Free credit cards'</em> and <em>'Are credit cards free?'</em> 
                  produce identical feature coordinates. Phrases like <em>'not free'</em> are split into independent tokens.
                </p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 space-y-1">
              <span className="font-bold text-slate-900 dark:text-white block">Academic Disclaimer:</span>
              <p className="leading-relaxed">
                HamSpam's predictions represent calibrated posterior probabilities conditioned on historical training evidence. 
                They are probabilistic estimations rather than absolute legal or security guarantees.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
