import React, { useState } from 'react';
import { predictSMS } from '../api';
import { PredictionResult } from '../types';
import { 
  Send, 
  RotateCcw, 
  Sparkles, 
  ShieldAlert, 
  ShieldCheck, 
  Info, 
  AlertCircle,
  CheckCircle2,
  Clock
} from 'lucide-react';

export const Detector: React.FC = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const sampleMessages = [
    {
      label: 'Spam Winner Sample',
      type: 'spam',
      text: 'Congratulations! You have won a free prize. Claim now.',
    },
    {
      label: 'Casual Lunch Sample',
      type: 'ham',
      text: 'Hey, are we meeting for lunch today?',
    },
    {
      label: 'Urgent Draw Sample',
      type: 'spam',
      text: 'URGENT! You have won a 1 week FREE membership in our £100,000 prize draw!',
    },
    {
      label: 'Academic Inquiry Sample',
      type: 'ham',
      text: 'Can you please send me the lecture slides for BAMAT207?',
    },
  ];

  const handlePredict = async (textToPredict?: string) => {
    const text = textToPredict !== undefined ? textToPredict : message;
    if (!text.trim()) {
      setError('Please enter a valid SMS message to classify.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const res = await predictSMS(text);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to communicate with prediction service.');
    } finally {
      setLoading(false);
    }
  };

  const handleSampleClick = (sampleText: string) => {
    setMessage(sampleText);
    handlePredict(sampleText);
  };

  const handleReset = () => {
    setMessage('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Real-Time Inference Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          SMS Spam Classification Console
        </h1>
        <p className="text-sm text-slate-400">
          Enter any SMS message to compute estimated posterior probabilities P(Spam | Message) 
          and P(Ham | Message) using the trained <strong>Multinomial Naive Bayes</strong> model.
        </p>
      </div>

      {/* Main Classifier Card */}
      <div className="bg-[#0b1324] border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
        {/* Text Area */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>INPUT MESSAGE</span>
            <span>{message.length} characters</span>
          </div>
          <textarea
            rows={4}
            value={message}
            onChange={(e) => {
              setMessage(e.target.value);
              if (error) setError(null);
            }}
            placeholder="Type or paste an SMS message here (e.g., 'URGENT: Your account requires verification...')"
            className="w-full bg-[#080d1a] border border-slate-700/80 rounded-xl p-4 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/40 focus:border-indigo-500 transition-all font-sans leading-relaxed"
          />
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePredict()}
              disabled={loading || !message.trim()}
              className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/25 active:scale-95 disabled:pointer-events-none"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                  <span>Computing Probabilities...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Detect Spam</span>
                </>
              )}
            </button>

            {message && (
              <button
                onClick={handleReset}
                className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-sm transition-all border border-slate-700 flex items-center space-x-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Clear</span>
              </button>
            )}
          </div>

          <div className="text-[11px] font-mono text-slate-500 flex items-center space-x-1">
            <Clock className="w-3.5 h-3.5" />
            <span>Inference latency: &lt; 5ms</span>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Sample Messages Quick Picker */}
        <div className="pt-4 border-t border-slate-800/80 space-y-2.5">
          <div className="text-xs font-mono text-slate-400">
            LOAD OFFICIAL TEST SAMPLES:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {sampleMessages.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => handleSampleClick(sample.text)}
                className="text-left p-3 rounded-lg bg-slate-900 hover:bg-slate-800/80 border border-slate-800 transition-all group flex flex-col justify-between"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[11px] font-mono text-slate-400 font-semibold group-hover:text-indigo-400 transition-colors">
                    {sample.label}
                  </span>
                  <span
                    className={`text-[10px] font-mono uppercase px-1.5 py-0.5 rounded ${
                      sample.type === 'spam'
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}
                  >
                    Expected {sample.type}
                  </span>
                </div>
                <p className="text-xs text-slate-300 line-clamp-1 italic">
                  "{sample.text}"
                </p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Prediction Output Card */}
      {result && result.is_valid && (
        <div
          className={`rounded-2xl border p-6 sm:p-8 space-y-6 transition-all duration-300 ${
            result.predicted_label === 'Spam'
              ? 'bg-rose-950/20 border-rose-500/40 shadow-2xl shadow-rose-950/40'
              : 'bg-emerald-950/20 border-emerald-500/40 shadow-2xl shadow-emerald-950/40'
          }`}
        >
          {/* Status Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/80">
            <div className="flex items-center space-x-3">
              {result.predicted_label === 'Spam' ? (
                <div className="w-12 h-12 rounded-xl bg-rose-500/20 border border-rose-500/30 flex items-center justify-center text-rose-400">
                  <ShieldAlert className="w-7 h-7" />
                </div>
              ) : (
                <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                  <ShieldCheck className="w-7 h-7" />
                </div>
              )}
              <div>
                <div className="text-xs font-mono uppercase text-slate-400 tracking-wider">
                  CLASSIFICATION DECISION
                </div>
                <div
                  className={`text-2xl font-bold font-mono ${
                    result.predicted_label === 'Spam' ? 'text-rose-400' : 'text-emerald-400'
                  }`}
                >
                  {result.predicted_label === 'Spam' ? '🚨 SPAM DETECTED' : '🟢 LEGITIMATE HAM'}
                </div>
              </div>
            </div>

            <div className="text-right font-mono text-xs text-slate-400">
              <div>Decision Threshold: τ = 0.50</div>
              <div className="text-slate-300">
                Confidence:{' '}
                <strong className="text-white">
                  {(
                    (result.predicted_label === 'Spam' ? (result.p_spam ?? 0) : (result.p_ham ?? 0)) * 100
                  ).toFixed(2)}
                  %
                </strong>
              </div>
            </div>
          </div>

          {/* Probability Bar Visualization */}
          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono font-semibold">
              <span className="text-emerald-400">P(Ham | Message) = {((result.p_ham ?? 0) * 100).toFixed(2)}%</span>
              <span className="text-rose-400">P(Spam | Message) = {((result.p_spam ?? 0) * 100).toFixed(2)}%</span>
            </div>

            <div className="w-full h-4 rounded-full bg-slate-900 border border-slate-800 overflow-hidden flex">
              <div
                style={{ width: `${(result.p_ham ?? 0) * 100}%` }}
                className="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 transition-all duration-500"
              />
              <div
                style={{ width: `${(result.p_spam ?? 0) * 100}%` }}
                className="h-full bg-gradient-to-r from-rose-400 to-rose-600 transition-all duration-500"
              />
            </div>
          </div>

          {/* Message Text Inspection */}
          <div className="bg-[#080d1a] border border-slate-800/80 rounded-xl p-4 font-mono text-xs space-y-1">
            <span className="text-slate-500 uppercase tracking-wider text-[10px]">ANALYZED TEXT:</span>
            <p className="text-slate-200 text-sm font-sans italic">
              "{result.original_message}"
            </p>
          </div>

          {/* Model Transparency Disclaimer */}
          <div className="flex items-start space-x-2.5 text-xs text-slate-400 bg-slate-900/40 p-3.5 rounded-xl border border-slate-800/60">
            <Info className="w-4 h-4 text-indigo-400 flex-shrink-0 mt-0.5" />
            <p className="leading-relaxed">
              <strong>Probabilistic Notice:</strong> {result.explanation}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
