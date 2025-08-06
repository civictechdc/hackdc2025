# Civic Hack DC 2025: Final Hackathon Judging Analysis

## Overview

Civic Hack DC 2025 brought together developers, data scientists, and policy experts to tackle pressing challenges in regulatory comment analysis. This analysis summarizes final judging outcomes, project scores, cross-cutting insights, and recommendations for future hackathons. As this was not a compettivie hackathon, the judges were encouraged to score projects based on their potential for impact, novelty, and scalability.

We will be highlighting projects that reach a certain threshold of scores.

## Projects by Alphabetical Order

### **Can of Spam**

* **Breakdown**: Median Scores: Impact 4, Novelty 3, Amplification 3, Open Source 3, Usability 3, Continuity 3

| Judge | Comments |
|-------|----------|
| Ben Coleman | "Good potential for a dashboard showing unique vs. duplicate comments. Current approach (text hashing) is limited but addresses a core problem" |
| Gautami Nadkarni | "Documentation could be better, more technical capabilities would have been nice" |
| Fred Trotter | "Good stab at the problem!" |
| Santhosh Veeramalla | "The core idea is good, but approach needs significant changes to support large datasets" |
| Michael Deeb | "Solid proof-of-concept for detecting coordinated bot comments using temporal bursts and duplicate detection; high civic value, moderate novelty" |

* **Takeaway**: Built a proof-of-concept for duplicate and bot comment detection, laying groundwork for campaign analysis. Early but functional addressing a novel approach to the problem.

### **Entity Resolution Team**

* **Breakdown**: Median Scores: Impact 3.75, Novelty 2.25, Amplification 3, Open Source 2.5, Usability 2, Continuity 2.5

| Judge | Comments |
|-------|----------|
| Melanie Kourbage | "I see a lot of potential here. I would use this to compare against a list of our member organizations" |
| Gautami Nadkarni | "Poor documentation but good idea" |
| Ben Coleman | "Interesting approach to entity resolution by grouping commenters by email domain. Lacked documentation and supporting files" |
| Fred Trotter | "Regex is a perfect hackathon strategy: 80% and quick!" |
| Santhosh Veeramalla | "Lacks clear documentation, making it hard to understand and reuse" |
| Michael Deeb | "Provides a classical approach to grouping regulatory comments by inferred organization. Uses standard text-cleaning and matching techniques that work but are not groundbreaking. Code reproducible via notebook" |

* **Takeaway**: High policy value with practical applications, but only basic technical execution and documentation.

### **Expanded Search**

* **Breakdown**: Median Scores: Impact 4, Novelty 2, Amplification 2.5, Open Source 3.5, Usability 3, Continuity 3.5

| Judge | Comments |
|-------|----------|
| Gautami Nadkarni | "High quality code and implementation" |
| Santhosh Veeramalla | "Clear documentation, quality code but it is not fully ready" |
| Ben Coleman | "Not presented. Appeared to be a search front-end" |
| Michael Deeb | "Solid start on a docket discovery tool ... Implementation is incomplete, limited NLP, and no live demo. Documentation and modular design are good foundations" |

* **Status**: Incomplete evaluation due to not presenting at the event and being incomplete.

* **Takeaway**: An incomplete but promising search front-end for regulations.gov dockets with "High quality code and implementation."

### **Hive-Partitioned Parquet**

* **Breakdown**: Median Scores: Impact 4.5, Novelty 4, Amplification 4, Open Source 4, Usability 3, Continuity 3.5

| Judge | Comments |
|-------|----------|
| Fred Trotter | "Totally made me rethink how to use S3 as a database. Before it was a metaphor" |
| Ben Coleman | "The idea is incredibly valuable and has significant potential for the ecosystem; judge has already used ideas from it" |
| Santhosh Veeramalla | "The core idea is very solid and the use of parquet and Hive partitioning is smart and scalable approach" |
| Gautami Nadkarni | "Very well explained, of the best documentations and scripting" |
| Evan Tung | "The query speed against remote S3 was amazing. Well-written README for technical users, but difficult for non-technical audience" |
| Michael Deeb | "Converts Mirrulations JSON to Hive-partitioned Parquet, sharply reducing query costs and enabling SQL access via DuckDB. High novelty and amplification as a foundational tool for the mirrulations ecosystem" |

