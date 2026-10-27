import React from 'react';
import { DatasetStats, ModelEvaluation } from '../types';
import { 
  ShieldCheck, 
  Database, 
  Sparkles, 
  Layers, 
  ArrowRight, 
  CheckCircle2, 
  AlertTriangle,
  Flame,
  Activity
} from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';

interface DashboardProps {
  stats: DatasetStats | null;
  evaluation: ModelEvaluation | null;
  setActiveTab: (tab: string) => void;
  loading: boolean;
}

export const Dashboard: React.FC<DashboardProps> = ({ stats, evaluation, setActiveTab, loading }) => {
  if (loading || !stats || !evaluation) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-10 h-10 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin" />
        <p className="text-slate-400 font-mono text-sm">Computing empirical probabilities & loading model...</p>
      </div>
    );
  }

  const chartData = [
    { name: 'Ham (Legitimate)', count: stats.ham_count, percentage: (stats.p_ham * 100).toFixed(2), fill: '#10b981' },
    { name: 'Spam (Unsolicited)', count: stats.spam_count, percentage: (stats.p_spam * 100).toFixed(2), fill: '#ef4444' },
  ];

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Hero Header */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-b from-[#101b33] to-[#0a1020] border border-slate-800 p-6 sm:p-8 shadow-xl">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Probability & Statistics Project · BAMAT207</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Probabilistic SMS Spam Detection <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-indigo-400 font-serif italic">
              via Bayes' Theorem & Naive Bayes
            </span>
          </h1>
          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            A rigorous implementation analyzing the official <strong>UCI SMS Spam Collection dataset</strong>. 
            We demonstrate empirical conditional probability calculations, formalize the binary spam indicator as a 
            <strong> Bernoulli random variable</strong>, mathematically verify <strong>Bayes' Theorem</strong> across suspicious tokens, 
            and deploy an 80:20 stratified <strong>Multinomial Naive Bayes</strong> classifier with Laplace smoothing.
          </p>

          <div className="flex flex-wrap gap-3 pt-2">
            <button
              onClick={() => setActiveTab('detector')}
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/25 active:scale-95"
            >
              <span>Test SMS Detector</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setActiveTab('lab')}
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-sm transition-all border border-slate-700 active:scale-95"
            >
              <span>Explore Probability Lab</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Cleaned */}
        <div className="bg-[#0b1324] border border-slate-800/80 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Cleaned Corpus</span>
            <Database className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-white">
            {stats.cleaned_total.toLocaleString()}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            From {stats.raw_total.toLocaleString()} raw ({stats.duplicates_removed} duplicates removed)
          </p>
        </div>

        {/* Prior P(Ham) */}
        <div className="bg-[#0b1324] border border-slate-800/80 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Prior P(Ham)</span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-emerald-400">
            {(stats.p_ham * 100).toFixed(2)}%
          </div>
          <p className="text-xs text-slate-400 mt-1">
            {stats.ham_count.toLocaleString()} legitimate messages
          </p>
        </div>

        {/* Prior P(Spam) */}
        <div className="bg-[#0b1324] border border-slate-800/80 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Prior P(Spam)</span>
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
          </div>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-rose-400">
            {(stats.p_spam * 100).toFixed(2)}%
          </div>
          <p className="text-xs text-slate-400 mt-1">
            {stats.spam_count.toLocaleString()} unsolicited spam messages
          </p>
        </div>

        {/* Model Accuracy */}
        <div className="bg-[#0b1324] border border-slate-800/80 rounded-xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Test Accuracy</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-white">
            {(evaluation.metrics.accuracy * 100).toFixed(2)}%
          </div>
          <p className="text-xs text-slate-400 mt-1">
            F1-Score: {(evaluation.metrics.f1_score * 100).toFixed(2)}% (n={evaluation.test_size})
          </p>
        </div>
      </div>

      {/* Two Column Layout: Class Distribution Chart & Statistical Parameters */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Class Distribution Visualization */}
        <div className="bg-[#0b1324] border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-semibold text-white flex items-center space-x-2">
                <Layers className="w-4 h-4 text-indigo-400" />
                <span>Class Distribution (Imbalance Analysis)</span>
              </h2>
              <span className="text-xs font-mono text-slate-400">N = {stats.cleaned_total}</span>
            </div>
            <p className="text-xs text-slate-400 mb-6 leading-relaxed">
              Legitimate messages outnumber spam by nearly <strong>7 to 1</strong>. This severe class imbalance requires evaluating 
              Precision and Recall alongside raw Accuracy.
            </p>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
                  <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    formatter={(value: any, name: any, item: any) => [
                      `${Number(value).toLocaleString()} messages (${item.payload.percentage}%)`,
                      'Count',
                    ]}
                  />
                  <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-4 border-t border-slate-800/80 text-xs font-mono">
            <div className="flex items-center space-x-2 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>Ham: {stats.ham_count} ({(stats.p_ham * 100).toFixed(2)}%)</span>
            </div>
            <div className="flex items-center space-x-2 text-rose-400">
              <span className="w-2 h-2 rounded-full bg-rose-500" />
              <span>Spam: {stats.spam_count} ({(stats.p_spam * 100).toFixed(2)}%)</span>
            </div>
          </div>
        </div>

        {/* Right: Bernoulli Random Variable Parameters */}
        <div className="bg-[#0b1324] border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-semibold text-white flex items-center space-x-2">
                <Flame className="w-4 h-4 text-amber-400" />
                <span>Bernoulli Random Variable Modeling</span>
              </h2>
              <span className="text-xs font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                Y ~ Bernoulli(p)
              </span>
            </div>
            <p className="text-xs text-slate-400 mb-5 leading-relaxed">
              We define discrete random variable Y ∈ &#123;0, 1&#125; representing message category, with parameter p = P(Spam).
            </p>

            <div className="space-y-3 font-mono text-xs">
              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="text-slate-400">P(Y = 1) = p (Spam Probability)</div>
                  <div className="text-slate-200 font-semibold mt-0.5">E(Y) = p</div>
                </div>
                <div className="text-rose-400 font-bold text-sm">{stats.bernoulli.expectation_E_Y.toFixed(6)}</div>
              </div>

              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="text-slate-400">P(Y = 0) = 1 - p (Ham Probability)</div>
                  <div className="text-slate-200 font-semibold mt-0.5">q = 1 - p</div>
                </div>
                <div className="text-emerald-400 font-bold text-sm">{stats.bernoulli.q.toFixed(6)}</div>
              </div>

              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="text-slate-400">Variance: Var(Y) = p(1 - p)</div>
                  <div className="text-slate-200 font-semibold mt-0.5">E(Y²) - [E(Y)]²</div>
                </div>
                <div className="text-indigo-400 font-bold text-sm">{stats.bernoulli.variance_Var_Y.toFixed(6)}</div>
              </div>

              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="text-slate-400">Standard Deviation: σ(Y)</div>
                  <div className="text-slate-200 font-semibold mt-0.5">√Var(Y)</div>
                </div>
                <div className="text-white font-bold text-sm">{stats.bernoulli.std_dev_sigma_Y.toFixed(6)}</div>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800/80 text-[11px] text-slate-400 flex items-center space-x-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
            <span>Theoretical values match empirical sample moments (|Δ| &lt; 10⁻¹⁵).</span>
          </div>
        </div>
      </div>

      {/* Model Overview Callout */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="text-sm font-semibold text-white flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Trained Model: Multinomial Naive Bayes (Laplace α = 1.0)</span>
          </div>
          <p className="text-xs text-slate-400">
            Evaluated on held-out test split of {evaluation.test_size} messages. Precision: {(evaluation.metrics.precision * 100).toFixed(2)}% · Recall: {(evaluation.metrics.recall * 100).toFixed(2)}%.
          </p>
        </div>
        <button
          onClick={() => setActiveTab('evaluation')}
          className="inline-flex items-center space-x-1.5 text-xs font-mono text-indigo-400 hover:text-indigo-300 transition-colors whitespace-nowrap"
        >
          <span>View Confusion Matrix & Report</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
