# Civic Hack DC 2025 - Project Archive

This directory contains all projects submitted during the hackathon. Each project has its own subdirectory with code snapshots, documentation, and resources.

## 📁 Project Structure

Each team's project should be organized as follows:

```text
projects/team-name/
├── README.md           # Project overview
├── snapshot/          # Code snapshot from hackathon submission
├── data/             # Sample data files (if applicable)
├── docs/             # Additional documentation
└── upstream/         # Git submodule pointing to active repo (optional)
```

## 📋 Submitted Projects

| Track | Team Name | Description |
|---|---|---|
| **Campaign Detection** | [**CanOfSpam**](./canOfSpam/README.md) | A data analysis tool for detecting fraudulent bot comments in federal regulatory rule dockets using temporal patterns, submission metadata, and content analysis. Identifies coordinated manipulation campaigns through statistical analysis of comment timing bursts and duplicate detection. Built with Python and Marimo notebooks. |
| **Cross-Docket Analysis & Influence Mapping** | [**Within Docket Dataset**](./within-docket-dataset/README.md) | Links public comments to specific regulatory documents they respond to within a single docket, using metadata analysis, time-window heuristics, and semantic similarity techniques. Helps understand how public comments influence changes from proposed rules to final rules. |
| **Data Accessibility** | [**Hive-partitioned Parquet**](./hive-partitioned-parquet/README.md) | Transforms regulatory data into Hive-partitioned Parquet files for fast and efficient queries using DuckDB. Enables direct querying from S3 with better performance for large-scale regulatory data analysis. |
|  | [**Mirrulations CLI**](./mirrulations-cli/README.md) | Published Python package incorporating scripts from Prof. Ben Coleman to make downloading regulatory data more accessible. Easy to install via pip or use with uvx for streamlined access to Mirrulations data. |
| | [**LLM.gov (CMS Docket Assistant)**](./llmgov/README.md) | An LLM wrapper that utilizes RAG queries to answer general questions about dockets. Transforms complex JSON text into machine-readable vector embeddings stored in S3, enabling semantic search and providing a simple chat interface for non-technical users. |
| **Data Quality & Derived Layers** | [**Taskmasters**](./taskmasters/README.md) | Extracts data from different document types (PDFs, images, documents) while implementing keyword extraction on comments. Converts JSON files to parquet format using AWS S3, Glue, and Athena services for improved data processing efficiency. |
|   | [**Team Velogear**](./team-velogear/README.md) | A command-line tool written in Go that parses text from PDF files and outputs to CSV, JSON, and Parquet formats. Uses pdftotext from poppler-utils for better accessibility of regulatory documents. |
| **Docket-Level Analysis / Topic & Sentiment** | [**Rules Talk**](./rules-talk/README.md) | Policy Comment Analyzer leveraging Google Gemini API to automate analysis of public comments on policy proposals. Extracts key policy information, analyzes comments for specific issues and sentiment, and generates comprehensive reports showing how organizations' critiques and support fit in the conversation. |
| **Entity Resolution** | [**Entity Resolution Team**](./entity-resolution-team/README.md) | Extracts and cleans organization information from comments to group submissions together, even when organization names weren't explicitly listed or had inconsistent naming conventions. Used Jupyter Notebooks for analysis. |
| **External Agency Scraping** | [**The Scrapers**](./the-scrapers/README.md) | Created basic code to scrape other government websites (FCC and SEC) and documented the challenges one may face. Focuses on different scraping methodologies for accessing government data sources. |
| **Regulatory Document Discovery** | [**USPF1**](./uspf1/README.md) | FDA Docket Classification System addressing "Docket Blindness" by automatically analyzing FDA docket comments and generating tags indicating what type of information is needed (Scientific/Technical, Policy/Regulatory, Procedural, etc.). |
| | [**Expanded Search**](./expanded-search/README.md) | A comprehensive search platform that enables citizens to discover relevant regulatory dockets based on their interests. Features Python backend with spaCy NLP keyword extraction, SQLite database, and Angular frontend with Material UI. *(Work in progress)* |
| **Topic & Sentiment Analysis** | [**Team Topic Modeling**](./team-topic-modeling/README.md) | Automated analysis of regulatory documents to identify regulated topics and extract meaningful keywords. Uses spaCy and RAKE for NLP processing, generates visualizations including bar charts and word clouds for each regulatory topic. |

---

### Highlighted Projects

- [Project Name](./team_slug/)
