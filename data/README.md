# SMS Spam Collection Dataset

## Dataset Overview

The **SMS Spam Collection** is a public set of SMS tagged messages that have been collected for SMS Spam research. It contains one set of SMS messages in English of 5,574 messages, tagged according to being `ham` (legitimate) or `spam`.

- **Repository**: UCI Machine Learning Repository
- **Dataset ID**: 228
- **URL**: [https://archive.ics.uci.edu/dataset/228/sms+spam+collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
- **Direct Archive**: `https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip`

## Citation

```bibtex
@misc{sms_spam_collection_228,
  author       = {Almeida, Tiago and Hidalgo, José},
  title        = {{SMS Spam Collection}},
  year         = {2011},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C5CC84}
}
```

## Schema

The raw dataset is stored in a tab-separated text format (`SMSSpamCollection`):
- Column 1: `label` (`ham` or `spam`)
- Column 2: `message` (SMS text)

## Acquisition and Preprocessing Pipeline

The project's `src/data_loader.py` manages dataset acquisition:
1. **UCI API Attempt**: It first calls `ucimlrepo.fetch_ucirepo(id=228)`.
2. **Robust Fallback**: If the UCI package reports that ID 228 is not directly importable via their client API, `data_loader.py` automatically downloads the official zip archive directly from the UCI ML Repository archive endpoint (`https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip`) and extracts `SMSSpamCollection` into this `data/` directory.
3. **Local Cache**: If `data/SMSSpamCollection` is already present locally, it is loaded without redownloading.
4. **Data Cleaning**:
   - Original records: 5,574
   - Missing values: 0
   - Duplicate messages identified and removed: 403
   - Cleaned records: 5,171 (4,518 Ham, 653 Spam)
   - Labels normalized to binary indicator `label_num` (Spam = 1, Ham = 0).
