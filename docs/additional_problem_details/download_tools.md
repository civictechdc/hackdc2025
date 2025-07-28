## Improve the Download Tools

There are multiple tools for downloading Regulations.gov data, but many need refinement. Help us improve them!

### Existing Resources & Examples

* **Search Tool** – Created by Moravian students. (Not available for direct development, but serves as a good reference.)
* **Direct S3 Access** – Pull data directly into the analysis tool of your choice.
* **Subset Analysis** – Enable focused analysis on a specific docket or a small group of dockets.
* **Docket Relationships** – Explore how dockets connect to each other.

### Current Tools to Build On

* [**Download a single docket**](https://github.com/mirrulations/mirrulations-fetch) – Simplifies fetching a complete docket from the S3 mirror.
* [**Download a CSV file for a single docket**](https://github.com/mirrulations/mirrulations-csv) – Extracts text comments into an easy-to-analyze CSV.
* [**Bulk download tool**](https://github.com/ftrotter/regulation_comments_downloader) – Supports downloading large datasets.

### Areas for Improvement

* [**Import JSON into MySQL**](https://github.com/ftrotter/mirrulation_hacking/blob/main/import_regulation_json_into_DB.py) – Could be made more robust for production use and integrated into broader pipelines.

**Goal:** Create reliable, user-friendly tools that make downloading and working with dockets simple, whether for small-scale exploration or large-scale analysis.
