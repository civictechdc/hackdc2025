import argparse
import sys
from difflib import HtmlDiff
from src.trottertools.myDBTable import myDBTable
from src.trottertools.mySQLh import mySQLh
from src.trottertools.WriteOnceDict import WriteOnceDict
from src.import_regulation_json_into_DB import import_json_files
from src.duplicate_comment_detection import compare_strings

hDiff = HtmlDiff()


def main():
    parser = argparse.ArgumentParser(prog="bot_sub_detector", usage="%(prog) [options]")

    parser.add_argument(
        "import_data", type=str, help="Import Docket from JSON file to SQL Database"
    )
    parser.add_argument("diff", help="Run diff on imported docket data")

    args = parser.parse_args()

    print(args)

    if len(sys.argv) == 0:
        raise Exception("The import or diff command was not provided...")
        sys.exit(1)

    if args.import_data is not None:
        if len(sys.argv) < 2:
            raise Exception("A filename must be provided from import...")
            sys.exit(1)

        m_db = "mirrulation"
        comment_table = "comment_json"
        commentDBT = myDBTable.myDBTable(m_db, comment_table)

        import_json_files(args.import_data, commentDBT)

    if args.diff is not None:
        if len(sys.argv) < 3:
            raise Exception(
                "Input and Output tables must be defined when diffing data..."
            )
            sys.exit(1)
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
                    outside_row.simplified_comment_text,
                    inside_row.simplified_comment_text,
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
        mySQLh.runQuerys(sql_dict)
        sql_dict = WriteOnceDict.WriteOnceDict()

        # Mark current comment as processed
        list_of_done.append(o_id)


if __name__ == "__main__":
    main()
