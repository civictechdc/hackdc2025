"""
The Query class is intended to provide a high level interface for
building/editing SQL queries.

Example usage:
    >>> new_query = Query()
    >>> new_query.f += 'ex_db.dbo.ex_table AS tbl'
    >>> new_query.s += ['col1', 'col2', 'col3']  # can take lists
    >>> new_query.s += 'col4'  # can take single strings
    >>> new_query.w += 'col1 = 1'
    >>> new_query.w &= 'col2 IS NULL'  # handles &= and |= operators
    >>> print new_query
    >>> new_query  # should print full query
"""

__author__ = 'Paul Garaud, Fred Trotter'
__version__ = '0.2'
__date__ = '2022-06-18'


import re


class Query(object):

    # A series of precompiled regex to perfom various SQL related string tasks

    # These help with merging all of the statements into a single line
    whitespace_regex = re.compile('(^\s+|(?<=\s)\s+|\s+$)')
    #the design of the where list is such that every element of the list has an 'AND' or 'OR' as a prefix..
    #but the first one after the where does not need that.. so we just look for a WHERE OR or a WHERE AND and remove the 'OR' or 'AND'
    where_clean_up = re.compile('(?<=WHERE )\s.*?AND|(?<=WHERE )\s.*?OR') 

    # All of these fmt_(something) help with the SQL pretty print implementation
    fmt = re.compile('\s(?=FROM)|\s(?=WHERE)|\s(?=GROUP BY)')
    fmt_after = re.compile(
        '(?<=SELECT)\s|(?<=FROM)\s|(?<=WHERE)\s|(?<=GROUP BY)\s'
    )
    fmt_join = re.compile(
        '\s(?={l} JOIN)|\s(?={o} JOIN)|\s(?={r} JOIN)'
        '|\s(?={i} JOIN)|(?<!{l})\s(?=JOIN)|(?<!{r})\s(?=JOIN)'
        '&(?<!{i})\s(?=JOIN)&(?<!{o})\s(?=JOIN)'.format(
            r='RIGHT', l='LEFT', i='INNER', o='OUTER'
        )
    )
    fmt_commas = re.compile('(?<=,)\s')
    fmt_and = re.compile('(?<=WHERE).*$', flags=re.S)
    fmt_or = re.compile('\sOR\s')




    def __init__(self):
        self.ci = CreateInsertComponent()
        self.s = SelectComponent()
        self.f = QueryComponent('FROM')
        self.j = JoinComponent()
        self.w = WhereComponent()
        self.g = QueryComponent('GROUP BY', sep=',')
        self.o = QueryComponent('ORDER BY', sep=',')
        self.l = LimitComponent()


    @property
    def statement(self):
        # Merges the various SQL componenets into a single SQL statement
        elements = [self.ci(), self.s(), self.f(), self.j(), self.w(), self.g(), self.o(), self.l()]
        full_statement = re.subn(self.where_clean_up, '', ' '.join(elements))[0] # removes messy contents of WHERE statements? Note sure why this is needed or why it is run on the whole SQL statement
        full_statement = re.subn(self.whitespace_regex, '', full_statement)[0]  # flattens pretty print SQL to a single line by removing whitespace
        if full_statement:
            #Then our regex and merging has worked and return the single line of SQL
            return full_statement
        else:
            return ''

    #Some properties that allow us to expose some of the variables in the QueryComponents, as thought they were 
    #directly on the main Query object

    @property
    def is_first_data_add(self):
        return self.ci.is_first_data_add

    @is_first_data_add.setter
    def is_first_data_add(self, value):
        self.ci.is_first_data_add = value

    @property
    def distinct(self):
        return self.s.distinct

    @distinct.setter
    def distinct(self, value):
        self.s.distinct = value

    @property
    def top(self):
        return self.s.top

    @top.setter
    def top(self, value):
        self.s.top = value

    @property
    def join_type(self):
        """
        join_type prepends the type before each 'JOIN'
        """
        return self.j.join_type

    @join_type.setter
    def join_type(self, value):
        self.j.join_type = value

    def __str__(self):
        # When we just print the object, we want to assume that we will pretty-print the SQL.
        # This section handles the conversion of the single line query, into a pretty printed version..
        # This section could be better implemented using a call to sqlpars
        # https://github.com/andialbrecht/sqlparse
        # But doing it this way keeps the dependancies low, which is important
        query = self.statement  # This is the single line query gotten from the statement function
        query = re.subn(self.fmt, '\n  ', query)[0]
        query = re.subn(self.fmt_after, '\n    ', query)[0]
        query = re.subn(self.fmt_join, '\n      ', query)[0]
        query = re.subn(self.fmt_commas, '\n    ', query)[0]
        query = re.subn(self.fmt_and, Query.replace_and, query)[0]
        query = re.subn(self.fmt_or, '\n      OR ', query)[0]
        
        return query

    __repr__ = __str__


    @staticmethod
    def build_join(*args):
        # A static helper function to build a join
        # this assumes that the first argument is the table...
        # and that every subsequent pair of arguments is something to join 'ON'

        tbl_name = args[0]
        args = args[1:]
        if len(args) % 2 != 0 or args == ():
           raise BaseException(
              'You must provide an even number of columns to join on.'
           )

        args_expr = ['{0} = {1}'.format(args[2 * i], args[2 * i + 1]) 
            for i in range(int(len(args) / 2))]  # int() for Python 3
        args_expr = ' AND '.join(args_expr)
        join_str = ' '.join([tbl_name, 'ON', args_expr])

        return join_str

    @staticmethod
    def replace_and(match):
        """
        helper function for indenting AND in WHERE clause
        """
        string = match.group(0)
        raw_newlines = re.subn('AND', '\n      AND', string)[0]
        out = re.subn('(?<=BETWEEN)( \w+? )\n\s*?(AND)', r'\1\2', raw_newlines)[0]
        return out




