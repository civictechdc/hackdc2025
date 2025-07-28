## Scraping Specific Agency Comment Systems

Outside of [Regulations.gov](https://www.regulations.gov), many agencies maintain their own portals for public comments, often with inconsistent formats that make scraping and analysis slow and error-prone.

### Pain Points

* Public comment data scattered across multiple agency-specific systems.
* Inconsistent submission and document formats.
* Difficulties in integrating these data sources into unified analysis pipelines.

### Current State

Agencies like **FCC**, **FERC**, **SEC**, **USITC**, **CFTC**, **FTC**, and **NLRB** operate their own portals for comments and related filings.

### Need

* Build scraping scripts for these agency systems (e.g., FCC’s ECFS API).
* Deliver clear, standardized JSON data formats for comments and attachments.
* Map non-Regulations.gov portals to the [Mirrulations](https://github.com/mirrulations/mirrulations-fetch) data structure for compatibility.

### Example: SEC Data

* **Main Index:** [SEC Rulemaking Activity](https://www.sec.gov/rules-regulations/rulemaking-activity)
* **Example Rule:** [S7-11-23 – Final Rule](https://www.sec.gov/rules-regulations/2025/06/s7-11-23#34-103320final)
* **Goal:** Map SEC data to follow the Mirrulations directory structure for ingestion into the S3 ecosystem.

```
s3://mirrulations
 ├── raw-data
 │   └── <agency>
 │       └── <docket id>
 │           ├── text-<docket id>
 │           │   ├── comments
 │           │   │   ├── <comment id>.json
 │           │   ├── docket
 │           │   │   ├── <docket id>.json
 │           │   └── documents
 │           │       ├── <document id>.json
 │           │       ├── <document id>_content.htm
 │           └── binary-<docket id>
 │               └── comments_attachments
 │                   ├── <comment id>_attachment_<counter>.<ext>
 └── derived-data
     └── <agency>/<docket id>/<organization>/<project>/<file type>/<data file>
```

### Key Agency Portals

| Agency | Portal                                                                                             | Notes                                               |
| ------ | -------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| FCC    | [ECFS](https://www.fcc.gov/ecfs)                                                                   | Public API for docket and comment queries.          |
| FERC   | [FERC Online](https://www.ferc.gov/ferc-online/overview)                                           | eComment & eLibrary for filings and search.         |
| SEC    | [SEC Rulemaking](https://www.sec.gov/rules-regulations/rulemaking-activity)                        | Lists rulemaking activity with public comments.     |
| USITC  | [EDIS](https://edis.usitc.gov)                                                                     | Trade-related complaints, investigations, comments. |
| CFTC   | [Public Comments](https://comments.cftc.gov)                                                       | Portal for proposed rules and feedback.             |
| FTC    | [Public Comments](https://www.ftc.gov/policy/public-comments)                                      | Feedback on rulemakings, settlements, workshops.    |
| NLRB   | [Rulemaking](https://www.nlrb.gov/about-nlrb/what-we-do/national-labor-relations-board-rulemaking) | Uses Regulations.gov for dockets and comments.      |

**Goal:** Build robust pipelines to scrape, standardize, and integrate agency-specific data into a unified open dataset for analysis.
