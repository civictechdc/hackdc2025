# DC-Hackathon-2025

## Regulatory Comment Linkage - Mirrulations Hackathon Project
This project aims to link public comments to the specific regulatory documents they respond to within a single docket, using a mix of metadata, time-window heuristics, and semantic similarity techniques.

### Inputs
- Single Docket dataset
- All regulatory documents (with metadata)
- All public comments for a docket (submitted directly or via attachments)

### Workflow
1. Document Inventory
   - Created an inventory of all documents in the docket with file metadata, document types, date posted, etc.
2. Comment Preprocessing
   - Prepared a clean dataset of comments and timestamps
3. Time-Window Matching
  - Sorted documents by posted_date, assigned sequential doc_order
  - Linked each comment to its most likely source document using pandas.cut() to bin comments into doc-based time intervals 
  - Inner merge to assign document to comment
4. Text Extraction
   - Extracted plain text from regulatory documents:
  - Added doc_text field to each document
5. Context Isolation
  - Isolated document sections between where a comment is referenced
6. Comment Matching
  - Compared each comment with extracted document sections:
    - used n-grams to find comment text within final rule

### Next Steps:
- Validate window matching logic for edge cases (e.g., comments right after a new rule is posted)
- De-duplicate/QC text extraction, especially for PDFs with encoding issues
- Analytics: topic modeling, keyword-in-context, clustering, sentiment tagging
- UI/UX: Build a searchable dashboard for policymakers, journalists, and researchers

### Contributors of this projects are
- Henry Ham
- Sridhar Gundumalla
- Kumar H
- Queyen Le
- Srishti Kama

https://files.slack.com/files-pri/T02GC3VEL-F097GGZBS5R/96cb94cb-e67e-484b-bdc5-8479b935d741.png
