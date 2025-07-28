## Topic Extraction & Sentiment Analysis

### Problem

Searching regulatory data is challenging for those unfamiliar with policy-specific language. In healthcare, for instance, terms like “Meaningful Use,” “interoperability,” “information blocking,” “FHIR,” and “Electronic Healthcare Records” are often used interchangeably or in related contexts. Policy experts know these terms, but journalists, advocates, or newcomers frequently do not know which keywords to use when navigating dockets or comment data.

### Key Questions

* Can we automate the discovery of related or synonymous regulatory terms, starting from a single keyword?
* How can we surface adjacent regulatory topics that broaden the context for analysis?

### Proposed Approach

* Use NLP techniques to extract key topics and terms from regulatory text and comments.
* Build a **topic graph** that connects synonymous, related, and adjacent terms to help non-experts explore regulatory themes.

### Sentiment Analysis on a Topical Basis

It’s not enough to assess the overall mood of commenters; we need context-specific sentiment. For example:

* Which topics do commenters support or oppose?
* How do stances on one policy (e.g., Policy A) correlate with views on related policies (e.g., Policies B and C)?

### Potential Outcome

An enriched dataset providing:

* **Topic extraction** for regulatory language mapping.
* **Contextual sentiment analysis** showing how commenters feel about specific policies and how those opinions relate across topics.

**Goal:** Create tools that make regulatory data more accessible and insightful for both experts and newcomers.
