# GtechX - Automatic MCQ Generator

An AI-powered web application that automatically generates Multiple Choice Questions (MCQs) from any given text using NLP techniques.

## Features

- Generate MCQs from full text or auto-generated summary
- Uses WordNet and ConceptNet for intelligent distractor (wrong option) generation
- TF-IDF based text summarization with configurable threshold (HANDICAP = 0.85)
- Keyword extraction using MultipartiteRank algorithm (extracts top 15 proper nouns)
- Web-based interface with real-time question generation
- Console output showing step-by-step progress

## How It Works

### Pipeline Overview

```
Input Text → Keyword Extraction → Sentence Filtering → Word Sense Disambiguation → Distractor Generation → MCQ Output
```

### Processing Steps (logged to console)

1. **Extracting Keywords** - MultipartiteRank extracts proper nouns from text
2. **Summary Generation** (if summary mode) - TF-IDF selects important sentences
3. **Selecting Sentences** - Maps keywords to sentences containing them
4. **Filtering Sentences** - Sorts by length, longest first
5. **Word Sense Disambiguation** - PyWSD finds best meaning for each keyword
6. **Distractor Generation** - WordNet/ConceptNet provide wrong options
7. **JSON Response** - Creates `response.json` and returns to frontend

### Core Modules

| Module | Purpose |
|--------|---------|
| `main.py` | Flask web server with `/` and `/result/` endpoints |
| `extract_keywords.py` | Extracts proper nouns using PKE's MultipartiteRank |
| `generate_summary.py` | TF-IDF based extractive summarization |
| `find_sentances.py` | Maps keywords to relevant sentences using FlashText |
| `gen_mcq.py` | Generates distractors via WordNet/ConceptNet APIs |

### Distractor Generation Strategy

1. **WordNet** (primary): Finds hypernyms (parent categories) then retrieves hyponyms (sibling concepts)
2. **ConceptNet** (fallback): Uses PartOf relations via REST API when WordNet returns <4 distractors
3. **Word Sense Disambiguation**: Uses PyWSD's `max_similarity` (Wu-Palmer similarity) and `adapted_lesk` for accurate sense selection

## Installation

```bash
# Clone repository
git clone <repo-url>
cd GtechX-main

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### NLTK Data (auto-downloaded on first run)

The following NLTK resources are downloaded automatically:
- `wordnet` - Lexical database
- `omw-1.4` - Open Multilingual WordNet
- `punkt` - Sentence tokenizer
- `averaged_perceptron_tagger` - POS tagger
- `stopwords` - Common stopwords

Pre-downloaded copies are included in `nltk_data/` folder.

## Usage

```bash
python main.py
```

Open `http://localhost:5000` in your browser.

### Input Requirements
- Minimum 200 words
- Choose "Full Text" or "Summary" mode

### Modes

| Mode | Description |
|------|-------------|
| **Full Text** (`num=1`) | Extracts keywords from entire text, generates more MCQs |
| **Summary** (`num=0`) | First summarizes text via TF-IDF, then extracts keywords only from summary |

## Dependencies

```
pke-tool          # Keyphrase extraction (MultipartiteRank)
nltk              # NLP toolkit (WordNet, tokenization, POS tagging)
pandas            # Data handling, JSON export
sklearn           # TF-IDF vectorization
Flask             # Web framework
requests          # ConceptNet API calls
pywsd             # Word sense disambiguation
flashtext         # Fast keyword matching in sentences
spacy             # NLP processing (required by PKE)
spacy-legacy      # spaCy compatibility
spacy-loggers     # spaCy logging
```

## Project Structure

```
GtechX-main/
├── main.py              # Flask application entry point
├── gen_mcq.py           # MCQ generation with WordNet/ConceptNet
├── generate_summary.py  # TF-IDF summarization (HANDICAP=0.85)
├── extract_keywords.py  # Keyword extraction (MultipartiteRank, top 15)
├── find_sentances.py    # Sentence-keyword mapping (FlashText)
├── requirements.txt     # Python dependencies
├── response.json        # Generated at runtime with MCQ data
├── templates/
│   └── index.html       # Web interface (jQuery 1.9.1)
├── static/
│   ├── script.js        # AJAX handling & UI logic
│   ├── style.css        # SeaGreen themed styling
│   └── logo.png         # Logo
└── nltk_data/           # Pre-downloaded NLTK resources
    ├── tokenizers/punkt/
    ├── taggers/averaged_perceptron_tagger/
    └── corpora/wordnet/, stopwords/
```

## API

### GET /

Returns the main HTML page (`index.html`).

### POST /result/

**Request (form data):**
```
paragraph: <text content>
num: "1" (full text) | "0" (summary)
```

**Response:** JSON array of MCQ objects
```json
[
  {
    "question": "______ is the capital of France.",
    "options": ["Paris", "London", "Berlin", "Madrid"],
    "extras": ["Rome", "Vienna"],
    "answer": "Paris"
  }
]
```

| Field | Description |
|-------|-------------|
| `question` | Sentence with keyword replaced by `______` |
| `options` | Top 4 shuffled choices (includes correct answer) |
| `extras` | Additional distractors (positions 5-8) |
| `answer` | Correct answer (the original keyword, capitalized) |

## Configuration

### Summarization Threshold

In `generate_summary.py`:
```python
HANDICAP = 0.85  # Lower = more sentences included in summary
```

### Keyword Count

In `extract_keywords.py`:
```python
keyphrases = extractor.get_n_best(n=15)  # Max keywords to extract
```

### ConceptNet API Limits

In `gen_mcq.py`:
```python
limit=5   # Categories to fetch
limit=10  # Words per category
```

## Alternative Summarizer (Commented)

`generate_summary.py` contains a commented XLNet transformer-based summarizer:
```python
# from summarizer import TransformerSummarizer
# model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
```
Requires: `pip install bert-extractive-summarizer`

## Limitations

- Requires minimum 200 words input
- Works best with factual/educational content containing proper nouns
- ConceptNet API calls require internet and may slow down generation
- Some generated MCQs may need manual review (noted in console output)
- `response.json` is overwritten on each request

## License

Made with ❤️ by Rakesh