* **Takeaway**: Paradigm-shifting approach to data architecture that fundamentally changed how judges think about S3 usage.

### **LLM.gov**

* **Breakdown**: Median Scores: Impact 5, Novelty 4, Amplification 4, Open Source 4, Usability 4, Continuity 4

| Judge | Comments |
|-------|----------|
| Taylor Wilson | "Semantic search capability will supercharge the ability of users to interface with the content" |
| Ben Coleman | "Incredibly valuable RAG transformation process and vector embedding code that could be incorporated into the Mirrulations ETL" |
| Santhosh Veeramalla | "Leveraging RAG with LLM's and Vector embeddings in powerful and scalable approach" |
| Fred Trotter | "LLM that scales. Sign me up" |
| Evan Tung | "Very usable for non-technical users. RAG is a standard GenAI application, but implementation is good. CLI scripts could be easier to run" |
| Gautami Nadkarni | "Average idea, documentation could be better" |
| Michael Deeb | "Makes CMS regulations searchable via RAG chat interface with AWS Bedrock. High civic value and user-friendly Streamlit UI; modular code with clear docs. Innovation is moderate given many LLM-RAG examples" |

* **Takeaway**: Standard GenAI application, thoughtfully implemented, and a scalable RAG architecture.

### **Mirrulations-CLI**

* **Breakdown**: Median Scores: Impact 5, Novelty 3.5, Amplification 5, Open Source 5, Usability 4.5, Continuity 4

| Judge | Comments |
|-------|----------|
| Fred Trotter | "Another example of 'oh this is the right way to think about this'" |
| Gautami Nadkarni | "Excels in making a valuable but hard-to-access dataset easily usable...highly practical and user-friendly solution" |
| Santhosh Veeramalla | "Practical and developer friendly solution with strong real-world utility" |
| Taylor Wilson | "I really love a quick, useful utility that expands functionality of existing tools. We should highly value contributions like this" |
| Ben Coleman | "A wonderful extension of the pre-event work that makes core tools easier to use. Judge will incorporate this approach" |
| Michael Deeb | "PyPI-distributed CLI that markedly lowers the barrier to accessing regulatory data. Low novelty, but sometimes the small things are the most impactful" |

* **Takeaway**:  They Packaged Mirrulations fetch and CSV tools into a polished CLI. Universal recognition as the fundamental solution to data accessibility.

### **Rules-Talk**

* **Breakdown**: Median Scores: Impact 4, Novelty 4, Amplification 4.25, Open Source 3.25, Usability 4, Continuity 3.5

| Judge | Comments |
|-------|----------|
| Gautami Nadkarni | "Exceptional and timely application of AI to a critical government function...solution with high impact and strong novelty" |
| Melanie Kourbage | "Info on sentiment, flavor of comments, serves as a pulse check...The instructions for how to use the tool are very detailed" |
| Santhosh Veeramalla | "High impact use case as public comment analysis is often time-consuming process" |
| Taylor Wilson | "The interface really took this project to the next level...might be better to create known classification frameworks" |
| Ben Coleman | "Interesting approach using LLMs for sentiment analysis on HTM files, a new data source. Could be good for identifying patterns" |
| Michael Deeb | "Leverages LLM to auto-outline policies and cluster comment issues with sentiment, delivering high-value insights for rule-makers. Clear JSON schemas, CLI, and docs aid reproducibility" |

* **Takeaway**: Used LLMs to cluster sentiment and topics in public comments, making regulatory feedback more digestible for non-technical stakeholders. Good building blocks for a more sophisticated tool.

