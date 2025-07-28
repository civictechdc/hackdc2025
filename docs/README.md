# Problem Landscape for Civic Hack DC 2025 – Part 1: Making Public Comments Count

## Table of Contents

### 📋 Overview & Context

- [Context](#context)
- [The Data Lake: A Technical Overview of the Mirrulations Ecosystem](#the-data-lake-a-technical-overview-of-the-mirrulations-ecosystem)

### 🔍 Interesting Dockets to Analyze

- [Interesting Dockets to Analyze](#interesting-dockets-to-analyze)
  - [CMS Digital Ecosystem RFI Docket Series](#cms-digital-ecosystem-rfi-docket-series)
  - [Kratom and Marijuana Docket Series](#kratom-and-marijuana-docket-series)

### 🎯 Core Problem Themes

- [Problem Themes](#problem-themes)
  - [Data Accessibility & Cost](#data-accessibility--cost)
  - [Scraping Specific Agency Comment Systems](#scraping-specific-agency-comment-systems)
  - [Data Quality & Derived Layers](#data-quality--derived-layers)
  - [Docket-Level Analysis](#docket-level-analysis)
  - [Cross-Docket & Version-Aware Analysis](#cross-docket--version-aware-analysis)
  - [Entity Resolution](#entity-resolution)
  - [Campaign Detection](#campaign-detection)
  - [Position & Sentiment Analysis](#position--sentiment-analysis)
  - [Influence Mapping & Feedback Loops](#influence-mapping--feedback-loops)
  - [Usability for Non-Technical Stakeholders](#usability-for-non-technical-stakeholders)
  - [Regulatory Document Discovery & Navigation](#regulatory-document-discovery--navigation)

### 🚀 Additional Opportunities

- [Other Needs](#other-needs)
  - [Emerging Additive Needs](#emerging-additive-needs)
  - [Where Mirrulations Helps & Where Gaps Remain](#where-mirrulations-helps--where-gaps-remain)
  - [Bottom Line](#bottom-line)

### 📝 Community Input & Use Cases

- [Problem Statement Submissions](#problem-statement-submissions)
  - [Consolidated Needs Across All Submissions](#consolidated-needs-across-all-submissions)
  
#### Form Submissions

- [Form Submissions (CSV)](#form-submissions-csv)
  - [Visualising Comment Data for Policy Analysis](#visualising-comment-data-for-policy-analysis)
  - [Summarising Large Volumes of Comments](#summarising-large-volumes-of-comments)
  - [How Common Is the Feedback?](#how-common-is-the-feedback)

#### Email Submissions

- [Email Submissions (Verbatim Excerpts)](#email-submissions-verbatim-excerpts)
  - [Potential Use Cases / Problem Statements](#potential-use-cases--problem-statements)
  - [Influence of Comments on Final Rules](#influence-of-comments-on-final-rules)
  - [Desired Insights From Comments](#desired-insights-from-comments)
  - [Case Study: USCDI V6 Platform Challenges](#case-study-uscdi-v6-platform-challenges)
  - [Additional Notes on Regulation Titles & Market Opportunity](#additional-notes-on-regulation-titles--market-opportunity)
  - [Fragmented Federal Comment Systems](#fragmented-federal-comment-systems)

---

# Things to Hack On & Context

## Context

Regulations.gov hosts tens of millions of public comments, dockets, and supporting documents that shape U.S. federal rule‑making, but access to the data is slow and cumbersome. The **Mirrulations** project mirrors this dataset to a public S3 bucket (\~2.3 TB), enabling faster, easier access. This opens opportunities for researchers, advocacy groups, journalists, and agencies to tackle challenges in finding, interpreting, and linking this data to policy outcomes.

Feedback from nonprofits, public‑health policy analysts, and civic technologists converges on inter‑related challenges that make regulatory engagement slow, costly, and opaque.

## The Data Lake: A Technical Overview of the Mirrulations Ecosystem

Mirrulations (MIRRor of regULATIONS.gov) is a comprehensive ecosystem developed by [Moravian University Computer Science](https://www.moravian.edu/computer-science) to ingest, process, store, and serve U.S. federal regulatory data from Regulations.gov. It provides a robust, scalable, and accessible way for researchers, developers, and the public to interact with this complex dataset. The system overcomes the API’s 1,000 items/hour limit by using donated API keys to maintain a continuously updated mirror — about 27 million items — including text extracted from PDFs.

**Data Access: [s3://mirrulations](https://github.com/awslabs/open-data-registry/blob/main/datasets/mirrulations.yaml)** At its core is the public S3 bucket `s3://mirrulations`, part of the AWS Open Data Sponsorship Program. This bucket hosts JSON files representing dockets, documents, and comments, as well as associated binary attachments (PDFs and more).

**Direct-Access Toolkit for Researchers** For users working directly with raw data, Mirrulations provides standalone command-line utilities:

- [**mirrulations-fetch**](https://github.com/mirrulations/mirrulations-fetch)**:** Download all data for a specific docket ID from the S3 bucket to a local machine with a simple command.  
- [**docket-stats (mirrulations-query)**](https://github.com/mirrulations/mirrulations-query)**:** Validate data completeness by comparing counts of dockets, documents, and comments in S3 against the live Regulations.gov API.  
- [**mirrulations-csv**](https://github.com/mirrulations/mirrulations-csv)**:** Convert downloaded comment JSON files into a single, clean CSV file, intelligently excluding empty or constant fields to simplify downstream analysis.

*For details on how the data is organised (dockets, documents, comments, attachments, and extraction outputs), see the [Mirrulations data structure reference](https://github.com/MoravianUniversity/mirrulations-data/blob/main/structure.md).*

Contact: [colemanb@moravian.edu](mailto:colemanb@moravian.edu)

---

## Interesting Dockets to Analyze

### CMS Digital Ecosystem RFI Docket Series

- **Most recent RFI:** [CMS‑0042‑NC – RFI on Digital Ecosystem](https://www.regulations.gov/docket/CMS-2025-0050)  

- **Previous related dockets:**  

  - [CMS‑0058‑NC – National Directory of Healthcare Providers & Services](https://www.regulations.gov/docket/CMS-2022-0163)  
  - [CMS‑9115‑P – Interoperability and Patient Access…](https://www.regulations.gov/docket/CMS-2019-0039)  
  - [HHS‑ONC‑2019‑0002 – 21st Century Cures Act: Interoperability, Information Blocking, and the ONC Health IT Certification Program](https://www.regulations.gov/docket/HHS-ONC-2019-0002)

### Kratom and Marijuana Docket Series

- **Kratom**  

  - [Temporary Placement of Mitragynine and 7‑Hydroxymitragynine into Schedule I – DEA‑2016‑0015](https://www.regulations.gov/docket/DEA-2016-0015)  
  - [Process and issues overview](https://www.uspharmacist.com/article/the-dea-changes-its-mind-on-kratom)

- **Marijuana**  

  - [Rescheduling of Marijuana – DEA‑2024‑0059](https://www.regulations.gov/document/DEA-2024-0059-0001)  
  - [Process and issues overview](https://moritzlaw.osu.edu/faculty-and-research/drug-enforcement-and-policy-center/research-and-grants/policy-and-data-analyses/federal-marijuana-rescheduling)

---

## Problem Themes

### Data Accessibility & Cost

- **Pain:** The mirrored data is large, highly structured, and JSON‑heavy, making it inconvenient for data analysis.  

- **Stakeholder Quotes:**  

  - “Accessing all the data in this format can be slow, but it’s way better than Regulations.gov.”  
  - “What can we build on top of the raw Mirrulations data… leveraging free S3 and open‑source tools?”

- **Need:**  

  - Efficient formats (Parquet/ORC) for scalable storage and querying.  
  - Lightweight, local‑friendly pipelines (DuckDB, SQLite).

**Details:** [download‑tool improvement](./additional_problem_details/download_tools.md)

---

### Scraping Specific Agency Comment Systems

- **Pain:** Outside [Regulations.gov](https://regulations.gov), public‑comment data is scattered across agency‑specific systems with inconsistent formats, making scraping and analysis slow and error‑prone.  

- **Current State:** Agencies such as FCC, FERC, SEC, USITC, CFTC, FTC, and NLRB operate their own portals.  

- **Need:**  

  - Build scraping scripts for agency systems (e.g., FCC’s ECFS API).  
  - Deliver clear, standardised data formats (JSON) for comments and attachments.

**Details:** [scraping regulations that are *not* on Regulations.gov](./additional_problem_details/external_agency_scraping.md)

---

### Data Quality & Derived Layers

- **Pain:** Derived data is incomplete and low‑quality.  

- **Stakeholder Quote:** “Data already exists — could be better… what derived format would be optimal?”  

- **Current State:** Most dockets have “derived” data via Mirrulations, but only PDFs are parsed; extraction quality is low and unstructured.  

- **Need:**  

  - Higher‑quality structured extraction for PDFs, Word docs, images, and HTML.  
  - Normalise text extraction across formats.  
  - Integrate with **Position & Sentiment Analysis** modules.

---

### Docket-Level Analysis

- **Pain:** Single dockets (e.g., DEA‑2024‑0059) can contain tens of thousands of comments; final rules reference commenters only abstractly.  

- **Stakeholder Quote:** “How can we summarise key themes, arguments, and sentiments from thousands of comments on a single rule?”  

- **Need:**  

  - Per‑docket dashboards to explore comments throughout the lifecycle.  
  - Easy export tools (CSV / text) for single‑docket analysis.  
  - Automated plain‑language summaries for non‑technical stakeholders.

**Details:**

- [linking comments from Proposed Rule to Final Rule](./additional_problem_details/rule_backlinking.md)  
- [coordinated comment detection](./additional_problem_details/campaign_detection.md)

---

### Cross-Docket & Version-Aware Analysis

- **Pain:** No global search or cross‑linking of related dockets; difficult to map RFIs → Proposed Rules → Final Rules or track rule evolution across years.  

- **Stakeholder Quotes:**  

  - “Global docket search… filtering by agency.”  
  - “How are dockets related?”

- **Need:**  

  - Cross‑docket mapping with thematic and phase linkages.  
  - Version‑aware tracking of iterative rules and comment cycles.  
  - Topical graphing: build a “connected dockets” dataset in S3.  
  - Semantic enrichment to expand keyword searches.

**Details:**

- [regulatory sequence map](./additional_problem_details/docket_mapping.md)  
- [topic extraction for regulatory terms](./additional_problem_details/topic_sentiment.md)  
- [commenter threads across dockets](./additional_problem_details/cross_docket_commenter_threads.md)

---

### Entity Resolution

- **Pain:** Organisation names are messy and inconsistent, obscuring who submitted comments.  

- **Stakeholder Quotes:**  

  - “Make it easier to determine which organisations submitted comments.”  
  - “We need entity disambiguation.”

- **Need:** Canonical entity resolution to unify aliases and classify entities (advocacy, industry, etc.).

**Details:** [entity map of regulatory commenters](./additional_problem_details/entity_mapping.md)

---

### Campaign Detection

- **Pain:** Duplicate or campaign‑driven comments inflate counts and obscure genuine engagement.  

- **Stakeholder Quote:** “Track campaigns.”  

- **Need:**  

  - Identify duplicates, irrelevant submissions, templates, and AI‑ or bot‑generated comments.  
  - Extract unique text as the signal.

**Starter Idea:** [detecting bots via submission times](./additional_problem_details/bot_detection.md)

---

### Position & Sentiment Analysis

- **Pain:** Binary “for/against” coding misses nuance; manual consensus measurement is error‑prone.  

- **Stakeholder Quotes:**  

  - “Sophisticated position analysis… can we use LLMs?”  
  - “How many credible commenters made similar points?”

- **Need:**  

  - Extract and cluster positions.  
  - Quantify shared stances.  
  - Summarise clusters.

---

### Influence Mapping & Feedback Loops

- **Pain:** Agencies summarise comments but rarely cite specifics, leaving commenters unsure of impact.  

- **Stakeholder Quotes:**  

  - “Develop tools to assess whether and how comments influenced the final rule.”  
  - “Which entities actually impact regulatory filings?”

- **Need:**  

  - Proposed → final diffing with regulator responses.  
  - Influence scoring.  
  - Feedback loops so organisations can benchmark and refine engagement.

---

### Usability for Non-Technical Stakeholders

- **Pain:** Advocates, journalists, and coalition staff struggle with Regulations.gov and lack digestible reports.  

- **Stakeholder Quotes:**  

  - “Help non‑experts discover adjacent topics.”  
  - “How can we develop interactive visualisations that help policy analysts and the public quickly understand patterns?”

- **Need:**  

  - Interactive dashboards of patterns, consensus, and trends.  
  - Guided semantic search.  
  - Automated sector‑specific digests.

**Details:** [LLM ingestion and Q&A](./additional_problem_details/llm_integration.md)

---

### Regulatory Document Discovery & Navigation

- **Pain:** Near‑identical, lengthy rule titles obscure key differences; critical provisions are buried without clear sign‑posting.  

- **Stakeholder Quote:** “Out of the 400+ pages, I'm interested in about 5\. If I didn't know what I was looking for, I never would have found the sections that impact public‑health data exchange.”  

- **Need:**  

  - AI‑generated section summaries with topic tags.  
  - Cross‑rule topic indexing (“public‑health reporting” → specific pages across all rules).

- **Impact:** Upstream discovery problems mean stakeholders miss commenting opportunities before they begin — making downstream comment‑analysis tools irrelevant if users can’t find what to comment on.

---

# Other Needs

## Emerging Additive Needs

- Semantic enrichment & onboarding to teach new users adjacent topics and common terms in a regulatory domain.  
- Topical graphing to store and expose "connected dockets" as a browsable dataset.  
- Entity threads across rules to track an organisation’s regulatory engagement longitudinally.  
- Advanced coordination/fraud detection using text similarity, timing analysis, and submission clustering.  
- Proposed → final rule diffing that combines comment clusters with regulator responses to pinpoint influence and adoption.  
- Scalable LLM pipelines that adapt proven API‑driven approaches for summarisation, topic mining, and cross‑docket analysis.

## Where Mirrulations Helps & Where Gaps Remain

| Strengths | Gaps |
| :---- | :---- |
| • Mirrored data available in public S3. | • No semantic enrichment or topical graphing. |
| • [Example repo with API & OpenSearch for full‑text search.](https://github.com/mirrulations/dev) | • No entity resolution or longitudinal tracking. |
| • Structured PostgreSQL metadata. | • No consensus measurement or influence mapping. |
|  | • No user‑facing dashboards or guided search. |

## Bottom Line

Stakeholders need affordable, enriched, and accessible pipelines that transform Regulations.gov data from a raw mirror into an actionable civic resource:

- **Policy analysts:** Find partner organisations’ comments, measure consensus, and receive sector‑specific digests.  
- **Advocates & journalists:** Detect coordinated campaigns and emerging issues using text‑plus‑timing analysis.  
- **Agencies & NGOs:** Trace comment influence, evaluate feedback adoption, and generate compliance‑ready summaries to inform better engagement strategies.

This landscape provides a blueprint for prioritising MVP pipelines (entity resolution, semantic search, consensus counting) while charting long‑term goals (influence mapping, advanced coordination detection, cross‑docket and cross‑platform graphs).

---

# Problem Statement Submissions

## Consolidated Needs Across All Submissions

| Theme | Specific Gaps |
| :---- | :---- |
| Discoverability | Locate and categorise commenters across platforms. |
| Visualisation | Dashboards for trends, geography, networks. |
| Summarisation | NLP clustering of themes and sentiment. |
| Impact Tracking | Link comments to final‑rule text and measure influence. |
| Cross‑Agency Aggregation | Unified access layer spanning all comment systems. |
| Title Clarity | Disambiguate lengthy rule titles and surface relevant sections. |

##

## Form Submissions (CSV)

### Visualising Comment Data for Policy Analysis

- **Submitted:** 23 Jul 2025 15:38  
- **Submitter:** *Yashin Lin*  
- **Problem / Challenge:** “How can we develop interactive visualisations that help policy analysts and the public quickly understand patterns, trends, and outliers within a large dataset of public comments?”  
- **Why It Matters:** “Raw data, even clean data, can be overwhelming. Effective visualisations (e.g., temporal trends of comments, geographical distribution of commenters, network graphs of related organisations) could unlock insights and improve public understanding of the rule‑making process.”  
- **Desired Solution:** Interactive visual dashboards showing temporal, geographic, and relational patterns in comment data.  
- **Participation Availability:** Potentially available.

---

### Summarising Large Volumes of Comments

- **Submitted:** 23 Jul 2025 15:40  

- **Submitter:** *Yashin Lin*  

- **Problem / Challenge:**  

  1. Same visualisation need as above.  
  2. “How can we effectively and accurately summarise the key themes, arguments, and sentiments from thousands or tens of thousands of public comments on a single proposed rule?”

- **Why It Matters:** “Agencies are required to consider comments, but manually sifting through vast quantities is impractical. Automated summarisation, perhaps using NLP techniques, could dramatically improve efficiency and understanding of public input.”  

- **Desired Solution:** NLP‑driven thematic and sentiment summaries.  

- **Participation Availability:** Potentially available.

---

### How Common Is the Feedback?

- **Submitted:** 25 Jul 2025 14:04  

- **Submitter:** *Melanie Kourbage* — Association of Public Health Laboratories (APHL)  

- **Problem / Challenge:** “It is often difficult to locate comments from sister organisations on Regulations.gov, even when I know they submitted them… We strongly suspect that partner organisations made similar points, but verifying this is challenging. For instance, CMS recently solicited comments via an RFI embedded in the CMS IPPS Proposed Rule for 2026. Approximately how many credible commenters made a similar point? Can we analyse the data to see how often those dataflows were referenced and produce a digestible report?”  

- **Why It Matters:**  

  1. Gauge the importance of an issue for the public‑health community.  
  2. Measure how engaged partner organisations are in the commenting process.

- **Desired Solution:** Search, aggregation, and reporting tools that identify commenters, quantify topic overlap, and produce clear comparative reports.  

- **Relevant Link:** [https://www.regulations.gov/document/CMS-2025-0028-0013/comment](https://www.regulations.gov/document/CMS-2025-0028-0013/comment)  

- **Participation Availability:** Potentially available (logo opt‑out).

---

## Email Submissions (Verbatim Excerpts)

### Potential Use Cases / Problem Statements

**Identifying commenters:** Make it easier to determine which organisations submitted comments and categorise them by type (advocacy, industry, academia, individuals).

**Analysing comment content:** Enable better analysis of how many organisations commented on specific topics or themes.

**Tracking impact:** Develop tools to assess whether and how submitted comments influenced the final rule (e.g., whether particular suggestions were accepted or addressed).

### Influence of Comments on Final Rules

“I’d love to know how often and how substantively rules actually change in response to comments — and whether certain areas of law are more likely to change or stay the same regardless of what comments are submitted. How much do comments actually influence the final rules? I’d also be interested in how agencies use RFIs before proposed rules.”

### Desired Insights From Comments

“Your focus on impact resonates. In a nutshell, this is what I want to get out of the comments:

• What did other organisations say? Did they make similar points to ours? Did we miss any obvious points? • What changed in the final rule, and were there comments suggesting that change? • APHL often submits the same feedback repeatedly, especially on annually updated rules. We must ask whether it’s worth submitting if our recommendations aren’t adopted, or whether we should re‑frame feedback. We’ve met with some federal agencies to get insight, but with mixed success.”

### Case Study: USCDI V6 Platform Challenges

“USCDI V6 uses a separate platform, not Regulations.gov, to collect feedback, amplifying existing problems. Commenters must respond to data elements one by one. We submitted at least a dozen comments in May for V6. There’s a separate submission process to add or remove a data element. The platform saves all comments on all previous USCDI versions (V1‑V6), which is both good and bad. I just compared the final V6 standard to our comments and found none adopted. Several NGOs submitted comments; I don’t know whether theirs were addressed. I would be ecstatic if AI could handle this comparison.”

### Additional Notes on Regulation Titles & Market Opportunity

“First, the titles are a nightmare. Three CMS proposed rules dropped within 60 days. If I didn’t know what I was looking for, I never would have found the sections that impact public‑health data exchange and reporting.”

### Fragmented Federal Comment Systems

Several major agencies host comments outside Regulations.gov:

| Agency | System |
| :---- | :---- |
| FCC | ECFS |
| SEC | Internal website / email |
| FERC | eFiling & eComment |
| USITC | EDIS |
| STB | Environmental & docket portals |
| FTC | Public Comments page |
| NRC | ADAMS archive (post‑Regulations.gov) |
| CFTC | Comment portal |
| CFPB | Mixed systems |
| NLRB | Electronic filing |

*Challenge:* Scrape the various portals and produce data aligned with the Mirrulations ecosystem to strengthen the broader dataset.  