class QueryComponent(object):
    #This is the base class that everything else will be added to..
    # this is where the magic of += is handled, which makes it easy 
    # to add things quickly to any componene of the overall query..

    def __init__(self, header, sep=''):
        self.header = header + ' '
        self.components = list()
        self.sep = sep + ' '

    def __iadd__(self, item):
        self.add_item(item)
        return self

    __iand__ = __ior__ = __iadd__  # lets set the default for &= and |= to be just += to start..

    def add_item(self, item, prefix=''):
        if prefix:
            prefix = prefix + ' '
        if type(item) == str:
            self.components.append(''.join([prefix, item]))
        elif type(item) == list:
            items = [''.join([prefix, i]) for i in item]
            self.components.extend(items)
        else:
            raise ValueError('Item must be a string or list')

    def clear(self):
        self.components = list()

    def __call__(self):
        # This is the function that converts the list of items in the querycomponent into a long string
        # it is always prefixed by the header..
        if self.components:
            return self.header + self.sep.join(self.components)
        return ''

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value

    def __str__(self):
        to_print = list()
        for n, c in enumerate(self.components):
            to_print.append("{0}: '{1}'".format(n, c))
        return 'index: item\n' + ', '.join(to_print)

    __repr__ = __str__

class CreateInsertComponent(QueryComponent):
    # Implements the very first part of a CREATE TABLE db.table AS or INSERT INTO db.table
    # depending on whether the is_first_data_add setting has been set
    # TODO the way this works now, you have to set is_first_data_add BEFORE adding the table
    # But it should not care whether it was added first or second.. the is_first_data_add 
    # Should swap between CREATE TABLE and INSERT INTO whenever it is set..
    # Which means that the behavior of setting the header should happen when the data is being read.. not when it is written...

    is_first_data_add = True

    def __iadd__(self, item):
        #we only have the one item.. 
        self.components = list() # overwrites whatever was there
        if self.is_first_data_add:
            #Then this is a CREATE TABLE AS clause
            self.header = 'CREATE TABLE ' + item + " AS \n" 
        else:
            self.header = 'INSERT INTO ' + item + " \n"
        return self

    def __init__(self):
        self.header = '' # by default, this is not used.
        self.components = list()

    def __call__(self):
        return self.header


