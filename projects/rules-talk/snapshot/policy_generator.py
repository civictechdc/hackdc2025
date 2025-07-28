import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from bs4 import BeautifulSoup # For parsing HTML within the comment text AND policy file

# Load environment variables from .env file (for API key)
load_dotenv()

# --- Configuration ---
# Get your Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Please create a .env file with GEMINI_API_KEY=your_key_here"
    )

# Configure the Gemini API client
genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL_NAME = "gemini-1.5-flash"


# Define the JSON Schema for the policy outline (Existing)
JSON_SCHEMA_POLICY_OUTLINE = {
    "type": "object",
    "properties": {
        "policy_name": {
            "type": "string",
            "description": "A concise, descriptive name for the policy proposal."
        },
        "summary": {
            "type": "string",
            "description": "A brief overview of the policy, no more than 3-4 sentences."
        },
        "key_objectives": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of the main goals or aims the policy seeks to achieve."
        },
        "proposed_actions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of concrete steps, initiatives, or changes proposed by the policy."
        },
        "affected_stakeholders": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of groups, organizations, or entities that will be significantly impacted by the policy."
        },
        "estimated_impact": {
            "type": "string",
            "description": "A brief statement about the expected positive or negative effects or outcomes of the policy."
        }
    },
    "required": [
        "policy_name",
        "summary",
        "key_objectives",
        "proposed_actions",
        "affected_stakeholders",
        "estimated_impact"
    ]
}

# --- New JSON Schema for Identified Issues ---
JSON_SCHEMA_ISSUES_LIST = {
    "type": "object",
    "properties": {
        "policy_name": {
            "type": "string",
            "description": "The name of the policy being discussed."
        },
        "total_comments_processed": {
            "type": "integer",
            "description": "The total number of public comments analyzed."
        },
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue_id": {
                        "type": "string",
                        "description": "A unique identifier for the issue (e.g., 'ISSUE_001')."
                    },
                    "description": {
                        "type": "string",
                        "description": "A clear description of the issue raised."
                    },
                    "related_policy_sections": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific sections or aspects of the policy that this issue pertains to."
                    },
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "negative", "neutral", "mixed"],
                        "description": "Overall sentiment towards this issue based on comments."
                    },
                    "referencing_comments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "comment_id": {
                                    "type": "string",
                                    "description": "The identifier of the comment (from the 'id' field in the original JSON, e.g., 'CMS-2022-0163-0002')."
                                },
                                "comment_file_name": {
                                    "type": "string",
                                    "description": "The original filename of the comment JSON (e.g., 'comment_001.json')."
                                },
                                "excerpt": {
                                    "type": "string",
                                    "description": "A relevant excerpt from the comment related to this issue."
                                },
                                "comment_sentiment": {
                                    "type": "string",
                                    "enum": ["positive", "negative", "neutral"],
                                    "description": "Sentiment of this specific comment excerpt towards the issue."
                                }
                            },
                            "required": ["comment_id", "comment_file_name", "excerpt", "comment_sentiment"]
                        }
                    }
                },
                "required": ["issue_id", "description", "related_policy_sections", "sentiment", "referencing_comments"]
            }
        }
    },
    "required": ["policy_name", "total_comments_processed", "issues"]
}

# --- Utility to extract and clean comment text ---
def extract_and_clean_comment_text(comment_json: dict) -> str | None:
    """
    Extracts the comment text from the nested JSON structure
    and cleans up HTML tags.
    """
    try:
        html_comment = comment_json["data"]["attributes"]["comment"]
        soup = BeautifulSoup(html_comment, 'html.parser')
        clean_text = soup.get_text(separator=' ', strip=True)
        return clean_text
    except KeyError as e:
        print(f"Warning: KeyError in comment JSON structure: {e}. Skipping comment.")
        return None
    except Exception as e:
        print(f"Error extracting or cleaning comment text: {e}")
        return None

