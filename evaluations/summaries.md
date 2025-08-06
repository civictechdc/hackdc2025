# Civic Hack DC 2025: Final Hackathon Judging Analysis

## Overview

Civic Hack DC 2025 brought together developers, data scientists, and policy experts to tackle pressing challenges in regulatory comment analysis. This analysis summarizes final judging outcomes, project scores, cross-cutting insights, and recommendations for future hackathons.

---

## Projects by Alphabetical Order

### **[Can of Spam](../projects/canOfSpam/README.md)**

**Breakdown**:
Median Scores: Impact 4, Novelty 3, Amplification 3, Open Source 3, Usability 3, Continuity 3

| Judge               | Comments                                                                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Ben Coleman](./submissions/coleman.md#project-canofspam)         | "Good potential for a dashboard showing unique vs. duplicate comments. Current approach (text hashing) is limited but addresses a core problem."   |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-canofspam)    | "Documentation could be better; more technical capabilities would have been nice."                                                                 |
| [Fred Trotter](./submissions/ftrotter.md#project-canofspam)        | "Good stab at the problem!"                                                                                                                        |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-canofspam) | "The core idea is good, but the approach needs significant changes to support large datasets."                                                     |
| [Michael Deeb](./submissions/deeb.md#project-canofspam)        | "Solid proof-of-concept for detecting coordinated bot comments using temporal bursts and duplicate detection. High civic value, moderate novelty." |

**Takeaway**: Built a proof-of-concept for duplicate and bot comment detection, laying the groundwork for campaign analysis. Early but functional approach to a novel problem.

---

### **[Entity Resolution Team](../projects/entity-resolution-team/README.md)**

**Breakdown**:
Median Scores: Impact 3.75, Novelty 2.25, Amplification 3, Open Source 2.5, Usability 2, Continuity 2.5

| Judge               | Comments                                                                                                                                                                                                 |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Melanie Kourbage](./submissions/melanie_kourbage.md#project-entity-resolution)    | "I see a lot of potential here. I would use this to compare against a list of our member organizations."                                                                                                 |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-entity-resolution-team)    | "Poor documentation but good idea."                                                                                                                                                                      |
| [Ben Coleman](./submissions/coleman.md#project-entity-resolution-team)         | "Interesting approach to entity resolution by grouping commenters by email domain. Lacked documentation and supporting files."                                                                           |
| [Fred Trotter](./submissions/ftrotter.md#project-entity-resolution-team)        | "Regex is a perfect hackathon strategy: 80% and quick!"                                                                                                                                                  |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-entity-resolution-team) | "Lacks clear documentation, making it hard to understand and reuse."                                                                                                                                     |
| [Michael Deeb](./submissions/deeb.md#project-entity-resolution-team)        | "Classical approach to grouping regulatory comments by inferred organization. Uses standard text-cleaning and matching techniques that work but are not groundbreaking. Code reproducible via notebook." |

**Takeaway**: High policy value with practical applications, but basic technical execution and poor documentation.

---

### **[Expanded Search](../projects/expanded-search/README.md)**

**Breakdown**:
Median Scores: Impact 4, Novelty 2, Amplification 2.5, Open Source 3.5, Usability 3, Continuity 3.5

| Judge               | Comments                                                                                                                                                        |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-expanded-search)    | "High-quality code and implementation."                                                                                                                         |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-expanded-search) | "Clear documentation, quality code, but it is not fully ready."                                                                                                 |
| [Ben Coleman](./submissions/coleman.md#project-expanded-search)         | "Not presented. Appeared to be a search front-end."                                                                                                             |
| [Michael Deeb](./submissions/deeb.md#project-expanded-search)        | "Solid start on a docket discovery tool. Implementation is incomplete, limited NLP, and no live demo. Documentation and modular design are strong foundations." |

**Status**: Incomplete evaluation due to missing presentation and incomplete implementation.

**Takeaway**: A promising but unfinished search front-end for regulations.gov dockets, noted for high-quality code.

---

### **[Hive-Partitioned Parquet](../projects/hive-partitioned-parquet/README.md)**

**Breakdown**:
Median Scores: Impact 4.5, Novelty 4, Amplification 4, Open Source 4, Usability 3, Continuity 3.5

| Judge               | Comments                                                                                                                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Fred Trotter](./submissions/ftrotter.md#project-hive-partitioned-parquet)        | "Totally made me rethink how to use S3 as a database. Before it was a metaphor."                                                                                                                                 |
| [Ben Coleman](./submissions/coleman.md#project-hive-partitioned-parquet)         | "The idea is incredibly valuable and has significant potential for the ecosystem; I've already used ideas from it."                                                                                              |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-hive-partitioned-parquet) | "The core idea is very solid and the use of Parquet and Hive partitioning is a smart and scalable approach."                                                                                                     |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-hive-partitioned-parquet)    | "Very well explained. One of the best documentations and scripts."                                                                                                                                               |
| [Evan Tung](./submissions/evan_tung.md#project-hive-partitioned-parquet)           | "The query speed against remote S3 was amazing. Well-written README for technical users, but difficult for non-technical audiences."                                                                             |
| [Michael Deeb](./submissions/deeb.md#project-hive-partitioned-parquet)        | "Converts Mirrulations JSON to Hive-partitioned Parquet, sharply reducing query costs and enabling SQL access via DuckDB. High novelty and amplification as a foundational tool for the Mirrulations ecosystem." |

**Takeaway**: A paradigm-shifting approach to data architecture that changed how judges think about scalable infrastructure using S3.

---

### **[LLM.gov](../projects/llmgov/README.md)**

**Breakdown**:
Median Scores: Impact 5, Novelty 4, Amplification 4, Open Source 4, Usability 4, Continuity 4

| Judge               | Comments                                                                                                                                                                                                       |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Taylor Wilson](./submissions/taylor_wilson.md#project-llmgov)       | "Semantic search capability will supercharge the ability of users to interface with the content."                                                                                                              |
| [Ben Coleman](./submissions/coleman.md#project-llmgov)         | "Incredibly valuable RAG transformation process and vector embedding code that could be incorporated into the Mirrulations ETL."                                                                               |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-llmgov) | "Leveraging RAG with LLMs and vector embeddings is a powerful and scalable approach."                                                                                                                          |
| [Fred Trotter](./submissions/ftrotter.md#project-llmgov)        | "LLM that scales. Sign me up."                                                                                                                                                                                 |
| [Evan Tung](./submissions/evan_tung.md#project-llmgov-cms-docket-assistant)           | "Very usable for non-technical users. RAG is a standard GenAI application, but implementation is good. CLI scripts could be easier to run."                                                                    |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#cms-docket-assistant)    | "Average idea; documentation could be better."                                                                                                                                                                 |
| [Michael Deeb](./submissions/deeb.md#project-llmgov)        | "Makes CMS regulations searchable via RAG chat interface with AWS Bedrock. High civic value and user-friendly Streamlit UI; modular code with clear docs. Innovation is moderate given many LLM-RAG examples." |

**Takeaway**: Standard GenAI application, thoughtfully implemented with a scalable and modular RAG architecture.

---

### **[Mirrulations-CLI](../projects/mirrulations-cli/README.md)**

**Breakdown**:
Median Scores: Impact 5, Novelty 3.5, Amplification 5, Open Source 5, Usability 4.5, Continuity 4

| Judge               | Comments                                                                                                                                                  |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Fred Trotter](./submissions/ftrotter.md#project-mirrulations-cli)        | "Another example of 'oh this is the right way to think about this.'"                                                                                      |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-mirrulations-cli-on-pypi)    | "Excels in making a valuable but hard-to-access dataset easily usable. Highly practical and user-friendly solution."                                      |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-mirrulations-cli) | "Practical and developer-friendly solution with strong real-world utility."                                                                               |
| [Taylor Wilson](./submissions/taylor_wilson.md#project-mirrulations-cli)       | "I really love a quick, useful utility that expands functionality of existing tools. We should highly value contributions like this."                     |
| [Ben Coleman](./submissions/coleman.md#project-mirrulations-cli)         | "A wonderful extension of the pre-event work that makes core tools easier to use. I will incorporate this approach."                                      |
| [Michael Deeb](./submissions/deeb.md#project-mirrulations-cli)        | "PyPI-distributed CLI that markedly lowers the barrier to accessing regulatory data. Low novelty, but sometimes the small things are the most impactful." |

**Takeaway**: Packaged Mirrulations fetch and CSV tools into a polished CLI. Universally recognized as a fundamental improvement for data access.

---

### **[Rules-Talk](../projects/rules-talk/README.md)**

**Breakdown**:
Median Scores: Impact 4, Novelty 4, Amplification 4.25, Open Source 3.25, Usability 4, Continuity 3.5

| Judge               | Comments                                                                                                                               |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#talk-to-me-in-rules)    | "Exceptional and timely application of AI to a critical government function. High impact and strong novelty."                          |
| [Melanie Kourbage](./submissions/melanie_kourbage.md#project-rules-talk)    | "Info on sentiment, flavor of comments, serves as a pulse check. The instructions are very detailed."                                  |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-rules-talk) | "High-impact use case, as public comment analysis is often time-consuming."                                                            |
| [Taylor Wilson](./submissions/taylor_wilson.md#project-rules-talk)       | "The interface really took this project to the next level. Might be better to create known classification frameworks."                 |
| [Ben Coleman](./submissions/coleman.md#project-rules-talk)         | "Interesting approach using LLMs for sentiment analysis on HTML files—a new data source. Good for identifying patterns."               |
| [Michael Deeb](./submissions/deeb.md#project-rules-talk)        | "Uses LLMs to auto-outline policies and cluster comment issues with sentiment. Clear JSON schemas, CLI, and docs aid reproducibility." |

**Takeaway**: Used LLMs to cluster sentiment and topics in public comments. Strong UI and reproducibility. Good building blocks for a more sophisticated tool.

---

### **[Taskmasters](../projects/taskmasters/README.md)**

**Breakdown**:
Median Scores: Impact 3.5, Novelty 3, Amplification 3, Open Source 2.5, Usability 2.5, Continuity 3.25

| Judge               | Comments                                                                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#data-quality-derived-layers)    | "Robust and well-designed solution. Highly impactful and usable with strong continuity potential."                                                               |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-taskmasters) | "Handling PDF images and text files enhances data coverage."                                                                                                     |
| [Ben Coleman](./submissions/coleman.md#project-taskmasters)         | "Interesting work on .docx files, a format not yet considered. Project was unfocused and lacked documentation."                                                  |
| [Michael Deeb](./submissions/deeb.md#project-taskmasters)        | "Cohesive pipeline to extract text from PDFs, DOCX, and images. Addresses data-quality problem but uses standard OCR/NLP techniques. Lacks packaging and tests." |

**Takeaway**: Strong technical pipeline for multi-format processing, but marred by poor documentation and lack of packaging.

---

### **[Team Topic Modeling](../projects/team-topic-modeling/README.md)**

**Breakdown**:
Median Scores: Impact 3, Novelty 2, Amplification 2, Open Source 2, Usability 2, Continuity 2

| Judge               | Comments                                                                                                                                                                                 |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-team-topic-modeling)    | "Exceptional and highly relevant application of NLP. Demonstrates both strong novelty and a deep understanding of user needs."                                                           |
| [Fred Trotter](./submissions/ftrotter.md#project-team-topic-modeling)        | "Basic spaCy analysis. Well done."                                                                                                                                                       |
| [Ben Coleman](./submissions/coleman.md#project-team-topic-modeling)         | "Basic analysis with spaCy. Lacked documentation and novelty."                                                                                                                           |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-team-topic-modeling) | "No clear documentation. The code lacks clarity and structure."                                                                                                                          |
| [Michael Deeb](./submissions/deeb.md#project-team-topic-modeling)        | "Uses spaCy and RAKE to highlight topics and auto-generate visual insights. Useful for exploratory analysis, but code is a single file with hard-coded paths and minimal documentation." |

**Takeaway**: Polarized responses reflect how critical documentation and clarity are, even for technically sound approaches.

---

### **[Team VeloGear](../projects/team-velogear/README.md)**

**Breakdown**:
Median Scores: Impact 3, Novelty 1, Amplification 2, Open Source 3, Usability 3, Continuity 2

| Judge            | Comments                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-team-velogear) | "Practical and well-executed utility. Strong potential for integration."                                                        |
| [Ben Coleman](./submissions/coleman.md#project-team-velogear)      | "Well-presented project, but was a simple wrapper for a PDF tool and didn’t integrate with the broader Mirrulations ecosystem." |
| [Michael Deeb](./submissions/deeb.md#project-team-velogear)     | "Simple Go CLI that uses `pdftotext` to convert PDFs into CSV/JSON/Parquet. Clear README and functional code."                  |

**Takeaway**: Useful utility, but limited innovation and ecosystem integration.

---

### **[The Scrapers](../projects/the-scrapers/README.md)**

**Breakdown**:
Median Scores: Impact 4.5, Novelty 3.5, Amplification 3.75, Open Source 3, Usability 3, Continuity 3.25

| Judge               | Comments                                                                                                       |
| ------------------- | -------------------------------------------------------------------------------------------------------------- |
| [Fred Trotter](./submissions/ftrotter.md#project-the-scrapers)        | "The possibility that Mirrulations could expand beyond regulations.gov is mind-blowing."                       |
| [Santhosh Veeramalla](./submissions/kumar_veeramalla.md#project-the-scrapers) | "Solid initiative. Would benefit from a note on scraping ethics and compliance."                               |
| [Ben Coleman](./submissions/coleman.md#project-the-scrapers)         | "Discovered SEC blocks scrapers while FCC has an API. Key insights for ecosystem expansion."                   |
| [Evan Tung](./submissions/evan_tung.md#project-fcc--sec-web-scraping)           | "High-impact project for adding non-regulations.gov data. Needs better documentation."                         |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-the-scrapers)     | "Fantastic contribution. Sharing methods and challenges lowers the barrier for others."                        |
| [Michael Deeb](./submissions/deeb.md#project-the-scrapers)        | "Scrapes FCC API and SEC via CSS selectors. Straightforward code, high impact, but lacks packaging and tests." |

**Takeaway**: Strategic expansion effort beyond regulations.gov. Excellent research and direction, but needs polish and ethical guidance.

---

### **[USPF1](../projects/uspf1/README.md)**

**Breakdown**:
Median Scores: Impact 2, Novelty 2, Amplification 3, Open Source 2, Usability 2, Continuity 2

| Judge            | Comments                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------- |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-uspf1) | "Highly impactful and novel solution. Very usable and insightful."                            |
| [Ben Coleman](./submissions/coleman.md#project-uspf1)      | "Valuable problem (tag generation), but code didn’t align with description."                  |
| [Michael Deeb](./submissions/deeb.md#project-uspf1)     | "Early LLM pipeline with basic foundations. Concept is stronger than current implementation." |

**Takeaway**: Disconnect between concept and code hurt evaluations. Needs alignment and clarity.

---

### **[Within-Docket Dataset](../projects/within-docket-dataset/README.md)**

**Breakdown**:
Median Scores: Impact 4, Novelty 3, Amplification 4, Open Source 3, Usability 2, Continuity 3

| Judge            | Comments                                                                                                   |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| [Melanie Kourbage](./submissions/melanie_kourbage.md#project-within-docket-dataset) | "Understanding the impact of comments on final rules is incredibly valuable."                              |
| [Gautami Nadkarni](./submissions/gautami_nadkarni.md#project-within-docket-dataset) | "Great architecture and use of AI for impact."                                                             |
| [Fred Trotter](./submissions/ftrotter.md#project-within-docket-dataset)     | "A 'why didn’t we think of this sooner' kind of idea. Solid gold."                                         |
| [Ben Coleman](./submissions/coleman.md#project-within-docket-dataset)      | "Addresses a difficult problem—linking rule changes to comments. Great idea, limited execution."           |
| [Michael Deeb](./submissions/deeb.md#project-within-docket-dataset)     | "Links comments to rules via timestamp windows and text matching. Clear notebook and replicable workflow." |

**Takeaway**: One of the most strategically valuable ideas. Technically hard to pull off in 6 hours but shows great promise.

---

## Judges

* **[Ben Coleman](./submissions/coleman.md)** – [LinkedIn](https://www.linkedin.com/in/moraviancoleman/)
  Professor of Computer Science at Moravian University and primary maintainer of the Mirrulations project.

* **[Fred Trotter](./submissions/ftrotter.md)** – [LinkedIn](https://www.linkedin.com/in/fredtrotter/)
  Healthcare Data Technologist at CMS Digital Service; healthcare informatics and open data expert.

* **[Evan Tung](./submissions/evan_tung.md)** – [LinkedIn](https://www.linkedin.com/in/ejtung/)
  Software Engineer at AWS and Civic Tech DC organizer.

* **[Gautami Nadkarni](./submissions/gautami_nadkarni.md)** – [LinkedIn](https://www.linkedin.com/in/gautaminadkarni/)
  Senior Customer Engineer at Google Cloud, focused on AI/ML and data modernization.

* **[Santhosh Kumar Veeramalla](./submissions/kumar_veeramalla.md)** – [LinkedIn](https://www.linkedin.com/in/santhoshk499/)
  Senior Scala Developer at Optum with deep expertise in Spark and data engineering.

* **[Melanie Kourbage](./submissions/melanie_kourbage.md)** – [LinkedIn](https://www.linkedin.com/in/melanie-kourbage-48769044/)
  Lead Specialist at APHL; veteran in public health informatics and federal-state data systems.

* **[Taylor Wilson](./submissions/taylor_wilson.md)** – [LinkedIn](https://www.linkedin.com/in/taylorjameswilson/)
  VP of Applied Statistics at Reveal Global Consulting, leads DataKind DC.

* **[Michael Deeb](./submissions/deeb.md)** – [LinkedIn](https://www.linkedin.com/in/michael-deeb/)
  Principal Consultant at TealWolf, CTO of Keeplist.io, and Director at Civic Tech DC.

---

## Cross-Cutting Insights

### What Judges Valued Most

* **Practical Impact Over Innovation** – Tools solving immediate problems scored higher than experimental or speculative ones.
* **Documentation Quality** – Consistently mentioned as critical for both understanding and reuse.
* **Ecosystem Integration** – Projects that built on or improved Mirrulations tools earned higher marks.
* **Usability for Non-Technical Users** – Often a differentiator in real-world adoption and impact.

---

### Common Failure Patterns

1. **Poor Documentation** – The most consistent criticism across judges.
2. **Jupyter Notebooks Only** – Penalized for being hard to reuse or scale.
3. **Scope Mismatch** – Big ideas with too little progress in the time allowed.
4. **Isolation** – Projects that didn’t integrate or duplicated existing functionality.

---

### Technical Trends

* **AI/LLM Applications** were prominent among top-scoring projects.
* **Data Infrastructure (Parquet, Hive, DuckDB)** considered critical enablers.
* **Multi-Format Support (PDFs, DOCX, images)** emerged as a key challenge area.

---

### Judge Consistency

* **Most Aligned**: Infrastructure and data tooling projects.
* **Most Divergent**: NLP and topic modeling projects.
* **Shared Priorities**: Clarity, reproducibility, integration, usability.

---

## Methodology Notes

* **Data Sources**: 8 judge submissions from Aug 1–5, 2025.
* **Project Name Normalization**:

  * `llmgov` = *CMS Docket Assistant*
  * `rules-talk` = *Talk to Me in Rules*
  * `taskmasters` = *Data Quality & Derived Layers*
  * `the-scrapers` = *FCC & SEC Web Scraping*
* **Scoring Formula**:
  `(Impact×0.2 + Novelty×0.2 + Amplification×0.15 + OpenSource×0.15 + Usability×0.15 + Continuity×0.15) × 20`
* **Incomplete Reviews**: Not all judges reviewed every project; some passed on projects outside their expertise.

---

## Recommendations for Future Events

### For Organizers

1. **Emphasize Documentation** – Provide README templates and checklists.
2. **Mid-Day Check-ins** – Include lightweight tech reviews to redirect struggling teams.
3. **Infrastructure Readiness** – Ensure datasets and APIs are available from the start.

### For Participants

* **Start with the README** – Writing your README early helps clarify the project.
* **Build on Existing Tools** – Integration often wins over reinvention.
* **Prepare Demos** – Even simple, working demos influence scoring heavily.
* **Modularize Your Code** – Extract functionality into clean, importable modules for reuse.
