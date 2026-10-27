import React from 'react';
import { 
  BookOpen, 
  ExternalLink, 
  GraduationCap, 
  Layers, 
  Cpu, 
  AlertCircle, 
  CheckCircle2,
  Code2
} from 'lucide-react';

export const About: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono">
          <GraduationCap className="w-3.5 h-3.5" />
          <span>Academic Documentation & Project Scope</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          About the HamSpam Project
        </h1>
        <p className="text-sm text-slate-400 leading-relaxed">
          Course project for <strong>BAMAT207 — Probability and Statistics</strong> at 
          <strong> Vellore Institute of Technology (VIT), Vellore</strong>.
        </p>
      </div>

      {/* Project Objective */}
      <div className="bg-[#0b1324] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <h2 className="text-base font-semibold text-white flex items-center space-x-2">
          <BookOpen className="w-4 h-4 text-emerald-400" />
          <span>Project Objective & Scope</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans">
          The goal of <strong>HamSpam</strong> is to develop a complete probabilistic classification system that bridges 
          classical theoretical probability concepts with modern computational natural language processing. 
          Rather than relying on closed-box machine learning APIs, every formula — from Bayes' Theorem to the 
          Bernoulli random variable's expectation and variance — is implemented and validated numerically against 
          the real UCI SMS Spam Collection dataset.
        </p>
      </div>

      {/* Dataset Citation & Source */}
      <div className="bg-[#0b1324] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-semibold text-white flex items-center space-x-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            <span>Dataset Provenance & Preprocessing</span>
          </h2>
          <a
            href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs font-mono text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
          >
            <span>UCI Repository (ID: 228)</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>

        <div className="text-xs sm:text-sm text-slate-300 space-y-3 font-sans leading-relaxed">
          <p>
            The project utilizes the <strong>SMS Spam Collection dataset</strong> created by Tiago A. Almeida and José María Gómez Hidalgo (2011).
          </p>

          <div className="bg-[#080d1a] border border-slate-800 p-3.5 rounded-xl font-mono text-xs text-slate-300 space-y-1">
            <div className="text-slate-500 uppercase text-[10px]">Data Preprocessing Audit:</div>
            <div>• Original Uncleaned Corpus: <strong>5,574</strong> messages</div>
            <div>• Duplicate Messages Removed: <strong>403</strong> messages</div>
            <div>• Missing Values Detected: <strong>0</strong></div>
            <div>• Final Cleaned Corpus: <strong>5,171</strong> messages (4,518 Ham · 653 Spam)</div>
            <div>• Normalized Binary Encoding: <strong>Spam = 1</strong>, <strong>Ham = 0</strong></div>
          </div>
        </div>
      </div>

      {/* Mathematical Methodology */}
      <div className="bg-[#0b1324] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <h2 className="text-base font-semibold text-white flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-teal-400" />
          <span>Multinomial Naive Bayes Mathematics</span>
        </h2>

        <div className="text-xs sm:text-sm text-slate-300 space-y-3 font-sans leading-relaxed">
          <p>
            Given an input message vector x = (x₁, x₂, ..., x_V) of word frequencies from vocabulary V:
          </p>
          <div className="bg-[#080d1a] border border-slate-800 p-3 rounded-xl font-mono text-xs text-indigo-300 text-center">
            P(Y = c | x) ∝ P(Y = c) · ∏ [ P(wᵢ | Y = c) ]^(xᵢ)
          </div>
          <p>
            To prevent zero-probability collapse for words absent in training class $c$, <strong>Laplace add-one smoothing ($\alpha = 1.0$)</strong> is applied:
          </p>
          <div className="bg-[#080d1a] border border-slate-800 p-3 rounded-xl font-mono text-xs text-teal-300 text-center">
            P̂(wᵢ | Y = c) = [ Count(wᵢ, c) + 1 ] / [ ∑ Count(w, c) + |V| ]
          </div>
          <p className="text-xs text-slate-400">
            <strong>Data Leakage Prevention:</strong> The <code>CountVectorizer</code> vocabulary and word counts are 
            strictly fitted on the 80% training partition ($n=4,136$). The 20% test partition ($n=1,035$) is strictly transformed using the frozen vocabulary.
          </p>
        </div>
      </div>

      {/* Limitations and Future Improvements */}
      <div className="bg-[#0b1324] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <h2 className="text-base font-semibold text-white flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-amber-400" />
          <span>Known Limitations & Engineering Considerations</span>
        </h2>

        <ul className="text-xs sm:text-sm text-slate-300 space-y-2.5 list-disc pl-5 font-sans leading-relaxed">
          <li>
            <strong>Naive Conditional Independence Assumption:</strong> Naive Bayes assumes words occur independently given the class label. In reality, words like "claim" and "prize" frequently co-occur.
          </li>
          <li>
            <strong>Out-of-Vocabulary (OOV) Tokens:</strong> Spammers often use spelling tricks (e.g. <code>w!n</code>, <code>fr33</code>). Character n-grams or subword tokenization can improve robustness.
          </li>
          <li>
            <strong>Context & Negation Blindness:</strong> Bag-of-words ignores word order ("free gift" vs "not free"). Contextual transformer embeddings (e.g., DistilBERT) offer semantic modeling for production scale.
          </li>
        </ul>
      </div>

      {/* Author & Footer Note */}
      <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
        <div>
          <span>BAMAT207 Probability and Statistics · VIT Vellore</span>
        </div>
        <div className="font-mono text-slate-500">
          Academic Project
        </div>
      </div>
    </div>
  );
};