# --- Utility to extract and clean policy text from HTML ---
def extract_text_from_html_policy(filepath: str) -> str | None:
    """
    Loads an HTML file, extracts all visible text, and returns it.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        # Get all text, clean up extra whitespace
        clean_text = soup.get_text(separator=' ', strip=True)
        return clean_text
    except FileNotFoundError:
        print(f"Error: Policy HTML file not found at {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred reading or parsing policy HTML: {e}")
        return None

# --- Functions for File Operations ---
def save_json_file(data: dict, filepath: str):
    """Saves a dictionary as a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully saved output to {filepath}")
    except Exception as e:
        print(f"Error saving JSON to {filepath}: {e}")

def load_json_file(filepath: str) -> dict | None: # Added this back for clarity with save_json_file
    """Loads a JSON file and returns its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred loading {filepath}: {e}")
        return None
    
def load_comments_from_directory(directory_path: str) -> list[dict]:
    """
    Loads all JSON files from a specified directory as comments,
    extracting the 'id' (from filename) and cleaning the comment text.
    """
    comments = []
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at {directory_path}")
        return comments

    for filename in os.listdir(directory_path):
        # Filter for relevant JSON files (e.g., starts with "CMS-" and ends with ".json")
        # This also implicitly ignores files like .DS_Store
        if filename.startswith("CMS-") and filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            comment_raw_data = load_json_file(filepath)
            if comment_raw_data:
                # Use the filename (without extension) as the primary comment_id
                # This directly uses "CMS-2022-0163-0002" from the filename
                comment_id_from_filename = os.path.splitext(filename)[0]

                # Still extract and clean the actual comment text from the nested structure
                clean_comment_text = extract_and_clean_comment_text(comment_raw_data)

                # You can still use the 'id' from within the JSON for cross-validation if needed,
                # but for now, we prioritize the filename-derived ID.
                # json_internal_id = comment_raw_data.get("data", {}).get("id")
                # if json_internal_id and json_internal_id != comment_id_from_filename:
                #     print(f"Warning: Filename ID '{comment_id_from_filename}' mismatch with internal JSON ID '{json_internal_id}' for file {filename}")


                if clean_comment_text: # We now only need the text to be present
                    comments.append({
                        "comment_id": comment_id_from_filename, # Use filename-derived ID
                        "comment_file_name": filename,
                        "comment_text": clean_comment_text
                    })
                    print(f"DEBUG: Loaded comment {comment_id_from_filename} from {filename}")
                else:
                    print(f"DEBUG: Skipping comment file {filename}: Could not extract clean text.")
            else:
                print(f"DEBUG: Skipping comment file {filename}: Failed to load JSON content.")
    return comments


# --- Gemini API Functions ---
def generate_policy_outline(policy_text: str) -> dict | None:
    """
    Takes a policy text, sends it to Google Gemini, and
    returns a JSON outline based on the defined policy schema.
    """
    print(f"\n--- Sending policy text to Gemini ({GEMINI_MODEL_NAME}) for outlining... ---")
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME, system_instruction=(
            "You are an expert policy analyst AI. Your task is to extract "
            "the core components of a policy proposal and format them "
            "strictly as a JSON object according to the provided schema. "
            "Ensure all required fields are present and accurately reflect "
            "the policy text. Do not include any text outside the JSON."
        ))

        response = model.generate_content(
            policy_text,
            generation_config=genai.GenerationConfig(
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=JSON_SCHEMA_POLICY_OUTLINE
            )
        )
        return json.loads(response.text) # Ensure it's a Python dict

    except json.JSONDecodeError:
        print("Error: AI did not return valid JSON for policy outline.")
        print(f"AI raw response content: {response.text}") # DEBUG: UNCOMMENT THIS!
        return None
    except Exception as e:
        print(f"An unexpected error occurred during policy outlining: {e}")
        return None

def analyze_comment_for_issues(comment_text: str, policy_summary: str) -> dict | None:
    """
    Analyzes a single comment against the policy summary to identify issues,
    related policy sections, and sentiment.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME, system_instruction=(
            "You are an AI assistant specialized in analyzing public comments "
            "on policy proposals. Your task is to identify specific issues, "
            "concerns, or points of feedback raised in a comment relative to "
            "a given policy summary. For each issue, identify the relevant "
            "sections of the policy (if inferable), an excerpt from the comment "
            "that highlights the issue, and the sentiment of that excerpt. "
            "Output must be a JSON array of issues. If no issues are found, "
            "return an empty array. Do not include any text outside the JSON."
        ))

        comment_analysis_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue_description": {
                        "type": "string",
                        "description": "A concise description of the issue or feedback point."
                    },
                    "related_policy_aspect": {
                        "type": "string",
                        "description": "Which part of the policy (e.g., 'proposed actions', 'estimated impact', 'summary') this comment directly relates to. If general, state 'overall policy'."
                    },
                    "comment_excerpt": {
                        "type": "string",
                        "description": "A direct quote or paraphrase from the comment highlighting the issue."
                    },
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "negative", "neutral"],
                        "description": "The sentiment of the comment excerpt regarding the identified issue."
                    }
                },
                "required": ["issue_description", "related_policy_aspect", "comment_excerpt", "sentiment"]
            }
        }

        prompt = (
            f"Policy Summary: {policy_summary}\n\n"
            f"Public Comment: {comment_text}\n\n"
            "Analyze the above public comment in the context of the policy summary. "
            "Identify distinct issues or feedback points. For each, provide a "
            "brief description, the part of the policy it relates to, "
            "a relevant excerpt from the comment, and the sentiment of that excerpt."
        )

        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=comment_analysis_schema
            )
        )
        return json.loads(response.text)

    except json.JSONDecodeError:
        print(f"Error: AI did not return valid JSON for comment analysis for comment: {comment_text[:50]}...")
        print(f"AI raw response content: {response.text}") # Uncomment for debugging
        return None
    except Exception as e:
        print(f"An unexpected error occurred during comment analysis: {e}")
        return None

