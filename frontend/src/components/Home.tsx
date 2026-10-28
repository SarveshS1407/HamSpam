import React from 'react';
import { DatasetStats, ModelEvaluation } from '../types';
import { 
  ShieldCheck, 
  Database, 
  Sparkles, 
  ArrowRight, 
  ShieldAlert, 
  Lock, 
  Smartphone, 
  Scale, 
  ExternalLink,
  Code2,
  FileText,
  Brain,
  Sliders,
  CheckCircle2
} from 'lucide-react';

interface HomeProps {
  stats: DatasetStats | null;
  evaluation: ModelEvaluation | null;
  setActiveTab: (tab: string) => void;
  loading: boolean;
}

export const Home: React.FC<HomeProps> = ({ stats, evaluation, setActiveTab, loading }) => {
  const colabUrl = "https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb";
  const reportPdfUrl = "/HamSpam_Project_Report.pdf";

  return (
    <div className="space-y-12 animate-fadeIn">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-slate-100 via-white to-slate-50 dark:from-[#101b33] dark:via-[#0b1324] dark:to-[#070b14] border border-slate-200 dark:border-slate-800 p-8 sm:p-12 shadow-xl transition-colors">
        <div className="relative z-10 max-w-4xl space-y-6">
          {/* Academic Pill */}
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-indigo-100 dark:bg-indigo-500/10 border border-indigo-200 dark:border-indigo-500/20 text-indigo-700 dark:text-indigo-400 text-xs font-mono">
            <Sparkles className="w-3.5 h-3.5" />
            <span>BAMAT207 Probability & Statistics Project · VIT Vellore</span>
          </div>

          {/* Heading */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight">
            Intelligent Spam Detection <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 via-teal-500 to-indigo-600 dark:from-emerald-400 dark:via-teal-300 dark:to-indigo-400 font-serif italic">
              Powered by Bayes' Theorem
            </span>
          </h1>

          {/* Subtitle / Explanation */}
          <p className="text-slate-600 dark:text-slate-300 text-base sm:text-lg leading-relaxed max-w-3xl">
            HamSpam is an academic machine-learning system that probabilistically classifies incoming SMS messages 
            into legitimate (<strong>Ham</strong>) or unsolicited (<strong>Spam</strong>). Built strictly on the official 
            <strong> UCI SMS Spam Collection benchmark (#228)</strong>, it bridges discrete probability theory, 
            empirical Bayes' Theorem inversion, and supervised <strong>Multinomial Naive Bayes</strong> classification.
          </p>

          {/* CTAs */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => setActiveTab('detector')}
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/25 active:scale-95"
            >
              <span>Launch Spam Detector</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setActiveTab('methodology')}
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-medium text-sm transition-all border border-slate-300 dark:border-slate-700 active:scale-95"
            >
              <span>Explore Dataset & Methodology</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <a
              href={colabUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-amber-100 hover:bg-amber-200 dark:bg-amber-500/10 dark:hover:bg-amber-500/20 text-amber-900 dark:text-amber-300 font-medium text-sm transition-all border border-amber-300 dark:border-amber-500/30"
            >
              <Sparkles className="w-4 h-4 text-amber-500" />
              <span>Open in Google Colab</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>

      {/* 4 Verified KPI Badges Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Accuracy */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Test Accuracy</span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
          </div>
          <div className="text-3xl font-extrabold font-mono text-slate-900 dark:text-white">
            {evaluation ? `${(evaluation.metrics.accuracy * 100).toFixed(2)}%` : '98.07%'}
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            1,015 of 1,035 test messages correctly classified
          </p>
        </div>

        {/* Precision */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Spam Precision</span>
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-500" />
          </div>
          <div className="text-3xl font-extrabold font-mono text-slate-900 dark:text-white">
            {evaluation ? `${(evaluation.metrics.precision * 100).toFixed(2)}%` : '95.12%'}
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Minimizes Type I false alarms (only 6 ham misclassified)
          </p>
        </div>

        {/* Cleaned Corpus */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Cleaned Corpus</span>
            <Database className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-3xl font-extrabold font-mono text-slate-900 dark:text-white">
            {stats ? stats.cleaned_total.toLocaleString() : '5,171'}
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Deduplicated from 5,574 raw records (UCI ID: 228)
          </p>
        </div>

        {/* Bayes Identity */}
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm transition-colors">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Bayes Identity</span>
            <Scale className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-3xl font-extrabold font-mono text-slate-900 dark:text-white">
            100%
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Direct count vs Bayes inversion diff &le; 2.22e-16
          </p>
        </div>
      </div>

      {/* End-to-End Workflow Visualization */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
        <div className="space-y-1">
          <div className="inline-flex items-center space-x-2 text-xs font-mono text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
            <Brain className="w-3.5 h-3.5" />
            <span>Probabilistic Inference Architecture</span>
          </div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            How HamSpam Classifies Messages
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 max-w-2xl">
            A deterministic five-stage probabilistic pipeline executing from raw SMS strings to calibrated posterior class assignments:
          </p>
        </div>

        {/* 5 Stages Flow */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
          {/* Stage 1 */}
          <div className="bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-xs font-bold font-mono flex items-center justify-center">1</span>
              <Smartphone className="w-4 h-4 text-slate-400" />
            </div>
            <h3 className="font-semibold text-sm text-slate-900 dark:text-white">Raw Ingestion</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
              Accepts arbitrary SMS text input (up to 160+ chars, emojis, casing).
            </p>
          </div>

          {/* Stage 2 */}
          <div className="bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-xs font-bold font-mono flex items-center justify-center">2</span>
              <Sliders className="w-4 h-4 text-slate-400" />
            </div>
            <h3 className="font-semibold text-sm text-slate-900 dark:text-white">Tokenization</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
              Lowercases and tokenizes via regex boundary matching (<code className="font-mono text-[10px] bg-slate-200 dark:bg-slate-800 px-1 py-0.5 rounded">\b\w\w+\b</code>).
            </p>
          </div>

          {/* Stage 3 */}
          <div className="bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-xs font-bold font-mono flex items-center justify-center">3</span>
              <Database className="w-4 h-4 text-slate-400" />
            </div>
            <h3 className="font-semibold text-sm text-slate-900 dark:text-white">Bag-of-Words</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
              Maps message into 7,297-dimensional token count vector fitted on training corpus.
            </p>
          </div>

          {/* Stage 4 */}
          <div className="bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-xs font-bold font-mono flex items-center justify-center">4</span>
              <Brain className="w-4 h-4 text-slate-400" />
            </div>
            <h3 className="font-semibold text-sm text-slate-900 dark:text-white">Log-Likelihood</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
              Computes Multinomial Naive Bayes joint log-odds with Laplace smoothing (&alpha;=1.0).
            </p>
          </div>

          {/* Stage 5 */}
          <div className="bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-xl p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="w-6 h-6 rounded-full bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-xs font-bold font-mono flex items-center justify-center">5</span>
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
            </div>
            <h3 className="font-semibold text-sm text-slate-900 dark:text-white">Posterior Class</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
              Softmax normalizes probabilities: flags Spam if P(Spam) &ge; 0.50 with confidence score.
            </p>
          </div>
        </div>
      </div>

      {/* Why Spam Detection Matters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
          <div className="w-10 h-10 rounded-xl bg-rose-100 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400 flex items-center justify-center">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900 dark:text-white">
            Smishing & Financial Fraud
          </h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
            SMS open rates exceed 98%, making it the top vector for mobile phishing ('smishing'), 
            credential harvesting, and unauthorized two-factor authentication intercepts.
          </p>
        </div>

        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
          <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <Smartphone className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900 dark:text-white">
            Strict 160-Character Limit
          </h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
            Unlike email with rich HTML, SPF/DKIM headers, and IP routing signatures, SMS text 
            is short, unstructured, and filled with colloquialisms, requiring sample-efficient models.
          </p>
        </div>

        <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 space-y-3 shadow-sm">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <Lock className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900 dark:text-white">
            Minimizing False Alarms (Type I)
          </h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
            Falsely blocking an authentic banking OTP or emergency medical text has severe consequences. 
            HamSpam prioritizes high Precision (95.12%) to protect legitimate deliveries.
          </p>
        </div>
      </div>

      {/* Academic Deliverables Banner */}
      <div className="bg-gradient-to-r from-indigo-50 via-slate-50 to-emerald-50 dark:from-[#0f172a] dark:via-[#101b33] dark:to-[#0f172a] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-sm">
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-xs font-mono text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
            <FileText className="w-4 h-4" />
            <span>Academic Submission Artifacts</span>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">
            Download the 10-Page Formal Project Report
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 max-w-xl">
            A comprehensive A4 academic report containing full mathematical derivations of Bernoulli variance, 
            Bayes' Theorem proofs, scikit-learn confusion matrices, and system architecture.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <a
            href={reportPdfUrl}
            download="HamSpam_Project_Report.pdf"
            className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-all shadow-md active:scale-95"
          >
            <FileText className="w-4 h-4" />
            <span>Download Report PDF</span>
          </a>
          <a
            href={colabUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-sm font-medium transition-all border border-slate-300 dark:border-slate-700 shadow-sm"
          >
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>Open in Colab</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
};
