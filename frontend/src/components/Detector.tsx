import React, { useState } from 'react';
import { predictSMS, inspectMessageTokens, TokenImpact } from '../api';
import { PredictionResult } from '../types';
import { 
  Send, 
  RotateCcw, 
  Sparkles, 
  ShieldAlert, 
  ShieldCheck, 
  AlertCircle,
  HelpCircle,
  Layers,
  ArrowRight,
  Info
} from 'lucide-react';

export const Detector: React.FC = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [tokens, setTokens] = useState<TokenImpact[]>([]);
  const [error, setError] = useState<string | null>(null);

  const sampleMessages = [
    {
      label: 'Prize Draw Spam',
      type: 'spam',
      text: 'Congratulations! You have won a free prize. Claim now.',
    },
    {
      label: 'Casual Lunch Ham',
      type: 'ham',
      text: 'Hey, are we meeting for lunch today?',
    },
    {
      label: 'Urgent Bank Alert',
      type: 'spam',
      text: 'URGENT! Your account requires verification. Call 0800123456 immediately to prevent suspension.',
    },
    {
      label: 'Academic Lecture Ham',
      type: 'ham',
      text: 'Can you please send me the lecture notes and syllabus for BAMAT207?',
    },
  ];

  const handlePredict = async (textToPredict?: string) => {
    const text = textToPredict !== undefined ? textToPredict : message;
    if (!text.trim()) {
      setError('Please enter a valid SMS message to classify.');
      setResult(null);
      setTokens([]);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const res = await predictSMS(text);
      setResult(res);
      const tokenAnalysis = inspectMessageTokens(text);
      setTokens(tokenAnalysis);
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
    setTokens([]);
    setError(null);
  };

  const wordCount = message.trim() ? message.trim().split(/\s+/).length : 0;
  const isSpam = result?.predicted_label?.toLowerCase() === 'spam';

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-emerald-700 dark:text-emerald-400 text-xs font-mono">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Real-Time Inference Console</span>
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          SMS Spam Classification Console
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
          Enter any SMS message to compute estimated posterior probabilities 
          <strong> P(Spam | Message)</strong> and <strong>P(Ham | Message)</strong> using the 
          trained <strong>Multinomial Naive Bayes</strong> classifier with Laplace smoothing (&alpha;=1.0).
        </p>
      </div>

      {/* Main Classifier Input Card */}
      <div className="bg-white dark:bg-[#0b1324] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6 transition-colors">
        {/* Text Area */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
            <span>INPUT SMS MESSAGE</span>
            <span>{message.length} chars · {wordCount} words</span>
          </div>

          <textarea
            value={message}
            onChange={(e) => {
              setMessage(e.target.value);
              if (error) setError(null);
            }}
            placeholder="Type or paste an SMS message here (e.g., 'Free entry in 2 a weekly competition to win £1,000 cash...')."
            rows={4}
            className="w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-700/80 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-sans text-sm sm:text-base resize-y transition-all"
          />
        </div>

        {/* Validation Error Banner */}
        {error && (
          <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/20 text-rose-700 dark:text-rose-300 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-500" />
            <span>{error}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => handlePredict()}
              disabled={loading}
              className="inline-flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-md shadow-indigo-600/25 active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Computing Posteriors...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Analyze Message</span>
                </>
              )}
            </button>

            {message && (
              <button
                onClick={handleReset}
                className="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 text-sm font-medium transition-all"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Reset</span>
              </button>
            )}
          </div>
        </div>

        {/* Preset Sample Buttons */}
        <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 space-y-2">
          <span className="text-xs font-mono text-slate-400 uppercase tracking-wider block">
            Or try a canonical test message:
          </span>
          <div className="flex flex-wrap gap-2">
            {sampleMessages.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => handleSampleClick(sample.text)}
                className={`inline-flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all border ${
                  sample.type === 'spam'
                    ? 'bg-rose-50 hover:bg-rose-100 dark:bg-rose-500/10 dark:hover:bg-rose-500/20 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-500/20'
                    : 'bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-500/10 dark:hover:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-500/20'
                }`}
              >
                <span className={`w-1.5 h-1.5 rounded-full ${sample.type === 'spam' ? 'bg-rose-500' : 'bg-emerald-500'}`} />
                <span>{sample.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Classification Result Card */}
      {result && result.is_valid && (
        <div
          className={`rounded-2xl p-6 sm:p-8 border shadow-lg space-y-6 transition-all animate-fadeIn ${
            isSpam
              ? 'bg-rose-50/80 dark:bg-[#160d16] border-rose-300 dark:border-rose-900/60'
              : 'bg-emerald-50/80 dark:bg-[#0c1815] border-emerald-300 dark:border-emerald-900/60'
          }`}
        >
          {/* Status Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800/60">
            <div className="flex items-center space-x-3">
              <div
                className={`w-12 h-12 rounded-xl flex items-center justify-center shadow-md ${
                  isSpam ? 'bg-rose-500 text-white' : 'bg-emerald-500 text-white'
                }`}
              >
                {isSpam ? <ShieldAlert className="w-6 h-6" /> : <ShieldCheck className="w-6 h-6" />}
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                    {isSpam ? 'Classified as SPAM' : 'Classified as HAM (Legitimate)'}
                  </h3>
                  <span
                    className={`text-[11px] font-mono uppercase px-2 py-0.5 rounded-full font-bold ${
                      isSpam
                        ? 'bg-rose-200 dark:bg-rose-500/20 text-rose-800 dark:text-rose-300'
                        : 'bg-emerald-200 dark:bg-emerald-500/20 text-emerald-800 dark:text-emerald-300'
                    }`}
                  >
                    Class {result.predicted_class}
                  </span>
                </div>
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                  {isSpam
                    ? 'Unsolicited commercial, smishing, or promotional message.'
                    : 'Personal, academic, or genuine operational correspondence.'}
                </p>
              </div>
            </div>

            {/* Confidence Score Pill */}
            <div className="text-right">
              <div className="text-2xl font-extrabold font-mono text-slate-900 dark:text-white">
                {isSpam
                  ? `${((result.p_spam || 0) * 100).toFixed(1)}%`
                  : `${((result.p_ham || 0) * 100).toFixed(1)}%`}
              </div>
              <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400 uppercase">
                Model Confidence
              </span>
            </div>
          </div>

          {/* Calibrated Probability Breakdown Bar */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-emerald-700 dark:text-emerald-400">
                P(Ham | Msg) = {((result.p_ham || 0) * 100).toFixed(2)}%
              </span>
              <span className="text-rose-700 dark:text-rose-400">
                P(Spam | Msg) = {((result.p_spam || 0) * 100).toFixed(2)}%
              </span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden flex shadow-inner">
              <div
                style={{ width: `${(result.p_ham || 0) * 100}%` }}
                className="bg-emerald-500 transition-all duration-500"
                title={`P(Ham) = ${((result.p_ham || 0) * 100).toFixed(2)}%`}
              />
              <div
                style={{ width: `${(result.p_spam || 0) * 100}%` }}
                className="bg-rose-500 transition-all duration-500"
                title={`P(Spam) = ${((result.p_spam || 0) * 100).toFixed(2)}%`}
              />
            </div>
          </div>

          {/* Mathematical Disclaimer */}
          <div className="p-3 rounded-xl bg-white/60 dark:bg-black/20 border border-slate-200 dark:border-slate-800/40 text-xs text-slate-600 dark:text-slate-400 space-y-1">
            <div className="flex items-center space-x-1.5 font-medium text-slate-800 dark:text-slate-300">
              <Info className="w-3.5 h-3.5 text-indigo-500" />
              <span>Statistical Meaning of the Probability Score:</span>
            </div>
            <p className="leading-relaxed">
              These percentages represent estimated class posteriors computed via Multinomial Naive Bayes using 
              empirical word frequencies and Laplace add-one smoothing (&alpha;=1.0) on the 5,171 cleaned UCI messages. 
              Under symmetric 0-1 loss, a message is flagged Spam if P(Spam | Msg) &ge; 0.50.
            </p>
          </div>

          {/* Token Analysis Impact Table */}
          {tokens.length > 0 && (
            <div className="space-y-3 pt-2">
              <div className="flex items-center space-x-2 text-xs font-mono uppercase text-slate-700 dark:text-slate-300 font-bold">
                <Layers className="w-3.5 h-3.5 text-indigo-500" />
                <span>Recognized Vocabulary Tokens & Log-Odds Impact:</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
                  <thead className="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 uppercase">
                    <tr>
                      <th className="p-2.5">Token</th>
                      <th className="p-2.5">In Vocabulary</th>
                      <th className="p-2.5">Spam Log-Prob</th>
                      <th className="p-2.5">Ham Log-Prob</th>
                      <th className="p-2.5">Log-Odds Impact</th>
                      <th className="p-2.5">Polarity Lean</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 dark:divide-slate-800 bg-white/70 dark:bg-slate-900/30">
                    {tokens.map((t, i) => (
                      <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                        <td className="p-2.5 font-bold text-slate-900 dark:text-white">{t.token}</td>
                        <td className="p-2.5 text-slate-500">
                          {t.inVocab ? <span className="text-emerald-600 dark:text-emerald-400">Yes</span> : <span className="text-slate-400">OOV (smoothed)</span>}
                        </td>
                        <td className="p-2.5 text-slate-600 dark:text-slate-400">{t.spamLogProb !== null ? t.spamLogProb : '—'}</td>
                        <td className="p-2.5 text-slate-600 dark:text-slate-400">{t.hamLogProb !== null ? t.hamLogProb : '—'}</td>
                        <td className="p-2.5 font-bold">
                          {t.logOdds !== null ? (
                            <span className={t.logOdds > 0 ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'}>
                              {t.logOdds > 0 ? `+${t.logOdds}` : t.logOdds}
                            </span>
                          ) : '0.000'}
                        </td>
                        <td className="p-2.5">
                          {t.lean === 'spam' && <span className="px-2 py-0.5 rounded bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-300 font-semibold">Pushes Spam</span>}
                          {t.lean === 'ham' && <span className="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 font-semibold">Pushes Ham</span>}
                          {t.lean === 'neutral' && <span className="text-slate-400">Neutral</span>}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
