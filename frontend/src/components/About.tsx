import React from 'react';
import { 
  BookOpen, 
  ExternalLink, 
  GraduationCap, 
  Layers, 
  Cpu, 
  AlertCircle, 
  CheckCircle2,
  Code2,
  FileText,
  Sparkles,
  ShieldCheck,
  Award
} from 'lucide-react';

export const About: React.FC = () => {
  const colabUrl = "https://colab.research.google.com/github/SarveshS1407/HamSpam/blob/main/notebooks/HamSpam_Colab_Evaluation.ipynb";
  const reportPdfUrl = "/HamSpam_Project_Report.pdf";

  return (
    <div className="max-w-4xl mx-auto space-y-10 animate-fadeIn">
      {/* Header */}
      <div className="space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-100 dark:bg-indigo-500/10 border border-indigo-200 dark:border-indigo-500/20 text-indigo-700 dark:text-indigo-400 text-xs font-mono">
          <GraduationCap className="w-4 h-4" />
          <span>Academic Project Documentation · BAMAT207</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          About the HamSpam Project
        </h1>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed">
          Course project for <strong>BAMAT207 — Probability and Statistics</strong> at 
          <strong> Vellore Institute of Technology (VIT), Vellore</strong>.
        </p>

        {/* Action Buttons: Colab & Report PDF */}
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <a
            href={colabUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-amber-100 hover:bg-amber-200 dark:bg-amber-500/10 dark:hover:bg-amber-500/20 text-amber-900 dark:text-amber-300 font-medium text-sm transition-all border border-amber-300 dark:border-amber-500/30 shadow-sm"
          >
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>Open in Google Colab (One-Click Viva)</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
          <a
            href={reportPdfUrl}
            download="HamSpam_Project_Report.pdf"
            className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-md active:scale-95"
          >
            <FileText className="w-4 h-4" />
            <span>Download 10-Page Report PDF</span>
          </a>
        </div>
      </div>

      {/* Project Objective */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 transition-colors">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
          <BookOpen className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <span>Project Objective & Theoretical Scope</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-sans">
          The primary objective of <strong>HamSpam</strong> is to develop a complete probabilistic classification system that bridges 
          classical theoretical probability concepts with computational machine learning. 
          Rather than treating classification as a black box, every mathematical formula — from Bayes' Theorem to the 
          Bernoulli random variable's expectation, variance, and Laplace add-one smoothing — is implemented and validated numerically against 
          the real UCI SMS Spam Collection benchmark dataset.
        </p>
      </div>

      {/* Dataset Citation & Source */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 transition-colors">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
            <Layers className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <span>Dataset Provenance & Preprocessing Audit</span>
          </h2>
          <a
            href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs font-mono text-indigo-600 dark:text-indigo-400 hover:underline flex items-center space-x-1"
          >
            <span>UCI Repository (ID: 228)</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>

        <div className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 space-y-3 font-sans leading-relaxed">
          <p>
            The project strictly utilizes the authentic <strong>SMS Spam Collection dataset</strong> created by Tiago A. Almeida and José María Gómez Hidalgo (2011).
          </p>

          <div className="bg-slate-50 dark:bg-[#080d1a] border border-slate-200 dark:border-slate-800 p-4 rounded-2xl font-mono text-xs text-slate-700 dark:text-slate-300 space-y-1.5">
            <div className="text-slate-400 dark:text-slate-500 uppercase text-[10px] font-semibold">Strict Data Preprocessing Audit:</div>
            <div>• Original Uncleaned Corpus: <strong>5,574</strong> raw messages</div>
            <div>• Duplicate Messages Removed: <strong>403</strong> messages (7.23% duplication rate)</div>
            <div>• Missing / Null Values Detected: <strong>0</strong></div>
            <div>• Final Cleaned Corpus: <strong>5,171</strong> messages (4,518 Ham · 653 Spam)</div>
            <div>• Stratified 80/20 Split: <strong>4,136</strong> training · <strong>1,035</strong> testing</div>
            <div>• Normalized Binary Encoding: <strong>Spam = 1</strong>, <strong>Ham = 0</strong></div>
          </div>
        </div>
      </div>

      {/* Mathematical Methodology */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 transition-colors">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-teal-600 dark:text-teal-400" />
          <span>Multinomial Naive Bayes Mathematics</span>
        </h2>

        <div className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 space-y-3 font-sans leading-relaxed">
          <p>
            Given an input message vector x = (x₁, x₂, ..., x_V) of token frequencies over vocabulary V:
          </p>
          <div className="bg-slate-50 dark:bg-[#080d1a] border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl font-mono text-xs text-indigo-700 dark:text-indigo-300 text-center">
            P(Y = c | x) ∝ P(Y = c) · ∏ [ P(wᵢ | Y = c) ]^(xᵢ)
          </div>
          <p>
            To prevent zero-probability collapse for words absent in training class c, <strong>Laplace add-one smoothing (α = 1.0)</strong> is applied:
          </p>
          <div className="bg-slate-50 dark:bg-[#080d1a] border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl font-mono text-xs text-teal-700 dark:text-teal-300 text-center">
            P̂(wᵢ | Y = c) = [ Count(wᵢ, c) + 1 ] / [ ∑ Count(w, c) + |V| ]
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            <strong>Data Leakage Prevention:</strong> The <code>CountVectorizer</code> vocabulary and word counts are 
            strictly fitted on the 80% training partition (\(n=4,136\)). The 20% test partition (\(n=1,035\)) is strictly transformed using the frozen vocabulary.
          </p>
        </div>
      </div>

      {/* Limitations and Future Improvements */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 transition-colors">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-amber-500" />
          <span>Known Limitations & Engineering Considerations</span>
        </h2>

        <ul className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 space-y-2.5 list-disc pl-5 font-sans leading-relaxed">
          <li>
            <strong>Conditional Independence Assumption:</strong> Naive Bayes assumes words occur independently given the class label. In reality, words like "claim" and "prize" frequently co-occur. Despite this violation, Bayes decision boundaries remain highly effective.
          </li>
          <li>
            <strong>Out-of-Vocabulary (OOV) Tokens:</strong> Adversarial spammers use deliberate misspellings (e.g. <code>w!n</code>, <code>fr33</code>). Character n-grams or subword tokenization provide greater robustness.
          </li>
          <li>
            <strong>Context & Negation Blindness:</strong> Bag-of-words ignores word order ("free trial" vs "not free"). Transformer embeddings (e.g., DistilBERT) offer contextual representation for complex semantic boundaries.
          </li>
        </ul>
      </div>

      {/* Technology Stack Grid */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 transition-colors">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center space-x-2">
          <Code2 className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
          <span>Technology Stack</span>
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
          <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
            <div className="font-semibold text-slate-900 dark:text-white">Python 3.10+</div>
            <div className="text-[11px] text-slate-500">Core Runtime</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
            <div className="font-semibold text-slate-900 dark:text-white">scikit-learn</div>
            <div className="text-[11px] text-slate-500">MultinomialNB & BoW</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
            <div className="font-semibold text-slate-900 dark:text-white">React & Vite</div>
            <div className="text-[11px] text-slate-500">Frontend Web UI</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
            <div className="font-semibold text-slate-900 dark:text-white">FastAPI</div>
            <div className="text-[11px] text-slate-500">REST API Engine</div>
          </div>
        </div>
      </div>

      {/* Author & Footer Note */}
      <div className="p-5 rounded-2xl bg-slate-100 dark:bg-[#080d1a] border border-slate-200 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center space-x-2">
          <Award className="w-4 h-4 text-indigo-500" />
          <span>BAMAT207 Probability and Statistics · Vellore Institute of Technology (VIT), Vellore</span>
        </div>
        <div className="font-mono text-slate-500 text-[11px]">
          Academic Submission 2026
        </div>
      </div>
    </div>
  );
};
