"""
Dataset Acquisition, Cleaning, and Preprocessing Module for HamSpam.

Retrieves the SMS Spam Collection dataset from the UCI Machine Learning Repository,
handles API availability fallbacks, audits duplicates/missing values, and normalizes
labels for probabilistic and statistical modeling.
"""

import csv
import io
import os
import urllib.request
import zipfile
from typing import Dict, Optional, Tuple

import pandas as pd

UCI_DATASET_ID = 228
UCI_ARCHIVE_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DEFAULT_LOCAL_PATH = os.path.join(DEFAULT_DATA_DIR, "SMSSpamCollection")


def fetch_raw_dataset(
    local_path: str = DEFAULT_LOCAL_PATH,
    force_download: bool = False,
) -> pd.DataFrame:
    """
    Fetch the raw SMS Spam Collection dataset from UCI repository.

    Attempts retrieval via `ucimlrepo` first. If unavailable through that API endpoint,
    falls back to downloading the official zip archive directly from the UCI archive URL,
    or reading an existing local copy.

    Parameters
    ----------
    local_path : str
        Path where local copy is stored or will be cached.
    force_download : bool
        If True, ignore local cache and redownload.

    Returns
    -------
    pd.DataFrame
        Raw dataset with columns ['label', 'message'].
    """
    # 1. Check local cache first if not forcing download
    if not force_download and os.path.exists(local_path):
        print(f"[DataLoader] Found cached dataset locally at: {local_path}")
        return _read_tsv_sms(local_path)

    # 2. Attempt download via ucimlrepo
    print("[DataLoader] Attempting dataset retrieval via ucimlrepo (id=228)...")
    try:
        from ucimlrepo import fetch_ucirepo

        dataset = fetch_ucirepo(id=UCI_DATASET_ID)
        if dataset and hasattr(dataset, "data") and dataset.data is not None:
            features = dataset.data.features
            targets = dataset.data.targets
            if features is not None and targets is not None:
                # Merge into normalized schema
                df = pd.DataFrame()
                target_col = targets.columns[0]
                feature_col = features.columns[0]
                df["label"] = targets[target_col].astype(str).str.strip().str.lower()
                df["message"] = features[feature_col].astype(str)
                print(f"[DataLoader] Successfully loaded via ucimlrepo ({len(df)} records).")
                _cache_dataframe(df, local_path)
                return df
    except Exception as exc:
        print(f"[DataLoader] ucimlrepo notification: {exc}")
        print("[DataLoader] Proceeding to official UCI archive direct download fallback...")

    # 3. Fallback: Download official zip archive from UCI repository
    print(f"[DataLoader] Downloading official UCI archive from: {UCI_ARCHIVE_URL}")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        req = urllib.request.Request(
            UCI_ARCHIVE_URL,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) HamSpam/1.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                if "SMSSpamCollection" in z.namelist():
                    extracted_bytes = z.read("SMSSpamCollection")
                    with open(local_path, "wb") as f_out:
                        f_out.write(extracted_bytes)
                    print(f"[DataLoader] Saved official dataset to {local_path}")
                    return _read_tsv_sms(local_path)
                else:
                    raise FileNotFoundError(
                        f"Expected 'SMSSpamCollection' in zip archive, found: {z.namelist()}"
                    )
    except Exception as exc:
        if os.path.exists(local_path):
            print(f"[DataLoader] Download failed ({exc}). Falling back to existing local copy.")
            return _read_tsv_sms(local_path)
        raise RuntimeError(
            f"Failed to acquire dataset from UCI repository ({exc}). "
            f"Please place 'SMSSpamCollection' manually in '{os.path.dirname(local_path)}'."
        ) from exc


def _read_tsv_sms(filepath: str) -> pd.DataFrame:
    """
    Read the raw TSV SMS file using csv.QUOTE_NONE to preserve all 5,574 lines.
    """
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        df = pd.read_csv(
            f,
            sep="\t",
            names=["label", "message"],
            header=None,
            quoting=csv.QUOTE_NONE,
            dtype={"label": str, "message": str},
        )
    # Strip whitespace from labels and ensure lowercase
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["message"] = df["message"].astype(str)
    return df


def _cache_dataframe(df: pd.DataFrame, filepath: str) -> None:
    """Cache the dataframe to a local TSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, sep="\t", index=False, header=False, quoting=csv.QUOTE_NONE)


def clean_dataset(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Perform rigorous data cleaning on the SMS dataset.

    Steps:
    1. Inspect missing values across 'label' and 'message'.
    2. Drop missing rows if any exist.
    3. Remove duplicate messages.
    4. Normalize labels: spam -> 1, ham -> 0.
    5. Validate cleaned dataset.

    Parameters
    ----------
    df_raw : pd.DataFrame
        Raw dataframe containing 'label' and 'message'.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, int]]
        Cleaned dataframe and cleaning metrics dictionary.
    """
    raw_count = len(df_raw)
    missing_label = int(df_raw["label"].isna().sum())
    missing_message = int(df_raw["message"].isna().sum())

    # Filter out any null or empty entries if present
    df = df_raw.dropna(subset=["label", "message"]).copy()

    # Document duplicates
    duplicate_count = int(df.duplicated(subset=["message"]).sum())
    df_clean = df.drop_duplicates(subset=["message"]).copy().reset_index(drop=True)

    # Normalize labels: spam = 1, ham = 0
    df_clean["label_num"] = df_clean["label"].map({"ham": 0, "spam": 1}).astype(int)

    # Validation
    cleaned_count = len(df_clean)
    ham_count = int((df_clean["label_num"] == 0).sum())
    spam_count = int((df_clean["label_num"] == 1).sum())

    if cleaned_count != (ham_count + spam_count):
        raise ValueError(
            f"Validation error: Cleaned count {cleaned_count} != Ham ({ham_count}) + Spam ({spam_count})"
        )

    stats = {
        "raw_total": raw_count,
        "missing_label": missing_label,
        "missing_message": missing_message,
        "duplicates_removed": duplicate_count,
        "cleaned_total": cleaned_count,
        "ham_count": ham_count,
        "spam_count": spam_count,
    }

    return df_clean, stats


def load_and_preprocess(
    local_path: str = DEFAULT_LOCAL_PATH,
    force_download: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, int]]:
    """
    High-level entrypoint: fetch raw dataset, clean it, and report statistics.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, Dict[str, int]]
        df_raw, df_cleaned, stats_dict
    """
    df_raw = fetch_raw_dataset(local_path=local_path, force_download=force_download)
    df_clean, stats = clean_dataset(df_raw)
    return df_raw, df_clean, stats


if __name__ == "__main__":
    raw_df, clean_df, report = load_and_preprocess()
    print("\n--- Data Preprocessing Report ---")
    for k, v in report.items():
        print(f"  {k:22}: {v}")
    print("\nCleaned Sample Head:")
    print(clean_df.head())
