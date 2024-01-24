import re
from .get_matches import get_matches


class Script():
    def __init__(self, inputSqlStr):
        
        self.isValidSql = False
        self.inputTypeStr = None
        self.rawInputSqlStr = inputSqlStr
        self.commentLst = self.__get_comments()
        self.cleanSqlInputStr = re.sub(r'(?=\-\-).*', '', self.rawInputSqlStr).replace('\n', ' ').strip() + ';'
        self.convertedSqlStr = ''
        self.errorLst = []
        self.inputTypeStr = self.__get_input_type()

        while self.inputTypeStr != 'invalid':
            self.tableStr = self.__get_table()
            self.columnLst = self.__get_columns()
            self.valueLst = self.__get_values()
            self.conditionLst = self.__get_conditions()

            if all([self.tableStr, self.columnLst, self.valueLst, self.conditionLst]):
                self.isValidSql = True
                self.convertedSqlStr = ''
                self.__convertScript()
            break


    # If value of var is None, then save error text in errorLst attribute
    def __check_save_error(self, var, errorTxt, compVal = None):
        if var == compVal:
            self.errorLst.append(errorTxt)


    # Get list of comments
    def __get_comments(self):
        commentLst = get_matches(self.rawInputSqlStr, r'(?<=\-\-).*', 'findall')

        if not commentLst:
            commentLst = []

        return [s.strip() for s in commentLst]


    # Set input type (update, insert, or invalid) attribute
    def __get_input_type(self):
        inputType = 'invalid'
        inputSql = self.cleanSqlInputStr.lower()

        if inputSql.startswith('insert into '):
            inputType = 'insert'

        if inputSql.startswith('update '):
            inputType = 'update'

        self.__check_save_error(inputType, 'ERROR: Invalid script type', 'invalid')       

        return inputType 
    

    # Read input SQL to find table
    def __get_table(self):
        table = get_matches(self.cleanSqlInputStr, r'(?i)((?<=insert\sinto\s)|(?<=update\s))\w+', 'search')
        self.__check_save_error(table, 'ERROR: Could not find table in input script.')

        return table


    # Read input SQL to find script's columns and store as list in columns attribute
    def __get_columns(self):
        searchResult = None

        # Use regex pattern to find matches for columns if SQL INSERT statement
        if self.inputTypeStr == 'insert':
            searchResult = get_matches(self.cleanSqlInputStr, r'[(](.*?)[)]', 'search', 1).split(', ')
            
        # Use regex pattern to find matches for columns if SQL UPDATE statement
        if self.inputTypeStr == 'update':
            searchResult = get_matches(self.cleanSqlInputStr, r'(?i)(?<=set\s)\w+|(?<=\,)\s*\w+', 'findall')

        self.__check_save_error(searchResult, 'ERROR: Could not find columns in input script.')

        return searchResult
            

    # Read input SQL to find script's values and store as list in values attribute
    def __get_values(self):
        searchResult = None

        # Use regex pattern to find values if SQL INSERT statement
        if self.inputTypeStr == 'insert':
            searchResult = get_matches(self.cleanSqlInputStr, r'(?i)(?<=values \()[^)]+', 'search').split(', ')

        # Use regex pattern to find values if SQL UPDATE statement
        if self.inputTypeStr == 'update':
            setStmnt = get_matches(self.cleanSqlInputStr, r'(?i)(?=set).+(?=\sWHERE)|(?=set).+(?=\;)', 'search')

            # Search for values within SET statement using regex pattern
            if setStmnt:
                searchResult = get_matches(setStmnt, r'(?<=\=\s).*(?=\,)|(?<=\= ).*', 'findall')
        
        self.__check_save_error(searchResult, 'ERROR: Could not find values in input script.')

        return searchResult

        
    # Get conditions
    def __get_conditions(self):
        whereStmnt = None

        if self.inputTypeStr == 'insert' and len(self.commentLst) > 0 and self.commentLst[0].lower().startswith('where'):
            whereStmnt = self.commentLst[0]

        if self.inputTypeStr == 'update':
            whereStmnt = get_matches(self.cleanSqlInputStr, r'(?i)(?<=where\s).*(?=\;)', 'search')

        self.__check_save_error(whereStmnt, 'ERROR: Could not find where statement in input script.')
        
        return whereStmnt


    # Get/Set converted SQL script
    def __convertScript(self):
        outputScript = ''

        return outputScript