class LimitComponent(QueryComponent):
    # Adds support for the limit command

    def __iadd__(self, item):
        #we only have the one item.. should be like '10, 100'
        #we should add a test to make sure this is correct. 
        self.components = list() # overwrites whatever was there
        self.components.append(item) 
        self.header = " LIMIT " 
        self.sep = ''
        return self

    def __init__(self):
        self.header = '' # by default, this is not used.
        self.components = list() # none to start


class SelectComponent(QueryComponent):
    # This models the SELECT component, and sends great energy ensuring that the "DISTINCT" and "TOP" syntax are supported
    # otherwise the actual columns are just stored as a list, which is handled by the parent class.

    header = 'SELECT'
    dist_pattern = re.compile(' DISTINCT')
    top_pattern = re.compile(' TOP \d+')

    def __init__(self):
        self.header = self.header + ' '
        self.components = list()
        self.dist = False
        self.topN = False
        self.sep = ', '

    def clear(self):
        self.components = list()
        self.dist = False
        self.topN = False

    @property
    def distinct(self):
        return self.dist

    @distinct.setter
    def distinct(self, value):
        if type(value) != bool:
            raise ValueError('distinct may only be set to True or False.')

        # remove DISTINCT from header if self.dist changed from True to False
        if self.dist != value:
            if self.dist:
                self.header = re.sub(self.dist_pattern, '', self.header)
            else:
                self.header += 'DISTINCT '

        self.dist = value

    @property
    def top(self):
        return self.topN

    @top.setter
    def top(self, value):
        if type(value) != int and value is not False:
            raise ValueError('top must be set to an integer or None')

        # remove TOP N from header if self.top changed to None
        if self.topN != value:
            if self.topN:
                self.header = re.sub(self.top_pattern, '', self.header)
            else:
                self.header += 'TOP ' + str(value) + ' '

        self.topN = value
        

class JoinComponent(QueryComponent):
    # like most query components, the joins are just a list of strings...
    # The exception is that the type of join is stored as a seperate
    # one would think that this allows for retyping the join later.. but really it just means that we 
    # do not need to add the word "join" to our string storage... so it just handling the fact that the type of join 
    # is listed before the word 'JOIN' while the method of the join is listed after.. 

    def __init__(self, sep = ''):
        QueryComponent.__init__(self, '', sep)
        self.type = ''

    @property
    def join_type(self):
        return self.type

    @join_type.setter
    def join_type(self, value):
        if type(value) != str:
            raise ValueError('join_type must be set to a string value.')
        self.type = value.upper()

    def __iadd__(self, item):
        if self.type:
            join = ' '.join([self.type, 'JOIN'])
        else:
            join = 'JOIN'
        self.add_item(item, join)
        return self

    __iand__ = __ior__ = __iadd__  # again, to start, lets have &= and |= just be the same function as +=  

    def __call__(self):
        if self.components:
            return self.sep.join(self.components)
        return ''


class WhereComponent(QueryComponent):

    header = 'WHERE'

    def __init__(self, sep=''):
        self.header = self.header + ' '
        QueryComponent.__init__(self, self.header, sep)

    def __iand__(self, item):
        self.add_item(item, 'AND')
        return self

    def __ior__(self, item):
        # add this to the list, but with a seperator of 'OR', this will be called when someone uses |=
        self.add_item(item, 'OR')
        return self

    __iadd__ = __iand__ # unless we use |= (which will invoke our custom built or function) we are using an "AND"

    def __str__(self):
        components = self.components
        if components:
            components = self.components[:]
            components[0] = re.sub('^AND |^OR ', '', components[0])
        to_print = list()
        for n, c in enumerate(components):
            to_print.append("{0}: '{1}'".format(n, c))
        return 'index: item\n' + ', '.join(to_print)

    __repr__ = __str__


