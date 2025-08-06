# Civic Hack DC 2025 – Evaluation Submission

**Evaluator Name:** Michael Deeb

**Organization:** TealWolf Consulting

**Date:** 2025-08-06

---

## Project Scores

### Project: canOfSpam

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 3/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 3/5
* **Comments:** Solid proof-of-concept for detecting coordinated bot comments using temporal bursts and duplicate detection; high civic value, moderate novelty.

---

### Project: entity-resolution-team

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 3/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 3/5
* **Comments:** Provides a classical approach to grouping regulatory comments by inferred organization. Uses standard text-cleaning and matching techniques that work but are not groundbreaking. Code reproducible via notebook.

---

### Project: expanded-search

* **Impact & Relevance (20%):** 3/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 2/5
* **Open Source Practices (15%):** 3/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:** Solid start on a docket discovery tool with a FastAPI backend, SQLAlchemy/Alembic data layer, and Angular Material UI. Implementation is incomplete, limited NLP, and no live demo. Documentation and modular design are good foundations.

---

### Project: hive-partitioned-parquet

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 4/5
* **Amplification (15%):** 4/5
* **Open Source Practices (15%):** 4/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 3/5
* **Comments:** Converts Mirrulations JSON to Hive-partitioned Parquet, sharply reducing query costs and enabling SQL access via DuckDB. Documentation and notebooks are clear and reproducible, and the technique can scale across agencies. Novelty is high because it applies a lesser known aspect of data-lake patterns to make the data more accessible. The Amplification affect is high, as this is a foundational tool for the mirrulations ecosystem.

---

### Project: llmgov

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 4/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 3/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 3/5
* **Comments:** Makes CMS regulations searchable via a RAG chat interface backed by an AWS Bedrock embeddings pipeline. High civic value and user-friendly Streamlit UI; code is modular with a pyproject and clear docs. Innovation is moderate given many LLM-RAG examples, was impressed with how they approached the overall data, and their prompt. The use of AWS-specific services is a bit limiting with the S3 Vector Store, but ultimately that is not a limited factor to the overall re-use of the code. The amplification affect is moderate, creating an embedding structure could facilitate other types of analysis.

---

### Project: mirrulations-cli

* **Impact & Relevance (20%):** 5/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 2/5
* **Open Source Practices (15%):** 5/5
* **Usability & Design (15%):** 5/5
* **Continuity Potential (15%):** 5/5
* **Comments:** Packaging Mirrulations fetch and CSV utilities into a single, PyPI-distributed CLI markedly lowers the barrier to accessing regulatory data and should see quick adoption. Strong licensing, changelog, tests, and Click-based UX merit high marks. Low Novelty, but sometimes the small things are the most impactful. Limited amplification affect since this is more a tool to be used by others initially exploring this data, or accessing specific dockets.

---

### Project: rules-talk

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 3/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 3/5
* **Comments:** Leverages LLM (Gemini) to auto-outline policies and cluster comment issues with sentiment, delivering high-value insights for rule-makers. Clear JSON schemas, CLI, and docs aid reproducibility.

---

### Project: taskmasters

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:** Provides a practical pipeline to extract text from PDFs, DOCX, and images, then clean and convert to structured CSV/Parquet for faster analysis. Addresses the data-quality problem statement directly and could slot into other teams’ ETL workflows, but techniques are standard OCR/NLP without novel algorithms. Repo offers example scripts and requirements files yet lacks packaging, tests, or CI, so ease of reuse is limited. A CLI wrapper, cloud deployment instructions, and roadmap would improve usability and long-term sustainability.

---

### Project: team-topic-modeling

* **Impact & Relevance (20%):** 3/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 2/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:** Leverages standard NLP (spaCy, RAKE) to highlight regulatory topics and auto-generate visual insights; useful for quick exploratory analysis. Code runs but is single-file with hard-coded paths, minimal documentation.

---

### Project: team-velogear

* **Impact & Relevance (20%):** 3/5
* **Novelty (20%):** 1/5
* **Amplification (15%):** 2/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 2/5
* **Comments:** Simple Go CLI that leverages `pdftotext` to convert PDFs into CSV/JSON/Parquet, lowering barriers to analyzing regulatory documents. Clear README and functional code.

---

### Project: the-scrapers

* **Impact & Relevance (20%):** 5/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 4/5
* **Open Source Practices (15%):** 3/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 2/5
* **Comments:** Leverages official FCC API and a reusable CSS‐selector scraper to retrieve filings and documents; addresses the “external agency scraping” challenge directly; straightforward Python code that newcomers can run with minimal dependencies. Code lacks packaging, tests, and robust error handling; SEC scraping is still manual and incomplete; documentation needs expansion. Huge impact and amplification affects.

---

### Project: uspf1

* **Impact & Relevance (20%):** 3/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:** A LLM analysis pipeline that builds out some basic bones for doing more complicated analysis.

---

### Project: within-docket-dataset

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:** Links comments to rule documents within a docket using timestamp windows and basic text matching. Clear notebook showcases end-to-end pipeline and yields actionable insights for policymakers. Heuristics are sensible but not innovative. Strength lies in demonstrating a replicable analytic workflow that can be expanded with richer NLP.

---

## Overall Feedback
