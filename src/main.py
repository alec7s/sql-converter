# NOTE: An overview of the application and user instructions can be found in the README.md file

import os
from pathlib import Path
import traceback
from modules.script import Script


# Get expected folder path for input folder and initialize inputFileList variable
rootPath = Path(__file__).parent.parent
logPath = rootPath / 'output' / 'error.txt'
inputPath = rootPath / 'input'
inputFileList = []


# Write custom error and stack trace text to log file
def write_error(customErrTxt):
    stackTrace = traceback.format_exc()
    log = open(logPath, 'a')
    log.write(f'{customErrTxt}\n{stackTrace}\n---------------------------\n\n')
    log.close()


# Get list of SQL scripts from input file
def extract_scripts(fileNameStr):
    file = open(inputPath / fileNameStr, 'r')
    fileText = file.read()
    scriptList = fileText.split(';')
    scriptList = [s for s in scriptList if s != '']
    file.close()

    return scriptList


# Custom exception to be thrown when input folder doesn't contain any files
class InputFolderEmpty(Exception):
    pass


# Custom exception to be thrown when an input script is NOT an UPDATE or INSERT statement
class IncompatibleSqlScript(Exception):
    pass


try:
    # Remove previous error log if it exists
    if os.path.exists(logPath):
        os.remove(logPath)

    # Extract names of files within the input folder if it exists.
    inputFileList = os.listdir(inputPath)

    # Throw exception if no files exist within folder
    if len(inputFileList) < 1:
        raise InputFolderEmpty()

    # Read each input file
    for fileName in inputFileList:
        
        # Get list of SQL scripts within each file
        extractedScripts = extract_scripts(fileName)
        outFileName = f'\nCONVERTED-{fileName}'
        print(outFileName)

        for s in extractedScripts:
            try:
                newScript = Script(s)

                print('\nCheck SQL elements:')
                print(f'clean input: {newScript.cleanSqlInputStr}\n')
                print(f'comments: {newScript.commentLst}\n')
                print(f'input type: {newScript.inputTypeStr}\n')
                print(f'errors: {newScript.errorLst}\n')

                # Throw exception if input script was NOT an UPDATE or INSERT statement (i.e., inputType is invalid)
                if not newScript.isValidSql:
                    raise IncompatibleSqlScript

                print(f'table: {newScript.tableStr}')
                print(f'columns: {newScript.columnLst}')
                print(f'values: {newScript.valueLst}')
                print(f'conditions: {newScript.conditionLst}')
                

                #print(newScript.convertScript())
                print('********************')

            except IncompatibleSqlScript:
                errorLstStr = '\n'.join(newScript.errorLst)
                write_error(f'Incompatible sql script found in {fileName}:\n{s}\n\n{errorLstStr}\n')
        
        print('---------------------')


# Throw exception if input folder does not exist (i.e., FileNotFoundError is thrown), create input folder, and save error info in log
except FileNotFoundError:
    os.mkdir(inputPath)
    write_error('The input folder was MISSING at runtime. Add SQL script file(s) to the input folder and run the program again.')


# Throw exception if input folder does not contain any files and save error info in log
except InputFolderEmpty:
    write_error('The input folder was EMPTY at runtime. Add SQL script file(s) to the input folder and run the program again.')