# SenseLab — NLP Assignment 5: Word Sense Disambiguation

A Streamlit website for demonstrating Word Sense Disambiguation (WSD) with a small artificial dataset and a transparent Lesk-inspired lexical-overlap algorithm.

## Features
- Overview dashboard with assignment scope and key counts
- Interactive WSD Lab: enter a sentence, choose a target word, inspect candidate scores and matched words
- Sense inventory with downloadable `sense_inventory.csv`
- Lexical Relations Explorer: synonyms, hypernyms, and related cue words
- Evaluation table with reference labels, predictions, accuracy, and downloadable annotated results
- Short analysis report available in the app and as a downloadable text file
- High-contrast CSS styling designed to keep headings and body text readable

## Dataset and algorithm
The included mini-lexicon is artificially curated for this assignment. It covers `bank`, `bat`, `light`, `plant`, `crane`, and `apple`, with two senses per word and 12 sample sentences. The algorithm is inspired by the Lesk method: it compares content words in the sentence with each candidate sense's definition and lexical cues.

**Important:** The website uses a WordNet-style teaching lexicon, not the full NLTK WordNet corpus. The report explains how to extend it to real WordNet. Accuracy is only illustrative on the small synthetic dataset.

## Run in VS Code
1. Extract the ZIP folder.
2. Open the extracted `NLP_Assignment_5_WSD` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment (recommended):
   - Windows: `python -m venv .venv`
   - Activate: `.venv\Scripts\activate`
5. Install dependencies:
   `pip install -r requirements.txt`
6. Start the website:
   `streamlit run app.py`
7. The local website opens in your browser. If it does not, open the `Local URL` printed in the terminal (usually `http://localhost:8501`).

## Files
- `app.py` — complete website and WSD logic
- `requirements.txt` — Python dependencies
- `data/sample_sentences.csv` — labeled artificial sample data
- `data/sense_inventory.csv` — sense inventory and lexical relations
- `analysis_report.txt` — short analysis report
- `DATA_DICTIONARY.md` — field descriptions