### **Taskmasters**

* **Breakdown**: Median Scores: Impact 3.5, Novelty 3, Amplification 3, Open Source 2.5, Usability 2.5, Continuity 3.25

| Judge | Comments |
|-------|----------|
| Gautami Nadkarni | "Robust and well-designed solution...highly impactful and usable tool with strong continuity potential" |
| Santhosh Veeramalla | "Handling pdf images, text files enhances data coverage" |
| Ben Coleman | "Interesting work on .docx files, a format not yet considered. Project was unfocused and lacked documentation" |
| Michael Deeb | "A cohesive pipeline to extract text from PDFs, DOCX, and images. Addresses data-quality problem directly but uses standard OCR/NLP techniques. Lacks packaging and tests" |

* **Takeaway**: A "Robust and well-designed solution" for processing multiple document formats, specifically DOCX and PDFs with images. Strong technical approach to multi-format processing, but suffered from unclear project organization and documentation.

### **Team Topic Modeling**

* **Breakdown**: Median Scores: Impact 3, Novelty 2, Amplification 2, Open Source 2, Usability 2, Continuity 2

| Judge | Comments |
|-------|----------|
| Gautami Nadkarni | "Exceptional and highly relevant application of NLP...demonstrates both strong novelty and a deep understanding of user needs" |
| Fred Trotter | "Basic spaCy analysis. Well done" |
| Ben Coleman | "Basic analysis with spaCy. Lacked documentation and novelty" |
| Santhosh Veeramalla | "No clear documentation. The code lacks clarity and structure" |
| Michael Deeb | "Leverages standard NLP (spaCy, RAKE) to highlight regulatory topics and auto-generate visual insights; useful for quick exploratory analysis. Code runs but is single-file with hard-coded paths, minimal documentation" |

* **Takeaway**: Basic technical approach, highly polarized scores, from "exceptional and highly relevant" to "lacked documentation and novelty," highlight the importance of presentation.

### **Team VeloGear**

* **Breakdown**: Median Scores: Impact 3, Novelty 1, Amplification 2, Open Source 3, Usability 3, Continuity 2

| Judge | Comments |
|-------|----------|
| Gautami Nadkarni | "Practical and well-executed utility...strong potential for integration into other projects" |
| Ben Coleman | "Well-presented project, but was a simple wrapper for a PDF tool and didn't integrate with or advance the Mirrulations ecosystem" |
| Michael Deeb | "Simple Go CLI that leverages `pdftotext` to convert PDFs into CSV/JSON/Parquet, lowering barriers to analyzing regulatory documents. Clear README and functional code" |

* **Takeaway**: Well-executed utility but limited in scope and lacked integration with the broader Mirrulations ecosystem, limited novelty.

### **The Scrapers**

* **Breakdown**: Median Scores: Impact 4.5, Novelty 3.5, Amplification 3.75, Open Source 3, Usability 3, Continuity 3.25

| Judge | Comments |
|-------|----------|
| Fred Trotter | "The possibility that mirrulations could expand beyond regulations.gov is mind blowing" |
| Santhosh Veeramalla | "Solid initiative but would be great if include a note on scraping ethics and compliance" |
| Ben Coleman | "Produced valuable insights, discovering the SEC blocks scrapers while the FCC has an API. This is key for expanding beyond regulations.gov" |
| Evan Tung | "High-impact project for adding non-Regulations.gov data. Figuring out the APIs/websites is great future help. Needs better documentation" |
| Gautami Nadkarni | "Fantastic contribution...sharing methodologies and challenges, which significantly lowers the barrier to entry for others" |
| Michael Deeb | "Leverages official FCC API and CSS-selector scraper to retrieve filings; addresses external agency scraping challenge directly. Straightforward Python code but lacks packaging and tests. Huge impact and amplification" |

