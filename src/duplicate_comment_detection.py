"""
This script performs duplicate and similar comment detection across a database of comments.
It uses difflib to compare comments and identify those that are identical or very similar.

The script:
1. Reads comments from a source database table
2. Compares each comment with every other comment using string similarity matching
3. Records pairs of similar comments that exceed a similarity threshold
4. Stores the results in a clustering table for further analysis

Key Features:
- Uses difflib's SequenceMatcher for string similarity comparison
- Configurable similarity threshold (default 0.85)
- Supports different source/output table configurations via command line arguments
- Maintains a record of processed comments to avoid duplicate comparisons
- Batches database insertions for better performance

Database Schema Requirements:
- Source table with comment text
- uniquecomment table for storing unique comments
- comment_clusters table for storing similarity relationships
- uniquecomment_to_comment table for mapping between comments and unique comments

Usage:
    python duplicate_comment_detection.py [--comment_source_table TABLE] [--db DATABASE] [--output_table OUTPUT]
"""

from .trottertools.WriteOnceDict import WriteOnceDict
from .trottertools.myDBTable import myDBTable
from .trottertools.mySQLh import mySQLh
import os
import json
import sys
import sqlalchemy as db
import re
import difflib
from difflib import unified_diff
from sqlalchemy import select
from sqlalchemy import text
from difflib import HtmlDiff
import argparse


hdiff = HtmlDiff()


def compare_strings(str1, str2):
    """
    Compares two strings using difflib and returns a numerical score of their similarity.

    The function uses difflib's SequenceMatcher to compute a similarity ratio between
    two strings. The ratio is calculated based on the number of matching characters
    and their positions.

    Args:
        str1 (str): The first string to compare.
        str2 (str): The second string to compare.

    Returns:
        float: A numerical score between 0 and 1 representing the similarity between
              the two strings. A score of 1.0 indicates identical strings, while 0.0
              indicates completely different strings.
    """
    sequence_matcher = difflib.SequenceMatcher(None, str1, str2)
    return sequence_matcher.ratio()


if __name__ == "__main__":
    # Parse command line arguments for configurable table names and database
    parser = argparse.ArgumentParser(description="Process comments.")
    parser.add_argument(
        "--comment_source_table",
        type=str,
        default="comment",
        help="Name of the comment table",
    )
    parser.add_argument(
        "--db", type=str, default="mirrulation", help="Name of the database"
    )
    parser.add_argument(
        "--output_table",
        type=str,
        default="mirrulation",
        help="Name of the output table",
    )
    args = parser.parse_args()

    # Initialize database connections and table objects
    comment_table = args.comment_source_table
    m_db = args.db
    commentDBT = myDBTable.myDBTable(m_db, comment_table)

    unique_comment_DBT = myDBTable.myDBTable(m_db, "uniquecomment")
    cluster_DBT = myDBTable.myDBTable(m_db, "comment_clusters")
    unique_to_comment_DBT = myDBTable.myDBTable(m_db, "uniquecomment_to_comment")

    # Initialize WriteOnceDict for storing SQL queries
    sql_dict = WriteOnceDict.WriteOnceDict()

    # Load all unique comments from the database
    all_unique_comments = []
    is_first_run = True
    result = mySQLh._conn.execute(f"SELECT * FROM {unique_comment_DBT}")
    for unique_comment_row in result:
        all_unique_comments.append(unique_comment_row)

    # Set similarity threshold - comments with similarity score above this are considered duplicates
    threshold = 0.85

    # Track processed comments to avoid duplicate comparisons
    list_of_done = []

    # Main comparison loop - compare each comment with every other comment
    outer_i = 0
    for outside_row in all_unique_comments:
        outer_i = outer_i + 1
        print(f"\t\t\t\t\tLooping over outer: {outer_i}")
        inner_j = 0
        for inside_row in all_unique_comments:
            inner_j = inner_j + 1
            # Calculate similarity score between comments
            score = compare_strings(
                outside_row.simplified_comment_text, inside_row.simplified_comment_text
            )
            score = round(score, 4)

            # If similarity exceeds threshold, record the relationship
            if score > threshold:
                o_id = outside_row.id
                i_id = inside_row.id
                if i_id in list_of_done:
                    # Skip if this comment has already been processed in outer loop
                    pass
                else:
                    matching_string = f"Match between {o_id} and {i_id}"
                    print(matching_string)
                    print(outside_row.simplified_comment_text[:70])
                    print(inside_row.simplified_comment_text[:70])
                    print(f"Score: {score}")
                    if o_id != i_id:
                        # Store the relationship in the clusters table
                        # Note: diff_text calculation is commented out for performance
                        sql_dict[matching_string] = f"""
INSERT INTO {cluster_DBT}
(`unique_comment_id`, `other_unique_comment_id`, `score`, `diff_text`) 
VALUES ('{o_id}', '{i_id}', '{score}', NULL 
);
"""
                    else:
                        print("Everything always matches itself")

        # Execute stored SQL queries after each outer loop iteration
        mySQLh.runQuerys(sql_dict, is_just_print)
        sql_dict = WriteOnceDict.WriteOnceDict()

        # Mark current comment as processed
        list_of_done.append(o_id)
