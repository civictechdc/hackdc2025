## Across Docket Dataset: Entity Map

### Problem

It’s difficult to identify and track which entities are commenting on which regulations. For instance, when a comment is “signed by the AMA,” it signals that the American Medical Association cares about the topic—but what other topics do they engage with? Analysts need an easy way to “click” on an entity like the AMA and view all their comments across dockets.

### Context from Stakeholders

> “I am responsible for tracking public health informatics policy on behalf of my organization. This responsibility includes surveilling proposed rules and standards, submitting comments, and tracking the comments of our sister organizations, such as CSTE, NACCHO, NAPHSIS, AMIA, AIRA, APHA, and HIMSS, as well as public health agencies at the local and state level. It is often difficult to locate their comments (or sometimes even my own) on Regulations.gov, even when I know that the organization has submitted them. As a workaround, I usually reach out to the NGO directly and ask for a copy.”

### Key Requirement

This requires **robust entity extraction and resolution** — accurately identifying organizations and individuals across datasets and unifying their submissions, even when names or formats vary.

### Proposed Approach

* Build an **entity map** linking organizations to all their comments across dockets.
* Develop tools for easy querying (e.g., “click on AMA to see all related comments across dockets”).
* Use curated starting lists of key entities (e.g., CSTE, NACCHO, NAPHSIS, AMIA, AIRA, APHA, HIMSS) to seed automated extraction tools.

### Potential Outcome

An enriched dataset providing:

* **Cross-docket entity profiles** showing where and how organizations engage in regulatory processes.
* Insights into organizational priorities and influence across multiple topics and rulemaking cycles.

**Goal:** Enable users to easily identify an organization’s full engagement across dockets, improving transparency and supporting policy analysis.
