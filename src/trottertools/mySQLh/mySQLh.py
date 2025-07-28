"""
mySQLh.py
A set of SQL helper functions, that is compatible with querpy
This one is for mysql
"""

import os
from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv


class mySQLh(object):
    def __init__(self):
        # we automatically use the .env file to connect to the datase.
        load_dotenv()  # means we will see the .env file as environment variables for os.getenv

        # have to have these three
        database = os.getenv("SQLITE_DB_FILE")

        # use sql alchemy to connect to the database and then keep the connection as an object variable.

        conn_string = f"sqlite:///{database}"
        print(conn_string)
        self.engine = create_engine(conn_string)
        self.conn = self.engine.connect()

    def runDictOfQuerys(
        self, query_dict, is_just_print=False, is_ignore_exception=False
    ):
        # This is just a wrapper for runQuerys
        self.runQuerys(query_dict, is_just_print, is_ignore_exception)

    def runListOfQuerys(
        self, query_list, is_just_print=False, is_ignore_exception=False
    ):
        # This is just a wrapper for runQuerys
        self.runQuerys(query_list, is_just_print, is_ignore_exception)

    def runQuerys(self, these_queries, is_just_print=False, is_ignore_exception=False):
        """
        Runs a dictoriary or list of queries against the spark SQL engine

        Arguments:
        these_queries -- a dictionary or a list of queries to run
        is_just_print -- will print the SQL instead of running it if True
        is_ignore_exception -- will prevent crashing due to SQL error if True

        """
        # this simple helper loops over a list of queries, prints them and shows the results
        # if you just want the loop to run the queries, then set is_just_print to true
        # This same function works on dictionaries too!! Should rename!!!
        #
        # We want to have only one code.. so we are going to convert all the list into a dict.
        if isinstance(these_queries, list):
            new_dict = {}
            i = 0
            for this_sql in these_queries:
                i = i + 1
                new_dict[i] = this_sql
            # finally reset these_queries to the new dictionary
            these_queries = new_dict

        # run this code against a series of dictionaries. First, make sure they are dictionaries.
        if isinstance(these_queries, dict):
            for this_label, this_sql in these_queries.items():
                print(this_label)
                print(this_sql)
                print("\n")
                if is_just_print:
                    # we do nothing, we have already printed
                    print("#not running sql")
                else:
                    print("running SQL command")
                    try:
                        # Todo mysql connection
                        self.conn.execute(text(this_sql))
                    except Exception as error:
                        # no matter what, we print the error!!
                        print(f"SQLh.runQuerys: Error in the SQL loop: \n", error)
                        if not is_ignore_exception:
                            # The user wants this error to stop the script execution
                            # So we just raise the error again
                            raise
                        else:
                            print(
                                "SQLh.runQuerys: is_ignore_exception is True. So we are continuing despite this error."
                            )

        else:
            # We have been passed something other than a list!!
            # That is fatal!
            print(these_queries)
            raise Exception(
                "The above was passed to SQLh.runListOfQueries but it is not a list or dict of queries!!!"
            )
