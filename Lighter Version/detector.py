import re
import sys

''' Method to Read a file and return it's content as String '''
def readDataFromFile(filePath):
    content = None
    try:
        with open(filePath, "r") as f:
            content = f.read()
    except:
        try:
            with open(filePath, "r", encoding="ISO-8859-1") as f:
                content = f.read()
        except:
            try:
                with open(filePath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print("Issue With File Reading")
                print(e)
                pass
    return content

''' Preparing list for all text and reference link words saperately using Regular expression '''
def processingFileContentForText(contentOfFile):
    refLinks = searchForReferenceLink(contentOfFile)
    bagOfWords = re.split('\t|\n|\.| |,|\(|\)|\”|"|\/|“', contentOfFile)
    refLinkWords = []
    if len(refLinks) > 0:
        refLinkWords = re.split('\/\/|\:\/\/|\/|\.| |#', ' '.join(refLinks))
    refLinkWordsFinal = []
    for word in refLinkWords:
        if word != '' and word.lower() not in refLinkWordsFinal:
            refLinkWordsFinal.append(word.lower())

    return bagOfWords, refLinkWordsFinal

''' Method to search for a links inside a text file '''
def searchForReferenceLink(contentOfFile):
    links = re.findall("(http:\/\/.*|https:\/\/.*|www:\/\/.*)", contentOfFile)
    return links

''' Preparing list of valid words including keywords of prgramming language '''
def processingFileContentForCode(contentOfFile):
    bagOfWords = re.split('\t|\n|\.| |,|\(|\)|\”|"|\/|=|\[|>>|<<|\'|\]|;|\|\'|!', contentOfFile)
    bagOfWordsFinal = []
    for word in bagOfWords:
        if word != '':
            bagOfWordsFinal.append(word)
    return bagOfWordsFinal

''' Method to check whether given file-string is code or simple-text '''
def isCodeFile(contentOfFile):
    keywords = ['!=', '#include', '()', '++', '+=', '--', '-=', '<', '<<', '<=', '=', '==', '>', '>=', '>>', 'abstract', 'and', 'as', 'assert', 'assert***', 'async', 'auto', 'await', 'bool', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'const*', 'continue', 'cout', 'def', 'default', 'del', 'do', 'double', 'elif', 'else', 'enum', 'enum****', 'except', 'extends', 'extern', 'false', 'final', 'finally', 'float', 'for', 'from', 'global', 'goto', 'goto*', 'h>', 'if', 'implements', 'import', 'in', 'instanceof', 'int', 'integer', 'interface', 'is', 'lambda', 'long', 'native', 'new', 'none', 'nonlocal', 'not', 'or', 'out', 'package', 'pass', 'print', 'println', 'private', 'protected', 'public', 'raise', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'strictfp**', 'struct', 'super', 'switch', 'synchronized', 'system', 'this', 'throw', 'throws', 'transient', 'true', 'try', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', 'with', 'yield', '{', '}']
    bagOfwords = re.split('\t|\n|\.| |\(|\'|\"', contentOfFile)
    codeKeywordsCount = 0
    totalWords = 0
    for word in bagOfwords:
        if word != '':
            if word.lower() in keywords:
                codeKeywordsCount = codeKeywordsCount + 1
            elif len(word.split(";")) == 2:
                codeKeywordsCount = codeKeywordsCount + 1
            totalWords = totalWords + 1
    return True if codeKeywordsCount * 100 / totalWords >= 25.50 else False

''' Method to find Longest Common Subsecquence between two Strings '''
def LCS(x, y):
    d = []
    prev = []
    for i in range(0, len(x)+1):
        a = []
        b = []
        for j in range(0, len(y)+1):
            a.append(0)
            b.append(0)
        d.append(a)
        prev.append(b)
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            if d[i-1][j] > d[i][j-1]:
                d[i][j] = d[i-1][j]
                prev[i][j] = str(i-1)+","+str(j)
            else:
                d[i][j] = d[i][j-1]
                prev[i][j] = str(i)+","+str(j-1)
            if x[i-1] == y[j-1] and (d[i-1][j-1] + 1) > d[i][j]:
                d[i][j] = d[i-1][j-1] + 1
                prev[i][j] = str(i-1)+","+str(j-1)
    result = []
    i = len(x)
    j = len(y)
    while i > 0 and j > 0:
        p, q = prev[i][j].split(",")
        p = int(p)
        q = int(q)
        if p == i-1 and q == j - 1:
            result.append(x[i-1])
        i = p
        j = q
    return d[len(x)][len(y)]

''' Method to find Editdistance between two Strings '''
def EditDistanceProblem(x, y):
    d = []
    for i in range(len(x)+1):
        a = []
        for j in range(len(y)+1):
            a.append(0)
        d.append(a)
    for i in range(len(x)+1):
        d[i][0] = i
    for j in range(len(y)+1):
        d[0][j] = j
    for i in range(1,len(x)+1):
        for j in range(1,len(y)+1):
            if x[i-1] != y[j-1]:
                if d[i-1][j] + 1 < d[i][j-1] + 1 and d[i-1][j] + 1 < d[i-1][j-1] + 1:
                    d[i][j] = d[i-1][j] + 1
                elif d[i-1][j] + 1 > d[i][j-1] + 1 and d[i][j-1] + 1 < d[i-1][j-1] + 1:
                    d[i][j] = d[i][j-1] + 1
                else:
                    d[i][j] = d[i-1][j-1] + 1
            else:
                if d[i-1][j] + 1 < d[i][j-1] + 1 and d[i-1][j] + 1 < d[i-1][j-1]:
                    d[i][j] = d[i-1][j] + 1
                elif d[i-1][j] + 1 > d[i][j-1] + 1 and d[i][j-1] + 1 < d[i-1][j-1]:
                    d[i][j] = d[i][j-1] + 1
                else:
                    d[i][j] = d[i-1][j-1]
    return d[len(x)][len(y)]

''' Method to detect plagiarism between two Text Files '''
def DetectPlagiarismInTextFiles(contentOfFile1, contentOfFile2):
    # Prepared two list for each file: one for normal textWords and another for refLinkWords
    bagOfWordsFile1WithRedudancy, refOfFile1 = processingFileContentForText(contentOfFile1)
    bagOfWordsFile2WithRedudancy, refOfFile2 = processingFileContentForText(contentOfFile2)
    # Calculating total length of Text file 1 and preparing new list by removing redundancy from the wordList
    bagOfWordsFile1 = []
    charactersOfFile1 = 0
    for word in bagOfWordsFile1WithRedudancy:
        if word != '':
            charactersOfFile1 = charactersOfFile1 + (len(word))
            if word.lower() not in bagOfWordsFile1:
                bagOfWordsFile1.append(word.lower())
    # Calculating total length of Text file 2 and preparing new list by removing redundancy from the wordList
    bagOfWordsFile2 = []
    charactersOfFile2 = 0
    for word in bagOfWordsFile2WithRedudancy:
        if word != '':
            charactersOfFile2 = charactersOfFile2 + (len(word))
            if word.lower() not in bagOfWordsFile2:
                bagOfWordsFile2.append(word.lower())
    # List of Ref-keywords which want to remove from original text File if it is present
    keyWordsNeedToAvoidForLink = ["https", "http", "www", "google", "wikipedia", "wiki", "com", "en", "org"]
    # Preparing list of words from Text File 1 for which reference is provided
    listToRemoveWordFromFile1 = []
    if len(refOfFile1) > 0:
        for word in refOfFile1:
            for word2 in bagOfWordsFile1:
                distance = EditDistanceProblem(word, word2)
                simillarity = LCS(word, word2)
                if distance == 0:
                    listToRemoveWordFromFile1.append(word2)
                elif simillarity > (len(word) * 66 // 100) and word not in keyWordsNeedToAvoidForLink:
                    listToRemoveWordFromFile1.append(word2)
                elif distance < (len(word) * 82 // 100) and word not in keyWordsNeedToAvoidForLink:
                    listToRemoveWordFromFile1.append(word2)
    # Remove the Ref-Link-Words from Text file 1 if found
    listToRemoveWordFromFile1 = list(dict.fromkeys(listToRemoveWordFromFile1))
    for word in listToRemoveWordFromFile1:
        bagOfWordsFile1.remove(word)
    # Preparing list of words from Text File 2 for which reference is provided
    listToRemoveWordFromFile2 = []
    if len(refOfFile2) > 0:
        for word in refOfFile2:
            for word2 in bagOfWordsFile2:
                distance = EditDistanceProblem(word, word2)
                simillarity = LCS(word, word2)
                if distance == 0:
                    listToRemoveWordFromFile2.append(word2)
                elif simillarity > (len(word) * 66 // 100) and word not in keyWordsNeedToAvoidForLink:
                    listToRemoveWordFromFile2.append(word2)
                elif distance < (len(word) * 82 // 100) and word not in keyWordsNeedToAvoidForLink:
                    listToRemoveWordFromFile2.append(word2)
    # Remove the Ref-Link-Words from Text file 2 if found
    listToRemoveWordFromFile2 = list(dict.fromkeys(listToRemoveWordFromFile2))
    for word in listToRemoveWordFromFile2:
        bagOfWordsFile2.remove(word)
    # Initializing 2D-Array for word-to-word compare LCS
    dp = []
    for i in range(0,len(bagOfWordsFile1)+1):
        d = []
        for j in range(0,len(bagOfWordsFile2)+1):
            d.append(0)
        dp.append(d)
    # Applying word-to-word LCS to calculate matching percentage
    for i in range(1, len(bagOfWordsFile1)+1):
        for j in range(1, len(bagOfWordsFile2)+1):
            if bagOfWordsFile1[i-1] == bagOfWordsFile2[j-1]:
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i][j-1], dp[i-1][j])
    # calculating matching percentage relative to both files and returning the final result based on threshold
    return False if (((1.00 * dp[len(bagOfWordsFile1)][len(bagOfWordsFile2)] / len(bagOfWordsFile1) * 100)+(1.00 * dp[len(bagOfWordsFile1)][len(bagOfWordsFile2)] / len(bagOfWordsFile2) * 100))/2) < 40.0 else True

''' Method to detect plagiarism between Code File '''
def DetectPlagiarismInCodeFiles(contentOfFile1, contentOfFile2):
    # Prepared list of words for both code files
    bagOfWordsFile1 = processingFileContentForCode(contentOfFile1)
    bagOfWordsFile2 = processingFileContentForCode(contentOfFile2)
    # Counting the total number of characters in code file1
    charactersOfFile1 = 0
    for word in bagOfWordsFile1:
        charactersOfFile1 = charactersOfFile1 + (len(word))
    # Counting the total number of characters in code file2
    charactersOfFile2 = 0
    for word in bagOfWordsFile2:
        charactersOfFile2 = charactersOfFile2 + (len(word))
    # Removing duplicate words from both the list which we prepared from Code File1 and File2
    bagOfWordsFile1 = list(dict.fromkeys(bagOfWordsFile1))
    bagOfWordsFile2 = list(dict.fromkeys(bagOfWordsFile2))
    # Preparing emtpy 2D-Array to store the result of word-to-word compare LCS
    dp = []
    for i in range(0,len(bagOfWordsFile1)+1):
        d = []
        for j in range(0,len(bagOfWordsFile2)+1):
            d.append(0)
        dp.append(d)
    # Word-To-Word Compare LCS to detect the matching words between two list
    for i in range(1, len(bagOfWordsFile1)+1):
        for j in range(1, len(bagOfWordsFile2)+1):
            if bagOfWordsFile1[i-1] == bagOfWordsFile2[j-1]:
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i][j-1], dp[i-1][j])
    # calculating matching percentage relative to both files and returning the final result based on threshold
    return False if (((1.00 * dp[len(bagOfWordsFile1)][len(bagOfWordsFile2)] / len(bagOfWordsFile1) * 100)+(1.00 * dp[len(bagOfWordsFile1)][len(bagOfWordsFile2)] / len(bagOfWordsFile2) * 100))/2) < 40.0 else True

''' Main Method of the file '''
if __name__ == "__main__":
    contentOfFile1 = None
    contentOfFile2 = None
    plagarism_detected = False
    # Reading Files from given command line argument
    contentOfFile1 = readDataFromFile(sys.argv[1])
    contentOfFile2 = readDataFromFile(sys.argv[2])
    # If Both the file succefully read then we further proceed to check plagiarism
    if contentOfFile1 != None and contentOfFile2 != None:
        # Checking for whether given file is Code or Text
        isCodeFile1 = isCodeFile(contentOfFile1)
        isCodeFile2 = isCodeFile(contentOfFile2)
        # Based on the result of above check we have three different possibilities which are illustrated below,
        if isCodeFile1 != isCodeFile2:
            # Comparison between Code and Text is not a plagiarism
            plagarism_detected = False
        elif isCodeFile1 == False:
            # If both files are Text files then we need to check for percentage match between two Text files
            plagarism_detected = DetectPlagiarismInTextFiles(contentOfFile1, contentOfFile2)
        else:
            # If both files are Code files then we need to check for percentage match between two code files
            plagarism_detected = DetectPlagiarismInCodeFiles(contentOfFile1, contentOfFile2)
    # Based on the above processing if there is a plagiarism then it will return 1 else 0 otherwise
    if plagarism_detected:
        print(1)
    else:
        print(0)