* **Takeaway**: Developed FCC and SEC scraping workflows, expanding the Mirrulations dataset beyond Regulations.gov. A strategic vision with critical intelligence gathering, but needs better documentation and usability.

### **USPF1**

* **Breakdown**: Median Scores: Impact 2, Novelty 2, Amplification 3, Open Source 2, Usability 2, Continuity 2

| Judge | Comments |
|-------|----------|
| Gautami Nadkarni | "Highly impactful and novel solution...highly usable tool that provides actionable insights" |
| Ben Coleman | "Addressed the valuable problem of tag generation, but the code didn't seem to match the description or the stated results" |
| Michael Deeb | "A LLM analysis pipeline that builds out some basic bones for doing more complicated analysis" |

* **Takeaway**: Mixed reception due to a disconnect between the project's stated goals and its actual implementation.

### **Within-Docket Dataset**

* **Breakdown**: Median Scores: Impact 4, Novelty 3, Amplification 4, Open Source 3, Usability 2, Continuity 3

| Judge | Comments |
|-------|----------|
| Melanie Kourbage | "Figuring out the impact of comments on the final rule is so valuable!...being able to study which comments are making an impact and how they're framed would be invaluable" |
| Gautami Nadkarni | "Great architecture and use of AI for impact" |
| Fred Trotter | "This project taught me the 'obvious after you say it' way to solve this problem. The idea is solid gold" |
| Ben Coleman | "Addresses the valuable but very difficult problem of linking rule changes to specific comments. Great idea, but delivered results were limited" |
| Michael Deeb | "Links comments to rule documents using timestamp windows and text matching. Clear notebook with actionable insights for policymakers. Strength lies in demonstrating a replicable analytic workflow" |

* **Takeaway**: Created a conceptual pipeline for mapping comment influence on regulatory changes. A "'solid gold' concept with immense policy value," but its execution was technically challenging within the hackathon's timeframe.

## Judges

