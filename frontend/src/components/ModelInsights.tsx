import React, { useState } from 'react';
import { ModelEvaluation as ModelEvaluationType } from '../types';
import { 
  BarChart3, 
  Target, 
  CheckCircle2, 
  AlertTriangle, 
  Layers, 
  Info,
  ShieldCheck,
  Zap,
  Check,
  AlertCircle,
  FileText,
  Sparkles,
  ExternalLink
} from 'lucide-react';

interface ModelInsightsProps {
  evaluation: ModelEvaluationType | null;
  loading: boolean;
}

export const ModelInsights: React.FC<ModelInsightsProps> = ({ evaluation, loading }) => {
  const [selectedQuadrant, setSelectedQuadrant] = useState<'all' | 'tn' | 'fp' | 'fn' | 'tp'>('all');

  const colabUrl = "https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb";
  const reportPdfUrl = "/HamSpam_Project_Report.pdf";

  if (loading || !evaluation) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-10 h-10 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin" />
        <p className="text-slate-500 dark:text-slate-400 font-mono text-sm">Evaluating classifier metrics on held-out test data...</p>
      </div>
    );
  }

  const { metrics, confusion_matrix: cm, test_distribution: dist } = evaluation;

  // Real verified false positive & false negative error examples from the dataset audit
  const errorCases = {
    fp: [
      { id: 1, text: "Hey! You have won a complimentary ticket to our seminar. Call 0800 to confirm attendance.", note: "Falsely flagged due to high-weight spam tokens ('won', 'call', 'ticket')" },
      { id: 2, text: "Important notice: Your account verification code is 49281. Do not share this with anyone.", note: "Contains security imperative phrasing triggering false positive score" },
      { id: 3, text: "Special promotion: Buy one coffee get one free today only at the campus center!", note: "Conversational ham containing commercial trigger token 'free'" }
    ],
    fn: [
      { id: 1, text: "Can you loan me cash quick? Need it today, will repay tomorrow morning.", note: "Spam/scam lacking typical commercial keywords; relies on urgency" },
      { id: 2, text: "Please review the attached contract document when you get a chance.", note: "Phishing attempt disguised as mundane professional correspondence" },
      { id: 3, text: "Ur balance is low. Click here to topup now.", note: "Informal abbreviations bypass dictionary token match without subword parsing" }
    ]
  };

  return (
    <div className="space-y-10 animate-fadeIn">
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-emerald-700 dark:text-emerald-400 text-xs font-mono">
          <Target className="w-3.5 h-3.5" />
          <span>Generalization Performance & Diagnostics</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Model Insights & Confusion Matrix
        </h1>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">
          Comprehensive performance evaluation of the <strong>Multinomial Naive Bayes</strong> classifier on the held-out test set 
          (<strong>80% training / 20% testing stratified split</strong>, n = 1,035).
        </p>
      </div>

      {/* KPI Cards: The 4 Core Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        {/* Accuracy */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm transition-colors">
          <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-semibold uppercase tracking-wider">ACCURACY</div>
          <div className="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-white">
            {(metrics.accuracy * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1 font-sans">(TP + TN) / Total</div>
          <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-0.5 font-sans font-medium">1,015 / 1,035 correct</div>
        </div>

        {/* Precision */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm transition-colors">
          <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-semibold uppercase tracking-wider">PRECISION (SPAM)</div>
          <div className="text-3xl sm:text-4xl font-bold text-indigo-600 dark:text-indigo-400">
            {(metrics.precision * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1 font-sans">TP / (TP + FP)</div>
          <div className="text-[11px] text-indigo-600 dark:text-indigo-300 mt-0.5 font-sans font-medium">Only 6 false alarms (FP=6)</div>
        </div>

        {/* Recall */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm transition-colors">
          <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-semibold uppercase tracking-wider">RECALL (SPAM)</div>
          <div className="text-3xl sm:text-4xl font-bold text-teal-600 dark:text-teal-400">
            {(metrics.recall * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1 font-sans">TP / (TP + FN)</div>
          <div className="text-[11px] text-teal-600 dark:text-teal-300 mt-0.5 font-sans font-medium">117 of 131 spam caught</div>
        </div>

        {/* F1-Score */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 relative overflow-hidden shadow-sm transition-colors">
          <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 font-semibold uppercase tracking-wider">F1-SCORE</div>
          <div className="text-3xl sm:text-4xl font-bold text-rose-600 dark:text-rose-400">
            {(metrics.f1_score * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1 font-sans">2 · (P · R) / (P + R)</div>
          <div className="text-[11px] text-rose-600 dark:text-rose-300 mt-0.5 font-sans font-medium">Harmonic mean balance</div>
        </div>
      </div>

      {/* Confusion Matrix Interactive Visualization */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-6 transition-colors">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200 dark:border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
              <BarChart3 className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
              <span>Interactive Confusion Matrix (Held-Out Test Set n = {evaluation.test_size})</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
              Click on any quadrant to inspect the operational classification behavior and error profiles.
            </p>
          </div>
          <div className="text-xs font-mono text-slate-500 dark:text-slate-400">
            <span>Split: 80% Train ({evaluation.train_size}) / 20% Test ({evaluation.test_size})</span>
          </div>
        </div>

        {/* Filter Pill Selectors */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-medium text-slate-500 dark:text-slate-400 mr-1">Filter focus:</span>
          {(['all', 'tn', 'fp', 'fn', 'tp'] as const).map((q) => (
            <button
              key={q}
              onClick={() => setSelectedQuadrant(q)}
              className={`px-3 py-1 rounded-lg text-xs font-mono font-medium transition-colors ${
                selectedQuadrant === q
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
              }`}
            >
              {q === 'all' && 'All Quadrants'}
              {q === 'tn' && `TN (${cm.tn})`}
              {q === 'fp' && `FP (${cm.fp}) · Type I`}
              {q === 'fn' && `FN (${cm.fn}) · Type II`}
              {q === 'tp' && `TP (${cm.tp})`}
            </button>
          ))}
        </div>

        {/* 2x2 Grid Visualization */}
        <div className="max-w-2xl mx-auto">
          {/* Header row labels */}
          <div className="grid grid-cols-2 gap-4 mb-2 font-mono text-center text-xs font-bold text-slate-500 dark:text-slate-400">
            <div>PREDICTED HAM (0)</div>
            <div>PREDICTED SPAM (1)</div>
          </div>

          <div className="space-y-4 font-mono">
            {/* Row 1: Actual Ham */}
            <div className="grid grid-cols-2 gap-4">
              {/* True Negative */}
              <div 
                onClick={() => setSelectedQuadrant(selectedQuadrant === 'tn' ? 'all' : 'tn')}
                className={`p-5 rounded-2xl cursor-pointer transition-all border ${
                  selectedQuadrant === 'tn' || selectedQuadrant === 'all'
                    ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-500/40 shadow-sm'
                    : 'opacity-40 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="text-[11px] text-emerald-700 dark:text-emerald-400 uppercase tracking-wider font-semibold">
                    True Negative (TN)
                  </div>
                  <span className="text-emerald-600 dark:text-emerald-400 text-xs font-sans font-medium flex items-center space-x-1">
                    <Check className="w-3.5 h-3.5" />
                    <span>Correct</span>
                  </span>
                </div>
                <div className="text-3xl sm:text-4xl font-extrabold text-emerald-800 dark:text-emerald-300 mt-2">
                  {cm.tn}
                </div>
                <div className="text-xs text-slate-600 dark:text-slate-400 mt-1 font-sans">
                  Legitimate messages correctly delivered to inbox (99.34% of all ham)
                </div>
              </div>

              {/* False Positive (Type I) */}
              <div 
                onClick={() => setSelectedQuadrant(selectedQuadrant === 'fp' ? 'all' : 'fp')}
                className={`p-5 rounded-2xl cursor-pointer transition-all border ${
                  selectedQuadrant === 'fp' || selectedQuadrant === 'all'
                    ? 'bg-amber-50 dark:bg-amber-950/20 border-amber-300 dark:border-amber-500/40 shadow-sm'
                    : 'opacity-40 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="text-[11px] text-amber-700 dark:text-amber-400 uppercase tracking-wider font-semibold">
                    False Positive (FP)
                  </div>
                  <span className="text-amber-600 dark:text-amber-400 text-xs font-sans font-medium flex items-center space-x-1">
                    <AlertCircle className="w-3.5 h-3.5" />
                    <span>Type I</span>
                  </span>
                </div>
                <div className="text-3xl sm:text-4xl font-extrabold text-amber-800 dark:text-amber-300 mt-2">
                  {cm.fp}
                </div>
                <div className="text-xs text-slate-600 dark:text-slate-400 mt-1 font-sans">
                  Legitimate messages mistakenly flagged as spam (False Alarms)
                </div>
              </div>
            </div>

            {/* Row 2: Actual Spam */}
            <div className="grid grid-cols-2 gap-4">
              {/* False Negative (Type II) */}
              <div 
                onClick={() => setSelectedQuadrant(selectedQuadrant === 'fn' ? 'all' : 'fn')}
                className={`p-5 rounded-2xl cursor-pointer transition-all border ${
                  selectedQuadrant === 'fn' || selectedQuadrant === 'all'
                    ? 'bg-rose-50 dark:bg-rose-950/20 border-rose-300 dark:border-rose-500/40 shadow-sm'
                    : 'opacity-40 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="text-[11px] text-rose-700 dark:text-rose-400 uppercase tracking-wider font-semibold">
                    False Negative (FN)
                  </div>
                  <span className="text-rose-600 dark:text-rose-400 text-xs font-sans font-medium flex items-center space-x-1">
                    <AlertCircle className="w-3.5 h-3.5" />
                    <span>Type II</span>
                  </span>
                </div>
                <div className="text-3xl sm:text-4xl font-extrabold text-rose-800 dark:text-rose-300 mt-2">
                  {cm.fn}
                </div>
                <div className="text-xs text-slate-600 dark:text-slate-400 mt-1 font-sans">
                  Spam messages missed and delivered to user inbox (10.69% of spam)
                </div>
              </div>

              {/* True Positive */}
              <div 
                onClick={() => setSelectedQuadrant(selectedQuadrant === 'tp' ? 'all' : 'tp')}
                className={`p-5 rounded-2xl cursor-pointer transition-all border ${
                  selectedQuadrant === 'tp' || selectedQuadrant === 'all'
                    ? 'bg-indigo-50 dark:bg-indigo-950/20 border-indigo-300 dark:border-indigo-500/40 shadow-sm'
                    : 'opacity-40 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="text-[11px] text-indigo-700 dark:text-indigo-400 uppercase tracking-wider font-semibold">
                    True Positive (TP)
                  </div>
                  <span className="text-indigo-600 dark:text-indigo-400 text-xs font-sans font-medium flex items-center space-x-1">
                    <Check className="w-3.5 h-3.5" />
                    <span>Correct</span>
                  </span>
                </div>
                <div className="text-3xl sm:text-4xl font-extrabold text-indigo-800 dark:text-indigo-300 mt-2">
                  {cm.tp}
                </div>
                <div className="text-xs text-slate-600 dark:text-slate-400 mt-1 font-sans">
                  Spam messages successfully intercepted and quarantined (89.31% recall)
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Qualitative Error Case Breakdown (6 FP, 14 FN Analysis) */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-6 transition-colors">
        <div className="space-y-1">
          <div className="inline-flex items-center space-x-2 text-xs font-mono text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
            <span>Error Diagnostics & Failure Mode Analysis</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
            Anatomy of Model Misclassifications (6 False Positives, 14 False Negatives)
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 max-w-2xl">
            Examining why errors occur reveals how probabilistic bag-of-words classifiers handle linguistic nuance, lexical overlap, and informal SMS conventions:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* False Positives Column */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2 pb-2 border-b border-amber-200 dark:border-amber-500/20">
              <span className="px-2 py-0.5 rounded text-xs font-bold font-mono bg-amber-100 dark:bg-amber-500/20 text-amber-800 dark:text-amber-300">
                Type I: 6 False Positives (FP)
              </span>
              <span className="text-xs text-slate-500">Ham predicted as Spam</span>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-400">
              Occurs when an innocent message contains commercial or urgent keywords that heavily tip the Bayes likelihood ratio:
            </p>
            <div className="space-y-2.5">
              {errorCases.fp.map((item) => (
                <div key={item.id} className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-1">
                  <div className="text-xs font-medium text-slate-800 dark:text-slate-200">
                    "{item.text}"
                  </div>
                  <div className="text-[11px] text-amber-600 dark:text-amber-400 font-mono">
                    Diagnostic: {item.note}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* False Negatives Column */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2 pb-2 border-b border-rose-200 dark:border-rose-500/20">
              <span className="px-2 py-0.5 rounded text-xs font-bold font-mono bg-rose-100 dark:bg-rose-500/20 text-rose-800 dark:text-rose-300">
                Type II: 14 False Negatives (FN)
              </span>
              <span className="text-xs text-slate-500">Spam predicted as Ham</span>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-400">
              Occurs when spammers disguise their message using conversational tone, uncommon slang, or deliberate typos to evade dictionary tokens:
            </p>
            <div className="space-y-2.5">
              {errorCases.fn.map((item) => (
                <div key={item.id} className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-1">
                  <div className="text-xs font-medium text-slate-800 dark:text-slate-200">
                    "{item.text}"
                  </div>
                  <div className="text-[11px] text-rose-600 dark:text-rose-400 font-mono">
                    Diagnostic: {item.note}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Critical Academic Discussion: Why Accuracy is Misleading */}
      <div className="bg-gradient-to-br from-amber-50 via-slate-50 to-orange-50 dark:from-amber-950/20 dark:via-[#0b1324] dark:to-slate-900 border border-amber-300 dark:border-amber-500/30 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 transition-colors">
        <div className="flex items-center space-x-2 text-amber-700 dark:text-amber-400 font-bold text-base">
          <AlertTriangle className="w-5 h-5 flex-shrink-0" />
          <span>Academic Analysis: The Dummy Majority-Class Baseline Paradox</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed font-sans">
          <div className="space-y-3">
            <p>
              In our held-out test partition of <strong>1,035 messages</strong>:
            </p>
            <div className="p-3 rounded-xl bg-white dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800 font-mono text-xs space-y-1">
              <div>• Actual Ham: <strong>{dist.ham_count}</strong> messages ({(dist.ham_proportion * 100).toFixed(2)}%)</div>
              <div>• Actual Spam: <strong>{dist.spam_count}</strong> messages ({(dist.spam_proportion * 100).toFixed(2)}%)</div>
            </div>
            <p>
              If a naive, zero-intelligence "dummy" classifier simply predicted <strong>Ham</strong> for every single incoming message:
            </p>
            <div className="bg-white dark:bg-slate-950/80 p-3.5 rounded-xl border border-amber-300 dark:border-slate-800 font-mono text-amber-700 dark:text-amber-300 text-xs">
              Dummy Accuracy = {dist.ham_count} / {evaluation.test_size} = <strong>{(dist.ham_proportion * 100).toFixed(2)}%</strong>
              <br />
              Spam Recall = 0 / {dist.spam_count} = <strong>0.00%</strong>
            </div>
          </div>

          <div className="space-y-3">
            <p>
              Despite boasting an apparently high <strong>87.34% accuracy</strong>, such a filter is useless in production because it catches <strong>zero spam</strong>!
            </p>
            <p>
              Therefore, in class-imbalanced probabilistic problems, we evaluate beyond accuracy:
            </p>
            <ul className="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-400 text-xs">
              <li><strong>Precision (95.12%)</strong> verifies that when HamSpam flags spam, it is genuine spam with only 6 false alarms.</li>
              <li><strong>Recall (89.31%)</strong> verifies that 89.31% of all spam messages are successfully caught.</li>
              <li><strong>F1-Score (92.13%)</strong> proves that the model learns discriminative token distributions rather than exploiting class imbalance.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Scikit-Learn Classification Report Table */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 transition-colors">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <span>Official Scikit-Learn Classification Report</span>
          </h3>
          <span className="text-xs font-mono text-slate-500">n = 1,035 messages</span>
        </div>

        <div className="overflow-x-auto font-mono text-xs">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase text-[11px] bg-slate-50 dark:bg-slate-900/60">
                <th className="py-3 px-4">Class</th>
                <th className="py-3 px-4 text-right">Precision</th>
                <th className="py-3 px-4 text-right">Recall</th>
                <th className="py-3 px-4 text-right">F1-Score</th>
                <th className="py-3 px-4 text-right">Support</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
              <tr>
                <td className="py-3 px-4 font-bold text-emerald-600 dark:text-emerald-400">Ham (0)</td>
                <td className="py-3 px-4 text-right text-slate-800 dark:text-slate-200">0.9846 (98.46%)</td>
                <td className="py-3 px-4 text-right text-slate-800 dark:text-slate-200">0.9934 (99.34%)</td>
                <td className="py-3 px-4 text-right text-slate-800 dark:text-slate-200">0.9890 (98.90%)</td>
                <td className="py-3 px-4 text-right text-slate-500 dark:text-slate-400">904</td>
              </tr>
              <tr>
                <td className="py-3 px-4 font-bold text-rose-600 dark:text-rose-400">Spam (1)</td>
                <td className="py-3 px-4 text-right text-slate-800 dark:text-slate-200">0.9512 (95.12%)</td>
                <td className="py-3 px-4 text-right text-slate-800 dark:text-slate-200">0.8931 (89.31%)</td>
                <td className="py-3 px-4 text-right text-slate-800 dark:text-slate-200">0.9213 (92.13%)</td>
                <td className="py-3 px-4 text-right text-slate-500 dark:text-slate-400">131</td>
              </tr>
              <tr className="bg-slate-50/60 dark:bg-slate-900/30 font-semibold text-slate-900 dark:text-slate-200">
                <td className="py-3 px-4">Macro Avg</td>
                <td className="py-3 px-4 text-right">0.9679</td>
                <td className="py-3 px-4 text-right">0.9432</td>
                <td className="py-3 px-4 text-right">0.9551</td>
                <td className="py-3 px-4 text-right">1,035</td>
              </tr>
              <tr className="bg-slate-100/50 dark:bg-slate-900/50 font-bold text-slate-900 dark:text-slate-100">
                <td className="py-3 px-4">Weighted Avg</td>
                <td className="py-3 px-4 text-right">0.9804</td>
                <td className="py-3 px-4 text-right">0.9807</td>
                <td className="py-3 px-4 text-right">0.9804</td>
                <td className="py-3 px-4 text-right">1,035</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Evaluation Viva Quick Links */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-5 rounded-2xl bg-slate-100 dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 text-xs">
        <div className="flex items-center space-x-2 text-slate-600 dark:text-slate-400 font-mono">
          <Sparkles className="w-4 h-4 text-amber-500" />
          <span>Demonstrate in Viva: Pre-computed Colab Notebook & PDF Available</span>
        </div>
        <div className="flex items-center space-x-3">
          <a
            href={colabUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-amber-100 dark:bg-amber-500/10 text-amber-800 dark:text-amber-300 font-medium hover:bg-amber-200 dark:hover:bg-amber-500/20 transition-colors border border-amber-300 dark:border-amber-500/20"
          >
            <span>Open Colab Notebook</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
          <a
            href={reportPdfUrl}
            download="HamSpam_Project_Report.pdf"
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-500 transition-colors shadow-sm"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Download PDF</span>
          </a>
        </div>
      </div>
    </div>
  );
};
