# Regulatory Comment Linkage

**Team:** Within Docket Dataset  
**Hackathon:** Civic Hack DC 2025  
**Challenge:** Cross-Docket Commenter Threads, Influence Mapping & Feedback Loops

## 🎯 Project Overview

This project links public comments to specific regulatory documents they respond to within a single docket, using metadata analysis, time-window heuristics, and semantic similarity techniques. The goal is to understand how public comments influence changes from proposed rules to final rules.

**Description:**
Check out the full [project readme](./upstream/README.md) for more details.

## 💡 Solution Approach

The system processes regulatory dockets to:

- Create an inventory of all documents with metadata and timestamps
- Preprocess public comments and establish time-based linking windows
- Extract text from regulatory documents and isolate relevant sections
- Match comments to document sections using n-gram analysis and semantic similarity
- Identify which comments influenced specific rule changes

## 🚀 Repository

**GitHub:** [SriInsights/DC-Hackathon-2025](https://github.com/SriInsights/DC-Hackathon-2025)

## 🛠️ Key Technologies

- **NLP Processing:** Text extraction, n-gram matching, semantic analysis
- **Data Processing:** Pandas for time-window binning and document matching
- **Text Analysis:** Comment-to-rule section mapping

## 📊 Data Pipeline

1. **Document Inventory** - Catalog all docket documents with metadata
2. **Time-Window Matching** - Link comments to documents using temporal analysis
3. **Text Extraction** - Process regulatory documents for plain text
4. **Semantic Matching** - Match comments to specific document sections

## 🔮 Future Development

- Enhanced validation for edge cases
- Advanced topic modeling and sentiment analysis
- Interactive dashboard for policymakers and researchers
- Comment impact scoring and demographic analysis

## 🤝 Team Members

- **Henry Ham**
- **Kumar H**
- **Queyen Le**
- **Sridhar Gundumalla**
- **Srishti Kama**
