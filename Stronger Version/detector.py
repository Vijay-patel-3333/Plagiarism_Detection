import sys
import re
import time

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
	#print(len(d))
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
	# for r in prev:
	# 	print(r)
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
	#print("Comman Sequence : ",result)
	return d[len(x)][len(y)]



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
	#for a in d:
	#	print(a)
	return d[len(x)][len(y)]
	
def readDataFromFile(file1):
	f = None
	content = None
	try:
		f = open(file1, "r", encoding="utf8")
		content = f.read()
	except:
		f = open(file1, "r")
		content = f.read()
	words = []
	refLinks = searchForReferenceLink(content)
	bagOfWords = re.split('\t|\n|\.| |,|\(|\)|\”|"|\/|“', content)
	refLinkWords = []
	if len(refLinks) > 0:
		refLinkWords = re.split('\/\/|\:\/\/|\/|\.| |#', ' '.join(refLinks))
	return bagOfWords, refLinkWords

	
def readDataFromCode(file1):
	f = open(file1, "r", encoding="utf8")
	content = f.read()
	words = []
	bagOfWords = re.split('\t|\n|\.| |,|\(|\)|\”|"|\/|=|\[|>>|<<|\'|\]|;|\|\'|!', content)
	return bagOfWords

def searchForReferenceLink(content):
	# pattern = re.compile("<(http:\/\/+|https:\/\/+|www:\/\/+)>")
	links = re.findall("(http:\/\/.*|https:\/\/.*|www:\/\/.*)", content)
		# print(x)
	# links = content.find(r'')
	print("@MEME@ ",links)
	return links
def prepareBagOfWordsWithFrequencyForCode(bagOfWords):
	bagOfWordsWithFrequency = {}
	for word in bagOfWords:
		if word != '':
			if word.lower() in bagOfWordsWithFrequency:
				bagOfWordsWithFrequency[word.lower()] = bagOfWordsWithFrequency[word.lower()] + 1
			else:
				bagOfWordsWithFrequency[word.lower()] = 1
	return bagOfWordsWithFrequency

def prepareBagOfWordsWithFrequency(bagOfWords, linkWords):
	bagOfWordsWithFrequency = {}
	for word in bagOfWords:
		if word != '':
			if word.lower() in bagOfWordsWithFrequency:
				bagOfWordsWithFrequency[word.lower()] = bagOfWordsWithFrequency[word.lower()] + 1
			else:
				bagOfWordsWithFrequency[word.lower()] = 1
	refWordsWithFrequency = {}
	if len(linkWords)!=0:
		for word in linkWords:
			if word != '':
				if word.lower() in refWordsWithFrequency:
					refWordsWithFrequency[word.lower()] = refWordsWithFrequency[word.lower()] + 1
				else:
					refWordsWithFrequency[word.lower()] = 1
	return bagOfWordsWithFrequency, refWordsWithFrequency