# --- Main Automation Logic ---
def create_issues_report(
    policy_filepath: str,
    comments_directory: str,
    output_filepath: str
):
    """
    Automates the process of ingesting policy and comments, analyzing them
    with Gemini, and generating a comprehensive issues report.
    """
    print("\n--- Starting Policy and Comment Analysis Project ---")

    # 1. Load and clean the Policy HTML file
    policy_text_for_gemini = extract_text_from_html_policy(policy_filepath)
    if not policy_text_for_gemini:
        print("Failed to load or parse policy HTML file. Exiting.")
        return
    print(f"DEBUG: Policy text extracted (first 500 chars): {policy_text_for_gemini[:500]}...")


    # Generate the initial policy outline
    policy_outline = generate_policy_outline(policy_text_for_gemini)
    if not policy_outline:
        print("Failed to generate policy outline. Exiting.")
        return

    policy_name = policy_outline.get("policy_name", "Unnamed Policy")
    policy_summary = policy_outline.get("summary", "")

    print(f"\nSuccessfully outlined policy: {policy_name}")
    print(f"Policy Summary: {policy_summary}")

    # 2. Load Public Comments
    comments_data = load_comments_from_directory(comments_directory)
    if not comments_data:
        print("No comments found or loaded. Exiting.")
        return
    print(f"\nLoaded {len(comments_data)} public comments.")

    # 3. Analyze Comments and Aggregate Issues
    comprehensive_issues = {} # Use a dictionary to store unique issues
    issue_counter = 0

    for i, comment_entry in enumerate(comments_data):
        comment_id = comment_entry.get('comment_id', f'unknown_id_{i}')
        comment_file_name = comment_entry.get('comment_file_name', f'unknown_file_{i}.json')
        comment_content = comment_entry.get('comment_text')

        if not comment_content:
            print(f"Warning: Comment '{comment_file_name}' (ID: {comment_id}) has no extractable text. Skipping.")
            continue

        print(f"Processing comment {i+1}/{len(comments_data)}: {comment_file_name} (ID: {comment_id})")
        analyzed_issues_from_comment = analyze_comment_for_issues(comment_content, policy_summary)

        if analyzed_issues_from_comment:
            for issue_from_comment in analyzed_issues_from_comment:
                issue_description = issue_from_comment.get("issue_description")
                comment_excerpt = issue_from_comment.get("comment_excerpt")
                comment_sentiment = issue_from_comment.get("sentiment")
                related_policy_aspect = issue_from_comment.get("related_policy_aspect")

                # Normalize issue description for better grouping
                normalized_issue_key = issue_description.lower().strip()

                if normalized_issue_key not in comprehensive_issues:
                    issue_counter += 1
                    issue_id = f"ISSUE_{issue_counter:03d}"
                    comprehensive_issues[normalized_issue_key] = {
                        "issue_id": issue_id,
                        "description": issue_description,
                        "related_policy_sections": [related_policy_aspect] if related_policy_aspect else [],
                        "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0}, # For calculating overall sentiment
                        "referencing_comments": []
                    }

                # Add comment reference
                current_issue = comprehensive_issues[normalized_issue_key]
                current_issue["referencing_comments"].append({
                    "comment_id": comment_id,
                    "comment_file_name": comment_file_name,
                    "excerpt": comment_excerpt,
                    "comment_sentiment": comment_sentiment
                })

                # Update sentiment scores for overall issue sentiment calculation
                if comment_sentiment in current_issue["sentiment_scores"]:
                    current_issue["sentiment_scores"][comment_sentiment] += 1

                # Add related policy aspect if not already present
                if related_policy_aspect and related_policy_aspect not in current_issue["related_policy_sections"]:
                    current_issue["related_policy_sections"].append(related_policy_aspect)

    # 4. Finalize Issues List and Calculate Overall Sentiment
    final_issues_list = []
    for issue_key, issue_data in comprehensive_issues.items():
        # Calculate overall sentiment for the issue
        sentiment_scores = issue_data.pop("sentiment_scores") # Remove temporary field
        total_sentiment_comments = sum(sentiment_scores.values())
        if total_sentiment_comments > 0:
            pos_ratio = sentiment_scores["positive"] / total_sentiment_comments
            neg_ratio = sentiment_scores["negative"] / total_sentiment_comments

            if pos_ratio > 0.6 and neg_ratio < 0.2: # Mostly positive
                issue_data["sentiment"] = "positive"
            elif neg_ratio > 0.6 and pos_ratio < 0.2: # Mostly negative
                issue_data["sentiment"] = "negative"
            elif pos_ratio > 0.2 and neg_ratio > 0.2: # Significant positive and negative
                issue_data["sentiment"] = "mixed"
            else:
                issue_data["sentiment"] = "neutral"
        else:
            issue_data["sentiment"] = "neutral" # Default if no sentiment comments

        final_issues_list.append(issue_data)

    # Sort issues by their ID for consistent output
    final_issues_list.sort(key=lambda x: x['issue_id'])

    # 5. Construct the Final Output JSON
    output_report = {
        "policy_name": policy_name,
        "total_comments_processed": len(comments_data),
        "issues": final_issues_list
    }

    # 6. Save the Output
    save_json_file(output_report, output_filepath)
    print("\n--- Project Completed. Issues Report Generated ---")

# --- Example Usage ---
if __name__ == "__main__":
    # Define your input and output paths

    POLICY_FILE = "input_data/CMS-2022-0163-0001_content.htm" # Changed to .htm
    COMMENTS_DIR = "input_data/comments"
    OUTPUT_REPORT_FILE = "output/issues_report.json"

    # Create dummy directories and files for demonstration if they don't exist
    os.makedirs(os.path.dirname(POLICY_FILE), exist_ok=True)
    os.makedirs(COMMENTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_REPORT_FILE), exist_ok=True)

    create_issues_report(POLICY_FILE, COMMENTS_DIR, OUTPUT_REPORT_FILE)