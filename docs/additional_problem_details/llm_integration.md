## General LLM to Read a Docket and Respond to Questions

### Problem

Current tools for exploring dockets via AI are limited by the [Regulations.gov](http://regulations.gov) API’s constraints, which slows access and limits scalability.

### Existing Work

Healthcare data expert **Josh Mandel** has created a stack that “sips” data through the Regulations.gov API and allows users to browse and query comments:

* [Twitter Summary](https://x.com/JoshCMandel/status/1940385674881814660)
* [GitHub Repository](https://github.com/jmandel/regulations.gov-comment-browser/tree/main)

### Opportunity

* Integrating **Mirrulations** as the backend would upgrade the approach from “sipping” data to **“gulping”** it, enabling large-scale ingestion and querying.
* This could also support projects like **cross-docket data mining**, providing AI-driven insights across multiple regulatory topics.

### Options

1. **Build on Josh Mandel’s Work:** Adapt and enhance his existing stack with Mirrulations integration.
2. **Start Fresh:** Develop a new LLM-based system tailored for large-scale docket analysis and interactive Q\&A.

### Potential Outcome

A scalable LLM-powered interface to:

* Ingest and summarize full dockets.
* Respond to targeted queries about topics, entities, and comment content.
* Enable advanced cross-docket analysis.

**Goal:** Provide researchers, advocates, and policymakers with a powerful AI tool for exploring and understanding large regulatory datasets.
