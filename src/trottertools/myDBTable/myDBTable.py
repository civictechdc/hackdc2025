
import datetime
import importlib
from importlib import util as iutil

class myDBTable(object):

    def __init__(self,database_name: str,table_name: str):
        #by setting these, instead of _db.. we enforce naming conventions with the getter and setters below...
        self.db = database_name
        self.table = table_name

    ### Methods that help convert this object to a string in different circumstances
    def __str__(self):
        #Converts this object into a string of the format catalog.db.table
        #This is really the only reason to even have this class...
        return f"{self._db}.{self._table}"    

    def __format__(self, format_spec):
        #to work with f strings, we must also have the '__format__ magic function
        return self.__str__() 
  
    def __repr__(self):
        # Not sure when this one is used.. but we want it the same
        return self.__str__() 


    
    @property
    def database(self):
        #getter for database name if you want to say 'database'
        return self._db
              
    @database.setter
    def database(self,this_database_name: str):
        #setter for database name if you want to say 'database'

        if self._is_valid_database_name(this_database_name):
            self._db = this_database_name
        else:
            raise ValueError(f"There was a problem with the database name")
    
    
    @property
    def db(self):
        #getter for database name if you want to say 'db'
        return self._db
             
    @db.setter
    def db(self,this_database_name: str):
        
        if self._is_valid_database_name(this_database_name):
            self._db = this_database_name
        else:
            raise ValueError(f"There was a probelm with the database name")
            
    
    @property
    def table(self):
        #getter for table name
        return self._table
            
    @table.setter
    def table(self,this_table_name: str):
        #setter for table name

        if self._is_valid_table_name(this_table_name):
            self._table = this_table_name
        else:
            raise ValueError(f"There was a probelm with the table name")


    #TODO make some sensible rules for database and table names..
    #for instance.. can we forbid spaces?? Probably not...
    #enforce rules for table names..

    ### Rules for what acceptable table names (etc) look like
    def _is_valid_table_name(self,this_table_name: str):
        if self._is_longer_than_one_character(this_table_name):
            return True
        else:
            return False
         
    def _is_valid_database_name(self,this_database_name: str):
        #enforce rules for database names..
        if self._is_longer_than_one_character(this_database_name):
            return True
        else:
            return False

    def _is_longer_than_one_character(self,this_string: str):
        if len(this_string) > 0:
            return True
        else:
            return False

    ### Data inspection methods
    def getColumnList(self):
        #returns the column list of the current version of the data
        #remimplement for mysql
        pass

    def does_exist(self, is_force_true = False):
        #Does this table exist. 
        #reimplement for mysql
        #remimplement for mysql
        pass


    ### Meta helper methods (typically return more instances of DBTables)
    def return_matching_tables(self, is_force_true: bool = False):
        # Treat this DB table as a prefix. Return a list of DBTables that match that prefix
        #remimplement for mysql
        pass

    def createChild(self, table_extenstion: str):
        # This method returns a new DBTable that is identical to this one, but has a table name that has been extended
        # with the table_extension argument

        if len(table_extenstion) == 0:
            #This would essentially copy the DBTable.. which is weird.
            raise ValueError("DBTable: return_matching_tables: tried to create a new DBTable with an empty string. ")
        
        new_table = self.table + table_extenstion # build the new table name.. which is the old one plus the extension argument.
        return_me_DBTable = DBTable(self.db,new_table)
        return(return_me_DBTable)
    


