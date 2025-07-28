## Within Docket Dataset: Coordinated Commenting Detection

### Problem

Organizations often coordinate comment submissions to amplify their positions in the regulatory process. While legitimate and common, this practice can become problematic when submissions use fraudulent identities or are crafted to obscure their coordinated nature.

### Examples

* **Legitimate coordination:** Members of an advocacy group submitting similar comments to show broad support.
* **Fraudulent activity:** ISPs submitting comments using identities of deceased or non-existent individuals during the [Net Neutrality proceedings](https://www.wired.com/story/isps-funded-85-million-fake-comments-opposing-net-neutrality/).
* **High-profile instance:** [John Oliver encouraging mass submissions on Network Neutrality](https://en.wikipedia.org/wiki/Net_Neutrality_%28Last_Week_Tonight_with_John_Oliver%29).

### Detection Challenges & Patterns

* Large blocks of identical or near-identical text across submissions.
* Templates with placeholders (“enter your story here”) combined with unique personalized additions.
* Multiple organizations using shared templates with minor rewrites to obscure their coordinated origin.
* Anticipation of LLM-generated comment permutations designed to appear unique while conveying the same core position.

### Need

* Detect and classify coordinated campaigns.
* Distinguish between organic grassroots campaigns and fraudulent or manipulated submissions.
* Identify aligned groups based on shared comment structures and content.

### Resources

* [Initial code for duplicate detection (prototype)](https://github.com/ftrotter/mirrulation_hacking)

**Outcome:** Tools to detect, classify, and analyze coordinated commenting efforts, improving transparency in regulatory engagement.
