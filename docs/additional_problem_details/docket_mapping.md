## Across Docket Dataset: Basic Regulatory Sequence Map

### Problem

It is surprisingly difficult to determine which dockets are connected to earlier or later stages of the same regulatory process. For example, given a docket covering a specific topic, identifying its related RFIs, proposed rules, and final rules is often unclear and undocumented.

### Key Questions

* Given a docket that covers a specific regulatory topic, what previous or subsequent dockets should be examined?
* How do we systematically link related dockets across different stages of rulemaking?

### Proposed Approach

* Build a **“topical graph”** of connected dockets, mapping relationships across stages (e.g., RFI → Proposed Rule → Final Rule).
* Store this as a structured dataset in S3 for easy querying and integration into analysis pipelines.

### Potential Outcome

A **Connected Dockets Dataset** that allows researchers, advocates, and policymakers to navigate the regulatory timeline, understand relationships between dockets, and discover relevant historical context.

**Goal:** Provide a foundational map for cross-docket analysis to enhance regulatory research and engagement.