def DetectPlagarismInTextFiles8(file1, file2):
	a, b = readDataFromFile(file1)
	c, d = readDataFromFile(file2)
	print(" : ",b)
	print(" : ",d)
	file1WordBag, file1RefLinkWords = prepareBagOfWordsWithFrequency(a, b)
	file2WordBag, file2RefLinkWords = prepareBagOfWordsWithFrequency(c, d)
	print("MEME", file1RefLinkWords)
	print("MEME", file2RefLinkWords)
	# smallFile = file1WordBag if len(file1WordBag) < len(file2WordBag) else file2WordBag
	# bigFile = file2WordBag if len(file2WordBag) > len(file1WordBag) else file1WordBag
	# print("SmallFile : ",len(smallFile))
	# print("BigFile : ",len(bigFile))
	charactersOfFile1 = 0
	for word in file1WordBag:
		charactersOfFile1 = charactersOfFile1 + (file1WordBag[word] * len(word))

	charactersOfFile2 = 0
	for word in file2WordBag:
		charactersOfFile2 = charactersOfFile2 + (file2WordBag[word] * len(word))

	smallFile, smallRefFile = {},{}
	bigFile, bigRefFile = {},{}
	# smallFile, smallRefFile = file1WordBag,file1RefLinkWords if charactersOfFile1 < charactersOfFile2 else file2WordBag, file2RefLinkWords
	# bigFile, bigRefFile = file2WordBag, file2RefLinkWords if charactersOfFile2 > charactersOfFile1 else file1WordBag, file1RefLinkWords
	if charactersOfFile1 < charactersOfFile2:
		smallFile, smallRefFile = file1WordBag, file1RefLinkWords
	else:
		smallFile, smallRefFile = file2WordBag, file2RefLinkWords

	if charactersOfFile2 > charactersOfFile1:
		bigFile, bigRefFile = file2WordBag, file2RefLinkWords
	else:
		bigFile, bigRefFile = file1WordBag, file1RefLinkWords


	if len(smallRefFile) > 0:
		smallRefFileTemp = {}
		smallRefFileTemp2 = {}
		for word in smallRefFile:
			for word2 in smallFile:
				temp2 = EditDistanceProblem(word, word2)
				temp = LCS(word, word2)

				if temp2 == 0:
					smallFile[word2] = 0
				elif temp > (len(word) * 66 // 100) and smallRefFile[word] > 0 and word not in ["https", "http", "www",
																							  "google", "wikipedia",
																							  "wiki", "com", "en",
																							  "org"]:
					smallFile[word2] = 0
					if temp in smallRefFileTemp:
						smallRefFileTemp[temp].append([word, word2])
					else:
						smallRefFileTemp[temp] = [[word, word2]]
				elif temp2 < (len(word) * 82 // 100) and smallRefFile[word] > 0 and word not in ["https", "http", "www",
																							   "google", "wikipedia",
																							   "wiki", "com", "en",
																							   "org"]:
					smallFile[word2] = 0
					if temp2 in smallRefFileTemp2:
						smallRefFileTemp2[temp2].append([word, word2])
					else:
						smallRefFileTemp2[temp2] = [[word, word2]]
		print("@@ MEME @@ : SMALL ", smallRefFileTemp)
		print("@@ MEME @@ : SMALL 2", smallRefFileTemp2)

	if len(bigRefFile) > 0:
		bigRefFileTemp = {}
		bigRefFileTemp2 = {}
		for word in bigRefFile:
			for word2 in bigFile:
				temp2 = EditDistanceProblem(word, word2)
				temp = LCS(word, word2)

				if temp2 == 0:
				# 	if bigFile[word2] > bigRefFile[word]:
				# 		bigFile[word2] = bigFile[word2] - bigRefFile[word]
				# 		bigRefFile[word] = 0
				# 	else:
				# 		bigRefFile[word] = bigRefFile[word] - bigFile[word2]
						bigFile[word2] = 0
				elif temp > (len(word) * 66 //100) and bigRefFile[word]>0 and word not in ["https","http","www","google","wikipedia","wiki","com","en","org"]:
					bigFile[word2] = 0
					if temp in bigRefFileTemp:
						bigRefFileTemp[temp].append([word, word2])
					else:
						bigRefFileTemp[temp] = [[word, word2]]
				elif temp2 < (len(word) * 82 // 100) and bigRefFile[word]>0 and word not in ["https","http","www","google","wikipedia","wiki","com","en","org"]:
					bigFile[word2] = 0
					if temp2 in bigRefFileTemp2:
						bigRefFileTemp2[temp2].append([word, word2])
					else:
						bigRefFileTemp2[temp2] = [[word, word2]]
		print("@@ MEME @@ : BIG ", bigRefFileTemp)
		print("@@ MEME @@ : BIG 2", bigRefFileTemp2)
	lst1 = []
	for word in smallFile:
		if smallFile[word] == 0:
			lst1.append(word)
	for word in lst1:
		del smallFile[word]
	lst1= []
	for word in bigFile:
		if bigFile[word] == 0:
			lst1.append(word)
	for word in lst1:
		del bigFile[word]
	dp = []
	for i in range(len(smallFile)+1):
		d = []
		for j in range(len(bigFile)+1):
			d.append(0)
		dp.append(d)
	print("FILE1 :",smallFile)
	print("File2 :",bigFile)
	i = 1
	for word1 in smallFile:
		j = 1
		for word2 in bigFile:
			if word1 == word2:
				dp[i][j] = dp[i-1][j-1]+1
			else:
				dp[i][j] = max(dp[i][j-1], dp[i-1][j])
			j = j + 1
		i = i + 1

	# for i in dp:
	# 	print(i)
	print("file1 length:",len(smallFile))
	print("file2 length:",len(bigFile))
	print("count",dp[len(smallFile)][len(bigFile)]);

	print(((1.00 * dp[len(smallFile)][len(bigFile)] / len(bigFile) * 100)+(1.00 * dp[len(smallFile)][len(bigFile)] / len(smallFile) * 100))/2)
	# return 0
	return False if (((1.00 * dp[len(smallFile)][len(bigFile)] / len(bigFile) * 100)+(1.00 * dp[len(smallFile)][len(bigFile)] / len(smallFile) * 100))/2) < 41.0 else True

def DetectPlagarismInCodeFiles3(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequencyForCode(readDataFromCode(file1))
	file2WordBag = prepareBagOfWordsWithFrequencyForCode(readDataFromCode(file2))
	charactersOfFile1 = 0
	for word in file1WordBag:
		charactersOfFile1 = charactersOfFile1 + (file1WordBag[word] * len(word))

	charactersOfFile2 = 0
	for word in file2WordBag:
		charactersOfFile2 = charactersOfFile2 + (file2WordBag[word] * len(word))

	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag
	lst1 = []
	for word in smallFile:
		if smallFile[word] == 0:
			lst1.append(word)
	for word in lst1:
		del smallFile[word]
	lst1= []
	for word in bigFile:
		if bigFile[word] == 0:
			lst1.append(word)
	for word in lst1:
		del bigFile[word]
	dp = []
	for i in range(len(smallFile)+1):
		d = []
		for j in range(len(bigFile)+1):
			d.append(0)
		dp.append(d)

	i = 1
	for word1 in smallFile:
		j = 1
		for word2 in bigFile:
			if word1 == word2:
				dp[i][j] = dp[i-1][j-1]+1
			else:
				dp[i][j] = max(dp[i][j-1], dp[i-1][j])
			j = j + 1
		i = i + 1

	# for i in dp:
	# 	print(i)
	print("file1 length:",len(smallFile))
	print("file2 length:",len(bigFile))
	print("count",dp[len(smallFile)][len(bigFile)]);

	print(((1.00 * dp[len(smallFile)][len(bigFile)] / len(bigFile) * 100)+(1.00 * dp[len(smallFile)][len(bigFile)] / len(smallFile) * 100))/2)
	return False if (((1.00 * dp[len(smallFile)][len(bigFile)] / len(bigFile) * 100)+(1.00 * dp[len(smallFile)][len(bigFile)] / len(smallFile) * 100))/2) < 40.0 else True
	# return 0
	
def isCodeFile(file1):
	keywords = ["#include","elif","void","bool","h>","int","for","while","return","char","cout","<<",">>","if","else","==","!=",">=","<=","{","}","=","++","--","<",">","++","--","switch","case","()","system","system","out","println","print","abstract" ,	"continue" ,	"for" ,	"new" ,	"switch","assert***", 	"default" 	,"goto*" ,	"package", 	"synchronized","boolean", 	"do" ,	"if" ,	"private" ,	"this","break" ,	"double" 	,"implements" 	,"protected" ,	"throw","byte" ,	"else" ,"import" ,	"public" 	,"throws","case", "enum****", 	"instanceof" ,	"return" ,	"transient","catch" 	,"extends" ,	"int" ,	"short" ,	"try","char" ,	"final" 	,"interface" ,	"static" 	,"void","class" ,	"finally" ,	"long" 	,"strictfp**" ,	"volatile","const*" ,	"float" ,	"native" ,	"super" 	,"while",'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',"auto",	"break","case","char","const","continue","default","do","double","else","enum","extern","float","for","goto","if","int","long","register","return","short","signed","sizeof","static","struct","switch","typedef","union","unsigned","void","volatile","while"]
	for w in range(len(keywords)):
		# w.lower()
		keywords[w]=keywords[w].lower()
	# print(keywords)
	print()
	print(file1)
	f = None
	content = None
	try:
		f = open(file1, "r", encoding="utf8")
		content = f.read()
	except:
		f = open(file1, "r")
		content = f.read()
	words = []
	bagOfwords = re.split('\t|\n|\.| |\(|\'|\"', content)
	# print(bagOfwords)
	codeKeywordsCount = 0
	totalWords = 0
	for word in bagOfwords:
		if word!='':
			if word.lower() in keywords:
				codeKeywordsCount = codeKeywordsCount + 1
			elif len(word.split(";")) == 2:
				codeKeywordsCount = codeKeywordsCount + 1
			totalWords = totalWords + 1
	print("codeKeywordsCount", codeKeywordsCount)
	#print(totalWords)
	print(codeKeywordsCount * 100 / totalWords)
	print("Total words : ",len(bagOfwords))
	print("codeKeywordsCount * 100 / totalWords",codeKeywordsCount * 100 / totalWords)
	return True if codeKeywordsCount * 100 / totalWords >= 30.00 else False 

if __name__ == "__main__":
	st = time.time()
	plagarism_detected  = True
	
	#print("Is Code File 1 : ",isCodeFile(sys.argv[1]))
	#print("Is Code File 2 : ",isCodeFile(sys.argv[2]))
	isCodeFile1 = isCodeFile(sys.argv[1])
	isCodeFile2 = isCodeFile(sys.argv[2])
	if isCodeFile1 != isCodeFile2:
		plagarism_detected = False 
	elif isCodeFile1 == True:
		plagarism_detected = DetectPlagarismInCodeFiles3(sys.argv[1], sys.argv[2])
		print("In Code part")
	else:
		# Call DetectPlagarismInTextFiles
		plagarism_detected = DetectPlagarismInTextFiles8(sys.argv[1], sys.argv[2])
		print("In Text Part")
	
	if plagarism_detected:
		print(1)
	else:
		print(0)
	
	
	et = time.time()
	elapsed_time = et - st
	print('Execution time:', elapsed_time, 'seconds')
	
