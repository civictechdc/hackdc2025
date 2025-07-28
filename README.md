# Talk to me in Rules

-----

# Policy Comment Analyzer

This project leverages the Google Gemini API to automate the analysis of public comments on policy proposals. It ingests a policy document (HTML) and a collection of public comments (JSON files), then uses Gemini to:

1.  **Outline the policy**: Extracts key information such as the policy name, summary, objectives, proposed actions, affected stakeholders, and estimated impact.
2.  **Analyze comments**: Processes each public comment, identifying specific issues, their relation to policy sections, relevant excerpts, and sentiment.
3.  **Generate a comprehensive issues report**: Aggregates all identified issues, calculates overall sentiment for each issue, and lists referencing comments with excerpts.

## Features

  * **Gemini API Integration**: Utilizes `google.generativeai` for intelligent policy outlining and comment analysis.
  * **JSON Schema Validation**: Ensures structured and consistent output using predefined JSON schemas for policy outlines and issue reports.
  * **HTML & JSON Parsing**: Employs `BeautifulSoup` for robust extraction of text from HTML policy documents and handles nested JSON structures for comments.
  * **Automated Workflow**: Provides an end-to-end script to process inputs and generate a final report.
  * **Sentiment Analysis**: Categorizes the sentiment of comments and overall issues (positive, negative, neutral, mixed).

## Setup

### Prerequisites

  * Python 3.8+
  * Google Gemini API Key

### Installation

1.  **Clone the repository (if applicable) or save the provided code.**

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python packages**:

    ```bash
    pip install google-generativeai python-dotenv beautifulsoup4
    ```

4.  **Set up your Google Gemini API Key**:

      * Obtain an API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).
      * Create a file named `.env` in the root directory of your project.
      * Add your API key to the `.env` file like this:
        ```
        GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```
      * **Important**: Do not share your `.env` file or commit it to version control.

## Usage

### Input Data Structure

The script expects the following directory structure for input files:

```
.
├── .env
├── main.py                 (or your script name)
├── input_data/
│   ├── policy_file.htm     (Your policy document in HTML format)
│   └── comments/
│       ├── HHS-XXXX-YYYY-0001.json
│       ├── HHS-XXXX-YYYY-0002.json
│       └── ...
└── output/
    └── (This directory will be created, and the report saved here)
```

  * **`input_data/policy_file.htm`**: The HTML file containing the policy proposal text. The example uses `HHS-ONC-2019-0002-0001_content.htm`.
  * **`input_data/comments/`**: A directory containing public comments as JSON files. Each JSON file should have a structure from which the comment text can be extracted (e.g., `data.attributes.comment`). Filenames are used as comment IDs.

### Running the Script

1.  **Place your policy HTML file** into the `input_data/` directory.

2.  **Place your public comment JSON files** into the `input_data/comments/` directory.

3.  **Open the `main.py` (or your script name) file** and verify the `POLICY_FILE`, `COMMENTS_DIR`, and `OUTPUT_REPORT_FILE` paths in the `if __name__ == "__main__":` block. Adjust them if your file names or paths differ.

    ```python
    if __name__ == "__main__":
        POLICY_FILE = "input_data/HHS-ONC-2019-0002-0001_content.htm"
        COMMENTS_DIR = "input_data/comments"
        OUTPUT_REPORT_FILE = "output/issues_report.json"

        # Create dummy directories for demonstration if they don't exist
        os.makedirs(os.path.dirname(POLICY_FILE), exist_ok=True)
        os.makedirs(COMMENTS_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(OUTPUT_REPORT_FILE), exist_ok=True)

        create_issues_report(POLICY_FILE, COMMENTS_DIR, OUTPUT_REPORT_FILE)
    ```

4.  **Run the script** from your terminal:

    ```bash
    python main.py
    ```

The script will print progress updates to the console. Once completed, a JSON file named `issues_report.json` (or your specified output file) will be generated in the `output/` directory, containing the comprehensive issues report.

### Output Report Structure

The `issues_report.json` file will follow the `JSON_SCHEMA_ISSUES_LIST` structure, similar to this:

```json
{
  "policy_name": "Name of the Policy",
  "total_comments_processed": 123,
  "issues": [
    {
      "issue_id": "ISSUE_001",
      "description": "Description of the first issue identified.",
      "related_policy_sections": ["proposed actions", "summary"],
      "sentiment": "negative",
      "referencing_comments": [
        {
          "comment_id": "HHS-2022-0163-0002",
          "comment_file_name": "HHS-2022-0163-0002.json",
          "excerpt": "This part of the comment strongly opposes the proposed action...",
          "comment_sentiment": "negative"
        },
        {
          "comment_id": "HHS-2022-0163-0005",
          "comment_file_name": "HHS-2022-0163-0005.json",
          "excerpt": "Another comment also raised concerns about the same action...",
          "comment_sentiment": "negative"
        }
      ]
    },
    {
      "issue_id": "ISSUE_002",
      "description": "A different issue raised by public comments.",
      "related_policy_sections": ["estimated impact"],
      "sentiment": "positive",
      "referencing_comments": [
        {
          "comment_id": "HHS-2022-0163-0010",
          "comment_file_name": "HHS-2022-0163-0010.json",
          "excerpt": "The estimated positive impact is well received, according to this comment.",
          "comment_sentiment": "positive"
        }
      ]
    }
  ]
}
```

-----
