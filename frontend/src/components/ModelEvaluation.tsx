import React from 'react';
import { ModelEvaluation as ModelEvaluationType } from '../types';
import { 
  BarChart3, 
  Target, 
  CheckCircle2, 
  AlertTriangle, 
  Layers, 
  Info,
  ShieldCheck,
  Zap
} from 'lucide-react';

interface ModelEvaluationProps {
  evaluation: ModelEvaluationType | null;
  loading: boolean;
}

export const ModelEvaluation: React.FC<ModelEvaluationProps> = ({ evaluation, loading }) => {
  if (loading || !evaluation) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-10 h-10 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin" />
        <p className="text-slate-400 font-mono text-sm">Evaluating classifier metrics on held-out test data...</p>
      </div>
    );
  }

  const { metrics, confusion_matrix: cm, test_distribution: dist } = evaluation;

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
          <Target className="w-3.5 h-3.5" />
          <span>Generalization Performance Metrics</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Model Evaluation & Confusion Matrix Analysis
        </h1>
        <p className="text-sm text-slate-400 max-w-3xl leading-relaxed">
          Performance of the <strong>Multinomial Naive Bayes</strong> classifier on the held-out test set 
          (<strong>80% training / 20% testing stratified split</strong>, n = 1,035).
        </p>
      </div>

      {/* KPI Cards: The 4 Core Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        {/* Accuracy */}
        <div className="bg-[#0b1324] border border-slate-800 rounded-xl p-5 relative overflow-hidden">
          <div className="text-xs text-slate-400 mb-1">ACCURACY</div>
          <div className="text-3xl font-bold text-white">
            {(metrics.accuracy * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">(TP + TN) / Total</div>
          <div className="text-[11px] text-emerald-400 mt-0.5">1,015 / 1,035 correct</div>
        </div>

        {/* Precision */}
        <div className="bg-[#0b1324] border border-slate-800 rounded-xl p-5 relative overflow-hidden">
          <div className="text-xs text-slate-400 mb-1">PRECISION (SPAM)</div>
          <div className="text-3xl font-bold text-indigo-400">
            {(metrics.precision * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">TP / (TP + FP)</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Low false alarm rate (FP=6)</div>
        </div>

        {/* Recall */}
        <div className="bg-[#0b1324] border border-slate-800 rounded-xl p-5 relative overflow-hidden">
          <div className="text-xs text-slate-400 mb-1">RECALL (SPAM)</div>
          <div className="text-3xl font-bold text-teal-400">
            {(metrics.recall * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">TP / (TP + FN)</div>
          <div className="text-[11px] text-slate-400 mt-0.5">117 of 131 spam caught</div>
        </div>

        {/* F1-Score */}
        <div className="bg-[#0b1324] border border-slate-800 rounded-xl p-5 relative overflow-hidden">
          <div className="text-xs text-slate-400 mb-1">F1-SCORE (HARMONIC)</div>
          <div className="text-3xl font-bold text-rose-400">
            {(metrics.f1_score * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">2 · (P · R) / (P + R)</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Harmonic balance</div>
        </div>
      </div>

      {/* Confusion Matrix Interactive Visualization */}
      <div className="bg-[#0b1324] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-800">
          <div>
            <h2 className="text-base font-semibold text-white flex items-center space-x-2">
              <BarChart3 className="w-4 h-4 text-indigo-400" />
              <span>Test Confusion Matrix Heatmap (n = {evaluation.test_size})</span>
            </h2>
            <p className="text-xs text-slate-400">
              Columns denote model predictions; rows denote actual ground truth labels.
            </p>
          </div>
          <div className="text-xs font-mono text-slate-400">
            <span>Split: 80% Train ({evaluation.train_size}) / 20% Test ({evaluation.test_size})</span>
          </div>
        </div>

        {/* 2x2 Grid Visualization */}
        <div className="max-w-xl mx-auto">
          {/* Header row labels */}
          <div className="grid grid-cols-2 gap-3 mb-2 font-mono text-center text-xs font-semibold text-slate-400">
            <div>PREDICTED HAM (0)</div>
            <div>PREDICTED SPAM (1)</div>
          </div>

          <div className="space-y-3 font-mono">
            {/* Row 1: Actual Ham */}
            <div className="grid grid-cols-2 gap-3">
              {/* True Negative */}
              <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/40 relative">
                <div className="text-[10px] text-emerald-400 uppercase tracking-wider font-semibold">
                  True Negative (TN)
                </div>
                <div className="text-2xl sm:text-3xl font-bold text-emerald-300 mt-1">
                  {cm.tn}
                </div>
                <div className="text-[11px] text-slate-400 mt-1 font-sans">
                  Genuine message correctly delivered as Ham
                </div>
                <span className="absolute top-3 right-3 text-emerald-500 text-xs">✓ Correct</span>
              </div>

              {/* False Positive (Type I) */}
              <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 relative">
                <div className="text-[10px] text-amber-400 uppercase tracking-wider font-semibold">
                  False Positive (FP) · Type I
                </div>
                <div className="text-2xl sm:text-3xl font-bold text-amber-300 mt-1">
                  {cm.fp}
                </div>
                <div className="text-[11px] text-slate-400 mt-1 font-sans">
                  Genuine message falsely flagged as Spam (False Alarm)
                </div>
                <span className="absolute top-3 right-3 text-amber-400 text-xs">⚠️ Type I Error</span>
              </div>
            </div>

            {/* Row 2: Actual Spam */}
            <div className="grid grid-cols-2 gap-3">
              {/* False Negative (Type II) */}
              <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 relative">
                <div className="text-[10px] text-rose-400 uppercase tracking-wider font-semibold">
                  False Negative (FN) · Type II
                </div>
                <div className="text-2xl sm:text-3xl font-bold text-rose-300 mt-1">
                  {cm.fn}
                </div>
                <div className="text-[11px] text-slate-400 mt-1 font-sans">
                  Spam message missed and delivered to user inbox
                </div>
                <span className="absolute top-3 right-3 text-rose-400 text-xs">⚠️ Type II Error</span>
              </div>

              {/* True Positive */}
              <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/40 relative">
                <div className="text-[10px] text-indigo-400 uppercase tracking-wider font-semibold">
                  True Positive (TP)
                </div>
                <div className="text-2xl sm:text-3xl font-bold text-indigo-300 mt-1">
                  {cm.tp}
                </div>
                <div className="text-[11px] text-slate-400 mt-1 font-sans">
                  Spam message successfully detected & filtered
                </div>
                <span className="absolute top-3 right-3 text-indigo-400 text-xs">✓ Correct</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Critical Academic Discussion: Why Accuracy is Misleading */}
      <div className="bg-gradient-to-r from-amber-950/20 via-slate-900 to-slate-900 border border-amber-500/30 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center space-x-2 text-amber-400 font-semibold text-sm">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" />
          <span>Academic Analysis: The Dummy Majority-Class Baseline Paradox</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs text-slate-300 leading-relaxed font-sans">
          <div className="space-y-2">
            <p>
              In our held-out test partition of <strong>1,035 messages</strong>:
            </p>
            <ul className="list-disc pl-4 space-y-1 font-mono text-slate-400">
              <li>Actual Ham: {dist.ham_count} messages ({(dist.ham_proportion * 100).toFixed(2)}%)</li>
              <li>Actual Spam: {dist.spam_count} messages ({(dist.spam_proportion * 100).toFixed(2)}%)</li>
            </ul>
            <p>
              If a naive "dummy" classifier simply predicted <strong>Ham</strong> for every single incoming message:
            </p>
            <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800 font-mono text-amber-300">
              Trivial Accuracy = {dist.ham_count} / {evaluation.test_size} = {(dist.ham_proportion * 100).toFixed(2)}%
              <br />
              Spam Recall = 0 / {dist.spam_count} = 0.00%
            </div>
          </div>

          <div className="space-y-2">
            <p>
              Despite presenting an apparently impressive <strong>87.34% accuracy</strong>, such a filter would completely fail in the real world by catching <strong>zero spam</strong>!
            </p>
            <p>
              Therefore, in class-imbalanced probabilistic problems:
            </p>
            <ul className="list-disc pl-4 space-y-1 text-slate-400">
              <li><strong>Precision (95.12%)</strong> verifies that when the filter flags spam, it is genuinely spam.</li>
              <li><strong>Recall (89.31%)</strong> verifies that 89.31% of incoming spam messages are caught.</li>
              <li><strong>F1-Score (92.13%)</strong> proves that the model learns discriminative word token distributions rather than guessing the majority class.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Scikit-Learn Classification Report Table */}
      <div className="bg-[#0b1324] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <h3 className="text-sm font-semibold text-white flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Full Scikit-Learn Classification Report</span>
        </h3>

        <div className="overflow-x-auto font-mono text-xs">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase text-[11px] bg-slate-900/60">
                <th className="py-2.5 px-4">Class</th>
                <th className="py-2.5 px-4 text-right">Precision</th>
                <th className="py-2.5 px-4 text-right">Recall</th>
                <th className="py-2.5 px-4 text-right">F1-Score</th>
                <th className="py-2.5 px-4 text-right">Support</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              <tr>
                <td className="py-2.5 px-4 font-bold text-emerald-400">Ham (0)</td>
                <td className="py-2.5 px-4 text-right text-slate-300">0.9846 (98.46%)</td>
                <td className="py-2.5 px-4 text-right text-slate-300">0.9934 (99.34%)</td>
                <td className="py-2.5 px-4 text-right text-slate-300">0.9890 (98.90%)</td>
                <td className="py-2.5 px-4 text-right text-slate-400">904</td>
              </tr>
              <tr>
                <td className="py-2.5 px-4 font-bold text-rose-400">Spam (1)</td>
                <td className="py-2.5 px-4 text-right text-slate-300">0.9512 (95.12%)</td>
                <td className="py-2.5 px-4 text-right text-slate-300">0.8931 (89.31%)</td>
                <td className="py-2.5 px-4 text-right text-slate-300">0.9213 (92.13%)</td>
                <td className="py-2.5 px-4 text-right text-slate-400">131</td>
              </tr>
              <tr className="bg-slate-900/30 font-semibold text-slate-200">
                <td className="py-2.5 px-4">Macro Avg</td>
                <td className="py-2.5 px-4 text-right">0.9679</td>
                <td className="py-2.5 px-4 text-right">0.9432</td>
                <td className="py-2.5 px-4 text-right">0.9551</td>
                <td className="py-2.5 px-4 text-right">1,035</td>
              </tr>
              <tr className="bg-slate-900/30 font-semibold text-slate-200">
                <td className="py-2.5 px-4">Weighted Avg</td>
                <td className="py-2.5 px-4 text-right">0.9804</td>
                <td className="py-2.5 px-4 text-right">0.9807</td>
                <td className="py-2.5 px-4 text-right">0.9804</td>
                <td className="py-2.5 px-4 text-right">1,035</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
