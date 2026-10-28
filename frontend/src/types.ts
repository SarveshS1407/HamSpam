export interface DatasetStats {
  dataset_name: string;
  raw_total: number;
  cleaned_total: number;
  duplicates_removed: number;
  missing_values: number;
  ham_count: number;
  spam_count: number;
  p_ham: number;
  p_spam: number;
  bernoulli: {
    p: number;
    q: number;
    expectation_E_Y: number;
    variance_Var_Y: number;
    std_dev_sigma_Y: number;
  };
}

export interface WordProbability {
  word: string;
  total_messages_with_word: number;
  spam_messages: number;
  ham_messages: number;
  p_word_given_spam: number;
  p_word_given_ham: number;
  p_word: number;
  p_spam_given_word_direct: number;
  p_spam_given_word_bayes: number;
  p_ham_given_word: number;
  bayes_direct_diff: number;
  bayes_verified: boolean;
}

export interface WordProbabilitiesResponse {
  matching_mode: string;
  tolerance: number;
  words: WordProbability[];
}

export interface ModelEvaluation {
  model_type: string;
  vectorizer: string;
  test_size_ratio: number;
  train_size: number;
  test_size: number;
  test_distribution: {
    ham_count: number;
    spam_count: number;
    ham_proportion: number;
    spam_proportion: number;
  };
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
  };
  confusion_matrix: {
    tn: number;
    fp: number;
    fn: number;
    tp: number;
    descriptions: {
      tn: string;
      tp: string;
      fp: string;
      fn: string;
    };
  };
  imbalance_insight: string;
}

export interface PredictionResult {
  original_message: string;
  is_valid: boolean;
  predicted_label: string;
  predicted_class: number | null;
  p_ham: number | null;
  p_spam: number | null;
  visual_indicator: string;
  explanation: string;
}

export interface DatasetSample {
  id: number;
  label: 'ham' | 'spam';
  message: string;
  length: number;
  words: number;
}

export interface LengthDistributionBin {
  bin: string;
  ham: number;
  spam: number;
  ham_pct: number;
  spam_pct: number;
}

export interface DatasetMeta {
  overview: {
    name: string;
    uci_id: number;
    uci_url: string;
    doi: string;
    authors: string;
    license: string;
    citation: string;
    raw_count: number;
    cleaned_count: number;
    duplicates_pruned: number;
    missing_values: number;
    ham_count: number;
    ham_pct: number;
    spam_count: number;
    spam_pct: number;
    format: string;
    columns: Array<{
      name: string;
      type: string;
      values: string;
      description: string;
    }>;
  };
  length_stats: {
    ham: {
      mean_chars: number;
      median_chars: number;
      max_chars: number;
      mean_words: number;
      median_words: number;
      max_words: number;
    };
    spam: {
      mean_chars: number;
      median_chars: number;
      max_chars: number;
      mean_words: number;
      median_words: number;
      max_words: number;
    };
    distribution: LengthDistributionBin[];
  };
  samples: {
    ham: DatasetSample[];
    spam: DatasetSample[];
  };
}
