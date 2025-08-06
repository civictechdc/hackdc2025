# Civic Hack DC 2025: Final Hackathon Judging Analysis

## Overview

Civic Hack DC 2025 brought together developers, data scientists, and policy experts to tackle pressing challenges in regulatory comment analysis. This analysis summarizes final judging outcomes, project scores, cross-cutting insights, and recommendations for future hackathons.

## Top-Ranked Projects (Weighted Score ≥ ~3.0) by Alphabetical Order

### **Can of Spam**

* **Breakdown**: Median Scores: Impact 4, Novelty 3, Amplification 3, Open Source 3, Usability 3, Continuity 3
* **Highlights**: Built a proof-of-concept for duplicate and bot comment detection, laying groundwork for campaign analysis.

### **Hive-Partitioned Parquet**

* **Breakdown**: Median Scores: Impact 4.5, Novelty 4, Amplification 4, Open Source 4, Usability 3, Continuity 3.5
* **Highlights**: Converted Mirrulations JSON to Hive-partitioned Parquet, enabling efficient SQL querying for large datasets.

### **LLM.gov**

* **Breakdown**: Median Scores: Impact 5, Novelty 4, Amplification 4, Open Source 4, Usability 4, Continuity 4
* **Highlights**: Combined Retrieval-Augmented Generation (RAG) with vector embeddings for semantic search and summarization. Well-documented and highly impactful.

### **Mirrulations-CLI**

* **Breakdown**: Median Scores: Impact 5, Novelty 3.5, Amplification 5, Open Source 5, Usability 4.5, Continuity 4
* **Highlights**: Packaged Mirrulations fetch and CSV tools into a polished CLI for easy installation and use, greatly improving accessibility.

### **Rules-Talk**

* **Breakdown**: Median Scores: Impact 4, Novelty 4, Amplification 4.25, Open Source 3.25, Usability 4, Continuity 3.5
* **Highlights**: Used LLMs to cluster sentiment and topics in public comments, making regulatory feedback more digestible for non-technical stakeholders.

### **The Scrapers**

* **Breakdown**: Median Scores: Impact 4.5, Novelty 3.5, Amplification 3.75, Open Source 3, Usability 3, Continuity 3.25
* **Highlights**: Developed FCC and SEC scraping workflows, expanding the Mirrulations dataset beyond Regulations.gov.

### **Within-Docket Dataset**

* **Breakdown**: Median Scores: Impact 4, Novelty 3, Amplification 4, Open Source 3, Usability 2, Continuity 3
* **Highlights**: Created a conceptual pipeline for mapping comment influence on regulatory changes.

## Judges

