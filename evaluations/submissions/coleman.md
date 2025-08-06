# Civic Hack DC 2025 – Evaluation Submission

**Evaluator Name:** Ben Coleman

**Organization:** Moravian University

**Date:** 2025-08-02

---

## Project Scores

### Project: canOfSpam

* **Impact & Relevance (20%):** 4.5/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 3/5
* **Comments:**

  * This project was one that we put out to the groups, and I was pleased to see someone explore the topic.
  * Minimal documentation
  * Code contains developer-specific paths, so hard to re-use
  * From the presentation at the event, they did hash of text rather than a full analysis of timestamps.  This approach is limited in that it only shows exact duplicates.  Extension to consider similarity (as opposed to equality) would be helpful.
  * There is good potential here: a dashboard to show how many unique comments and how many in each duplicate group.

---

### Project: entity-resolution-team

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 2/5
* **Open Source Practices (15%):** 1/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:**

  * Code in a Jupyter notebook, no supporting files
  * No documentation
  * They looked for emails (via regex) and grouped by domain
  * Interesting way to identify organizations that submit multiple comments that are not duplicate.

---

### Project: expanded-search

* **Impact & Relevance (20%):** /5
* **Novelty (20%):** /5
* **Amplification (15%):** /5
* **Open Source Practices (15%):** /5
* **Usability & Design (15%):** /5
* **Continuity Potential (15%):** /5
* **Comments:**

  * Not presented at the event
  * Looks like a search front end - similar to what Moravian did during the Spring 2025 semester.

---

### Project: hive-partitioned-parquet

* **Impact & Relevance (20%):** 5/5
* **Novelty (20%):** 4/5
* **Amplification (15%):** 5/5
* **Open Source Practices (15%):** 4/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 3/5
* **Comments:**

  * This project has significant potential for the mirrulations ecosystem.  Since the event, I used ideas from this project to explore how to store a parquet representation of the data in the S3 bucket.
  * The actual code in the project is limited, but the idea here is incredibly valuable.

---

### Project: llmgov

* **Impact & Relevance (20%):** 5/5
* **Novelty (20%):** 5/5
* **Amplification (15%):** 5/5
* **Open Source Practices (15%):** 4/5
* **Usability & Design (15%):** 4/5
* **Continuity Potential (15%):** 4/5
* **Comments:**

  * The RAG transformation process is another incredibly valuable contribution to the mirrulations ecosystem.
  * The code to transform data into vector embeddings could readily be incorporated into the mirrulations ETL process
  * The example LLM queries are instructive.  I am curious how well this will scale too *all* the data.

---

### Project: mirrulations-cli

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 5/5
* **Open Source Practices (15%):** 5/5
* **Usability & Design (15%):** 4/5
* **Continuity Potential (15%):** 3/5
* **Comments:**

  * This project was a wonderful extension of the work I did in preparation for the event.  It makes the mirrulations-fetch and mirrulations-csv tools easier to obtain and use.
  * I will incorporate this approach with the tools (Jay and I plan to work together to transfer ownership of the PyPi package).

---

### Project: rules-talk

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 4/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 3/5
* **Usability & Design (15%):** 4/5
* **Continuity Potential (15%):** 3/5
* **Comments:**

  * Processes the HTM file - something we haven't worked with yet.
  * Using LLMs to perform a type of sentiment analysis is an interesting approach.  I don't know a lot about this, but I wonder how reliable it will be.  It certainly could be a way to identify ideas within a docket to explore further - i.e. the LLM finds a pattern, and then a human goes in to explore in more detail.

---

### Project: taskmasters

* **Impact & Relevance (20%):** 3/5
* **Novelty (20%):** 3/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:**

  * minimal documentation
  * main folder and sub-folders appear to be different sub-projects, not unified
  * Work on docx is interesting - something we haven't considered yet but want to.
  * Mix of Jupyter and straight Python is hard to syntesize

---

### Project: team-topic-modeling

* **Impact & Relevance (20%):** 3/5
* **Novelty (20%):** 1/5
* **Amplification (15%):** 1/5
* **Open Source Practices (15%):** 1/5
* **Usability & Design (15%):** 1/5
* **Continuity Potential (15%):** 1/5
* **Comments:**

  * No doc, all code in one file
  * Uses spacey to do basic analysis
  * I don't see anything new here

---

### Project: team-velogear

* **Impact & Relevance (20%):** 1/5
* **Novelty (20%):** 1/5
* **Amplification (15%):** 1/5
* **Open Source Practices (15%):** 4/5
* **Usability & Design (15%):** 3/5
* **Continuity Potential (15%):** 1/5
* **Comments:**

  * Tool to process 1 pdf file at a time
  * No integration with mirrulations concepts
  * Just a wrapper around a pdf tool
  * Well-presented project, but doesn't advance the mirrulations ecosystem

---

### Project: the-scrapers

* **Impact & Relevance (20%):** 4/5
* **Novelty (20%):** 4/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 4/5
* **Comments:**

  * Limited documentation, which is unfortunate.  This project produced valuable insights to the broader mirrulations ecosystem.
  * Understanding that SEC does **NOT** have an API and FCC **DOES** is valuable if we decide to expand the data to beyond regulations.gov
  * The work uncovered an attempt by the SEC to block scrapers.  While it was frustrating during the event, understanding this space is a valuable contribution (I wish it had been documented).
  * Similarly, I want to understand the format of the FCC data more so we can contemplate its compatibility with the current bucket structure.

---

### Project: uspf1

* **Impact & Relevance (20%):** 2/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 2/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 2/5
* **Comments:**

  * Tag generation for dockets would be incredibly valuable for the mirrulations ecosystem
  * The source code doesn't seem to match the description - or the results in the README.  The code seems to use an LLM to determine if text is from a letter or to get "specific information requested."
  * The results in the README don't look like tags that expand what information can be informed from the organization and title of the docket.

---

### Project: within-docket-dataset

* **Impact & Relevance (20%):** 3/5
* **Novelty (20%):** 2/5
* **Amplification (15%):** 3/5
* **Open Source Practices (15%):** 2/5
* **Usability & Design (15%):** 2/5
* **Continuity Potential (15%):** 3/5
* **Comments:**

  * This project aims to identify changes in proposed rules (i.e. diff between V1 and V2 of a proposal) and then find comments that influenced this change.  This would be incredibly valuable, but is incredibly hard to accomplish.
  * Steps are documented at a high level, but not technical details are included.  From a scan of the Jupyter notebook, I don't see how they are identifying changes to the proposal.
  * Great idea, but I don't see a lot of delivered results addressing the (significant) challenges in this space.

---

## Overall Feedback
