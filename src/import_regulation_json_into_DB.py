"""--- import_regulation_json_into_DB.py -----
Import JSON Comment Files to MySQL Database

This script imports JSON files containing comment data into a MySQL database. It processes JSON files
from a specified directory, extracts comment data, performs text cleanup, and stores the results
in a MySQL database table named 'comment_json'.

Features:
- Strips HTML tags from comment text
- Simplifies whitespace in comments
- Splits sentences onto separate lines for easier diff comparison
- Handles JSON parsing errors and database insertion errors gracefully
- Uses SQLAlchemy for safe database operations

Dependencies:
- trottertools.WriteOnceDict: Custom dictionary implementation
- trottertools.myDBTable: Database table operations
- trottertools.mySQLh: MySQL connection handling
- sqlalchemy: SQL database toolkit
- os, json, sys, re: Standard Python libraries
- html.parser: HTML parsing functionality

Usage:
    python import_json.py <directory_path>

Where:
    directory_path: Path to directory containing JSON files to process
"""

from .trottertools.WriteOnceDict import WriteOnceDict
from .trottertools.myDBTable import myDBTable
from .trottertools.mySQLh import mySQLh
import os
import json
import sys
import sqlalchemy as db
import re

from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    """
    HTML Parser subclass that strips HTML tags from text.

    This class is used to remove HTML markup from comment text while preserving
    the actual content. It accumulates text content in a StringIO buffer.

    Source: https://stackoverflow.com/a/925630/144364
    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        """Accumulate non-markup text in the StringIO buffer."""
        self.text.write(d)

    def get_data(self):
        """Retrieve the accumulated text content."""
        return self.text.getvalue()


def strip_tags(html):
    """
    Remove HTML tags from a string by using the MLStripper class above.

    Args:
        html (str): HTML-formatted string

    Returns:
        str: Text content with HTML tags removed
    """
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def import_json_files(directory, commentDBT):
    """
    Import JSON files from a directory into the comment_json database table.

    This function:
    1. Connects to the MySQL database
    2. Iterates through JSON files in the specified directory
    3. Processes each file to extract comment data
    4. Cleans and formats the comment text
    5. Inserts the data into the database

    Args:
        directory (str): Path to directory containing JSON files
        commentDBT (myDBTable): Database table object for comments

    Returns:
        list: List of processed JSON objects (currently empty, placeholder for future use)
    """
    SQLh = mySQLh.mySQLh()
    json_objects = []
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return json_objects

    meta_data = db.MetaData(bind=SQLh._engine)
    db.MetaData.reflect(meta_data)

    commentTable = meta_data.tables["comment_json"]

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r") as file:
                    data = json.load(file)
                    commentId = data["data"]["id"]

                    # Strip HTML tags from the raw comment text
                    comment_text = strip_tags(data["data"]["attributes"]["comment"])

                    # Normalize whitespace and format for readability
                    simplified_comment_text = " ".join(
                        comment_text.split(" ")
                    )  # Whitespace normalization
                    # Split sentences onto separate lines for easier diff viewing
                    simplified_comment_text = re.sub(
                        r"([.?!])", r"\1\n", simplified_comment_text
                    )

                    # Insert into database using SQLAlchemy, with IGNORE to handle duplicates
                    stmt = (
                        db.insert(commentTable)
                        .values(
                            commentId=commentId,
                            comment_on_documentId=data["data"]["attributes"][
                                "commentOnDocumentId"
                            ],
                            comment_text=comment_text,
                            simplified_comment_text=simplified_comment_text,
                            comment_date_text=data["data"]["attributes"]["modifyDate"],
                        )
                        .prefix_with("IGNORE")
                    )

                    print(f"Inserting {commentId}")
                    SQLh._conn.execute(stmt)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file {filepath}")
            except db.exc.SQLAlchemyError as e:
                print(f"Tried and got\n {e}")
            except Exception as e:
                print(f"Error with file {filepath}: {e}")


if __name__ == "__main__":
    # Initialize database connection
    m_db = "mirrulation"
    comment_table = "comment_json"
    commentDBT = myDBTable.myDBTable(m_db, comment_table)

    # Validate command line arguments
    if len(sys.argv) < 2:
        print("Usage: python import_regulation_json_into_DB.py <directory_path>")
        sys.exit(1)

    # Process files from specified directory
    directory_path = sys.argv[1]
    import_json_files(directory_path, commentDBT)