* **Judge 1**: [Ben Coleman](https://www.linkedin.com/in/moraviancoleman/)
Ben is a Professor of Computer Science at Moravian University with expertise in Software Engineering and Computer Science Education. He serves as the primary maintainer of the Mirrulations project, and has lead it's development. [Their Evaluation](submissions/coleman.md)

* **Judge 2**: [Fred Trotter](https://www.linkedin.com/in/fredtrotter/)
Fred is a Healthcare Data Technologist at the Centers for Medicare & Medicaid Services (CMS) Digital Service team, with extensive experience in healthcare informatics, data journalism, and cybersecurity. He collaborated with Ben Colman to explore the regulatory comment data space that forms the foundation of this hackathon. [Their Evaluation](submissions/ftrotter.md)

* **Judge 3**: [Evan Tung](https://www.linkedin.com/in/ejtung/)
Evan is a Software Development Engineer at Amazon Web Services (AWS) and organizer at Civic Tech DC, where he coordinates biweekly project nights and connects volunteer civic hackers to local government and nonprofit projects. [Their Evaluation](submissions/evan_tung.md)

* **Judge 4**: [Gautami Nadkarni](https://www.linkedin.com/in/gautaminadkarni/)
Gautami is a Senior Customer Engineer at Google Cloud with 7+ years of experience in cloud architecture and data strategy. She specializes in AI/ML solutions, data analytics, and helping Fortune 500 enterprises with cloud modernization and AI implementation. [Their Evaluation](submissions/gautami_nadkarni.md)

* **Judge 5**: [Santhosh kumar Veeramalla](https://www.linkedin.com/in/santhoshk499/)
Santhosh is a Senior Scala Developer at Optum with 9+ years of experience building large-scale data platforms, real-time streaming pipelines, and cloud-native solutions. He specializes in Apache Spark, Databricks, and data engineering across Azure, AWS, and GCP environments. [Their Evaluation](submissions/kumar_veeramalla.md)

* **Judge 6**: [Melanie Kourbage](https://www.linkedin.com/in/melanie-kourbage-48769044/)
Melanie is a Lead Specialist in Informatics at the Association of Public Health Laboratories (APHL) with 20+ years of experience in public health informatics project management, policy development, and system implementation. She specializes in informatics standards, technical assistance, and coordinating national public health initiatives across federal, state, and local organizations. [Their Evaluation](submissions/melanie_kourbage.md)

* **Judge 7**: [Taylor Wilson](https://www.linkedin.com/in/taylorjameswilson/)
Taylor is Vice President of Applied Statistics and Data Science at Reveal Global Consulting, where he leads a team delivering AI/ML solutions to federal clients. He has extensive experience across multiple government agencies including the U.S. Census Bureau, Consumer Product Safety Commission, and Bureau of Labor Statistics. Taylor also runs DataKind DC, a partner organization of Civic Tech DC, and a partner for Civic Hack DC 2025. [Their Evaluation](submissions/taylor_wilson.md)

* **Judge 8**: [Michael Deeb](https://www.linkedin.com/in/michael-deeb//)
Michael is a Principal Consultant with TealWolf Consulting and CTO with 15+ years of experience in AI, digital transformation, and systems architecture. He serves as Director & Board Member of Civic Tech DC and is the Founder & CTO of Keeplist.io. He specializes in AI strategy, civic technology, and complex problem solving across government and nonprofit sectors. [Their Evaluation](submissions/deeb.md)

## Cross-Cutting Insights

### What Judges Valued Most

* **Practical Impact Over Innovation**: Usable tools with immediate value outscored technically complex prototypes.
* **Documentation Quality**: Repeatedly highlighted as a differentiator for high-scoring projects.
* **Ecosystem Integration**: Projects leveraging Mirrulations and other existing tools scored higher.
* **Usability for Non-Technical Users: Critical for real-world adoption.**

### Common Failure Patterns

* **Poor Documentation**: The most consistent critique.
* **Overuse of Jupyter Notebooks**: Docked for lacking production readiness.
* **Scope Mismatch**: Ambitious projects often failed to deliver complete prototypes.
* **Isolation**: Standalone tools without ecosystem integration scored lower.

### Technical Trends

* **AI/LLM Applications** dominated top-scoring entries.
* **Data Infrastructure** (Parquet, vectorization) recognized as foundational.
* **Multi-format Processing** appreciated for comprehensive data coverage.

### Judge Consistency Analysis

* **Most Aligned**: Infrastructure and practical utility projects.
* **Most Divergent**: NLP/topic modeling projects.
* **Consensus**: Documentation, ecosystem integration, and usability.

## Methodology Notes

* **Data Sources**: 8 judge evaluation forms submitted between 2025-08-01 and 2025-08-05

* **Project Name Standardization**: Some judges used different names for the same projects:

llmgov = "CMS Docket Assistant"
rules-talk = "Talk to me in Rules"
taskmasters = "Data Quality & Derived Layers"
the-scrapers = "FCC & SEC Web Scraping"

* **Weighted Scoring Formula**: (Impact×0.2 + Novelty×0.2 + Amplification×0.15 + OpenSource×0.15 + Usability×0.15 + Continuity×0.15) × 20

## Recommendations for Future Events

### For Organizers

* **Emphasize Documentation**: Create README templates.
* **Technical Review**: Do lightweight code reviews mid-day.
* **Data & Infrastructure Prep**: Make sure to have data and infrastructure ready to go immediately.

### For Participants

* **Start with Documentation**: Write README first, code second.
* **Focus on Integrations**: Build on existing tools for greater impact, don't reinvent the wheel.
* **Prepare Demos**: Clear basic, user-friendly demos improve scoring.
* **Aim for Production Readiness**: Extract your code into discrete files to refrence from your notebook.
