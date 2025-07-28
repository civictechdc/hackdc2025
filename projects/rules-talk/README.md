# Talk to me in Rules

**Team:** Rules Talk  
**Hackathon:** Civic Hack DC 2025  
**Challenge:** Docket‑Level Analysis / Topic & Sentiment Analysis

## 🎯 Problem Statement

We are creating a Policy Comment Analyzer that leverages AI to automate the analysis of public comments on policy proposals. The system helps agencies better understand sentiment and issues within public comments by aggregating all comments related to a policy and breaking down talking points, linking them to specific issues and identifying sentiment.

## 💡 Solution

This project uses the Google Gemini API to:

1. **Outline policies**: Extract key information from HTML policy documents including policy name, summary, objectives, proposed actions, affected stakeholders, and estimated impact
2. **Analyze comments**: Process public comments to identify specific issues, their relation to policy sections, relevant excerpts, and sentiment
3. **Generate comprehensive reports**: Aggregate all identified issues, calculate overall sentiment for each issue, and list referencing comments with excerpts

Shows how organizations' critiques and support fit in the conversation, providing a comprehensive view of public sentiment on regulatory policies.

**Links:** [GitHub Repository](https://github.com/grubbjabari/talk-to-me-in-rules)

## 🛠️ Tech Stack

- **Backend:** Python 3.8+
- **AI/NLP:** Google Gemini API for intelligent analysis and sentiment analysis
- **Data Processing:** BeautifulSoup for HTML parsing, JSON schema validation
- **Environment:** python-dotenv for configuration management

## 🤝 Team Members

- **Brian Varrieur**
- **Jabari Grubb**
- **Lucas Gover**
- **Rajiv Sundar**
- **Justin Mezetin**
