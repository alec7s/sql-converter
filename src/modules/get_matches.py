import re


def get_matches(searchTxtStr, rePatternRawStr, reFnNameStr, groupNum = 0):
    searchResult = None

    if reFnNameStr == 'search':
        search = re.search(rePatternRawStr, searchTxtStr)

        if search:
            searchResult = search.group(groupNum)

    if reFnNameStr == 'findall':
        searchResult = re.findall(rePatternRawStr, searchTxtStr)

        if len(searchResult) < 1:
            searchResult = None
    
    return searchResult