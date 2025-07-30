# Summary of Regulated Topics, Keywords, and Visualization Insights

**Team:** Team Topic Modeling  
**Hackathon:** Civic Hack DC 2025  
**Challenge:** Topic & Sentiment Analysis

## 🎯 Problem Statement

Automated analysis of regulatory documents to identify topics that are regulated and extract meaningful keywords that describe regulations. The goal is to process legal documents and policy submissions to uncover regulatory focus areas and language trends.

**Description:**
Check out the full [project readme](./upstream/README.md) for more details.

## 💡 Solution

The project processes regulatory documents through an NLP pipeline:

1. **Regulatory Sentence Extraction**: Identifies sentences containing regulatory language using keywords like "shall", "must", "prohibited", "required", "mandated"
2. **Topic & Keyword Extraction**: Uses spaCy for topic identification through noun chunks and RAKE (Rapid Automatic Keyword Extraction) for keyword extraction
3. **Data Cleaning**: Filters out vague topics and stop words to focus on meaningful regulatory content
4. **Visualization**: Generates bar charts showing keyword counts per topic and word clouds for each regulatory topic
5. **Structured Output**: Converts results to pandas DataFrames for analysis and export

The system analyzes public comments, legal documents, and policy submissions to identify regulatory focus areas and language patterns.

**File:** [code.py](code.py)

## 🛠️ Tech Stack

- **Backend:** Python 3.x with NLP processing
- **NLP Processing:** spaCy (en_core_web_sm model), RAKE-NLTK for keyword extraction
- **Data Analysis:** pandas for data manipulation and cleaning
- **Visualization:** matplotlib, seaborn for charts, WordCloud for topic visualization
- **Text Processing:** NLTK for stopwords and text preprocessing
- **Development:** Jupyter/Spyder compatible with Variable Explorer integration

## 🤝 Team Members

- **AJ (Anaswar Jayakumar)**