* **Judge 1**: [Ben Coleman](https://www.linkedin.com/in/moraviancoleman/)

Ben is a Professor of Computer Science at Moravian University with expertise in Software Engineering and Computer Science Education. He serves as the primary maintainer of the Mirrulations project, and has lead it's development.

[Their Evaluation](submissions/coleman.md)

* **Judge 2**: [Fred Trotter](https://www.linkedin.com/in/fredtrotter/)

Fred is a Healthcare Data Technologist at the Centers for Medicare & Medicaid Services (CMS) Digital Service team, with extensive experience in healthcare informatics, data journalism, and cybersecurity. He collaborated with Ben Colman to explore the regulatory comment data space that forms the foundation of this hackathon.

[Their Evaluation](submissions/ftrotter.md)

* **Judge 3**: [Evan Tung](https://www.linkedin.com/in/ejtung/)

Evan is a Software Development Engineer at Amazon Web Services (AWS) and organizer at Civic Tech DC, where he coordinates biweekly project nights and connects volunteer civic hackers to local government and nonprofit projects.

[Their Evaluation](submissions/evan_tung.md)

* **Judge 4**: [Gautami Nadkarni](https://www.linkedin.com/in/gautaminadkarni/)

Gautami is a Senior Customer Engineer at Google Cloud with 7+ years of experience in cloud architecture and data strategy. She specializes in AI/ML solutions, data analytics, and helping Fortune 500 enterprises with cloud modernization and AI implementation.

[Their Evaluation](submissions/gautami_nadkarni.md)

* **Judge 5**: [Santhosh kumar Veeramalla](https://www.linkedin.com/in/santhoshk499/)

Santhosh is a Senior Scala Developer at Optum with 9+ years of experience building large-scale data platforms, real-time streaming pipelines, and cloud-native solutions. He specializes in Apache Spark, Databricks, and data engineering across Azure, AWS, and GCP environments.

[Their Evaluation](submissions/kumar_veeramalla.md)

* **Judge 6**: [Melanie Kourbage](https://www.linkedin.com/in/melanie-kourbage-48769044/)

Melanie is a Lead Specialist in Informatics at the Association of Public Health Laboratories (APHL) with 20+ years of experience in public health informatics project management, policy development, and system implementation. She specializes in informatics standards, technical assistance, and coordinating national public health initiatives across federal, state, and local organizations.

[Their Evaluation](submissions/melanie_kourbage.md)

* **Judge 7**: [Taylor Wilson](https://www.linkedin.com/in/taylorjameswilson/)

Taylor is Vice President of Applied Statistics and Data Science at Reveal Global Consulting, where he leads a team delivering AI/ML solutions to federal clients. He has extensive experience across multiple government agencies including the U.S. Census Bureau, Consumer Product Safety Commission, and Bureau of Labor Statistics. Taylor also runs DataKind DC, a partner organization of Civic Tech DC, and a partner for Civic Hack DC 2025.

[Their Evaluation](submissions/taylor_wilson.md)

* **Judge 8**: [Michael Deeb](https://www.linkedin.com/in/michael-deeb//)

Michael is a Principal Consultant with TealWolf Consulting and CTO with 15+ years of experience in AI, digital transformation, and systems architecture. He serves as Director & Board Member of Civic Tech DC and is the Founder & CTO of Keeplist.io. He specializes in AI strategy, civic technology, and complex problem solving across government and nonprofit sectors.

[Their Evaluation](submissions/deeb.md)

## Cross-Cutting Insights

### What Judges Valued Most

* **Practical Impact Over Innovation**: Usable tools with immediate value outscored technically complex prototypes.
* **Documentation Quality**: Repeatedly highlighted as a differentiator for high-scoring projects.
* **Ecosystem Integration**: Projects leveraging Mirrulations and other existing tools scored higher.
* **Usability for Non-Technical Users: Critical for real-world adoption.**

### Common Failure Patterns

1. **Poor Documentation** - Most common criticism across projects
2. **Only Jupyter Notebooks** - Consistently marked down for difficulty in reproducing results
3. **Scope Mismatch** - Ambitious ideas with limited execution time
4. **Isolation** - Projects that didn't connect to broader ecosystem goals or reinvented the wheel

### Technical Trends

* **AI/LLM Applications** dominated high-scoring projects
* **Data Infrastructure** (Parquet, vectorization) seen as foundational
* **Multi-format Processing** valued for comprehensive data coverage

### Judge Consistency Analysis

* **Most Aligned:** Infrastructure and practical utility projects
* **Most Divergent:** NLP/topic modeling approaches  
* **Consistent Themes:** Documentation, ecosystem integration, real-world applicability

## Methodology Notes

* **Data Sources**: 8 judge evaluation forms submitted between 2025-08-01 and 2025-08-05

* **Project Name Standardization**: Some judges used different names for the same projects:

* `llmgov` = "CMS Docket Assistant"
* `rules-talk` = "Talk to me in Rules"
* `taskmasters` = "Data Quality & Derived Layers"
* `the-scrapers` = "FCC & SEC Web Scraping"

* **Weighted Scoring Formula**: (Impact×0.2 + Novelty×0.2 + Amplification×0.15 + OpenSource×0.15 + Usability×0.15 + Continuity×0.15) × 20

* **Missing Evaluations**: Judges only evaluated projects they felt comfortable reviewing, or felt they could provide a useful evaluation for.

## Recommendations for Future Events

### For Organizers

1. **Emphasize Documentation**: Create README templates.
2. **Technical Review**: Do lightweight code reviews mid-day.
3. **Data & Infrastructure Prep**: Make sure to have data and infrastructure ready to go immediately.

### For Participants

* **Start with Documentation**: Write README first, code second.
* **Focus on Integrations**: Build on existing tools for greater impact, don't reinvent the wheel.
* **Prepare Demos**: Clear basic, user-friendly demos improve scoring.
* **Aim for Production Readiness**: Extract your code into discrete files to refrence from your notebook.
