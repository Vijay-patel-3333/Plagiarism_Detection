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
	print(file1)
	refLinks = searchForReferenceLink(content)
	bagOfWords = re.split('\t|\n|\.| |,|\(|\)|\”|"|\/|“', content)
	refLinkWords = []
	print("@@@ MEME ",' '.join(refLinks))
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

def DetectPlagarismInTextFiles3(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file1))
	file2WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file2))
	#smallFile = file1WordBag if len(file1WordBag) < len(file2WordBag) else file2WordBag
	#bigFile = file2WordBag if len(file2WordBag) > len(file1WordBag) else file1WordBag
	#print("SmallFile : ",len(smallFile))
	#print("BigFile : ",len(bigFile))
	charactersOfFile1 = 0
	for word in file1WordBag:
		charactersOfFile1 = charactersOfFile1 + (file1WordBag[word]*len(word))
		
	charactersOfFile2 = 0
	for word in file2WordBag:
		charactersOfFile2 = charactersOfFile2 + (file2WordBag[word]*len(word))
	
	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag
		
	EditDistanceMap = {}
	for word1 in bigFile:
		lst = []
		for word2 in smallFile:
			lst.append([word2,EditDistanceProblem(word1, word2)])
		EditDistanceMap[word1] = lst
	print("small : ",len(smallFile)," charactersOfFile1 : ",charactersOfFile1," Temp : ",len(file1WordBag))
	print("big : ",len(bigFile)," charactersOfFile2 : ",charactersOfFile2," Temp : ",len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ",smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ",bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	LCSDistanceMap = {}
	for word1 in bigFile:
		lst = []
		for word2 in smallFile:
			if LCS(word1, word2) in LCSDistanceMap:
				LCSDistanceMap[LCS(word1, word2)].append([word1,word2])
			else:
				LCSDistanceMap[LCS(word1, word2)] = [[word1,word2]]
	
	
	for word in EditDistanceMap:
		lst = EditDistanceMap[word]
		for key2, distance in lst:
			if distance == 0:
				print("Word : ",word," key2 : ",key2," distance : ",distance)
				if smallFile[key2] < bigFile[word]:
	#				print("first")
					bigFile[word] = bigFile[word] - smallFile[key2]
					smallFile[key2] = 0
					
				else:
	#				print("second")
					smallFile[key2] = smallFile[key2] - bigFile[word]
					bigFile[word] = 0
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	# words = bigFile.keys()
	# costToChangeLargeFileToSmallFile = 0
	
	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			#for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 					# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					#print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 					# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 			#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	# print("FWord : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 	if smallKey1 != None:
	# 		print("=================")
	# 		print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		print(smallFile)
	# 		print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			#print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[smallKey1]*minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
				
	# 		else:
	# 			#print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1]*minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 		# print("small : ",smallFile)
	# 		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 		# print("big : ",bigFile)
	# 		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	# print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)	
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# for word in bigFile:
	# 	#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
	# 	if bigFile[word] > 0:
	# 		print(word)
	# 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word]*len(word))
			
	# 	bigFile[word] = 0
	# #print("charLength : ", charactersOfFile2)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)	
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # for word in smallFile:
	# # 	if smallFile[word] > 0:
	# # 		print(word)
	# # 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	# bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	# smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	# print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	# print("smallFileChars : ",smallFileChars)
	# print("bigFileChars : ",bigFileChars)
	# print("Percentage Distance : ",	(costToChangeLargeFileToSmallFile * 100)/bigFileChars)
	# # print("LCSDistanceMap : ",LCSDistanceMap)
	# return True if ((costToChangeLargeFileToSmallFile * 100)/bigFileChars) < 41.0 else False


def DetectPlagarismInTextFiles2(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file1))
	file2WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file2))
	#smallFile = file1WordBag if len(file1WordBag) < len(file2WordBag) else file2WordBag
	#bigFile = file2WordBag if len(file2WordBag) > len(file1WordBag) else file1WordBag
	#print("SmallFile : ",len(smallFile))
	#print("BigFile : ",len(bigFile))
	charactersOfFile1 = 0
	for word in file1WordBag:
		charactersOfFile1 = charactersOfFile1 + (file1WordBag[word]*len(word))
		
	charactersOfFile2 = 0
	for word in file2WordBag:
		charactersOfFile2 = charactersOfFile2 + (file2WordBag[word]*len(word))
	
	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag
		
	EditDistanceMap = {}
	for word1 in bigFile:
		tempDict = {}
		for word2 in smallFile:
			tempDict[word2] = EditDistanceProblem(word1, word2)
			# lst.append([word2,EditDistanceProblem(word1, word2)])
		EditDistanceMap[word1] = tempDict
	print("small : ",len(smallFile)," charactersOfFile1 : ",charactersOfFile1," Temp : ",len(file1WordBag))
	print("big : ",len(bigFile)," charactersOfFile2 : ",charactersOfFile2," Temp : ",len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ",smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ",bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	LCSDistanceMap = {}
	for word1 in bigFile:
		lst = []
		for word2 in smallFile:
			if LCS(word1, word2) in LCSDistanceMap:
				LCSDistanceMap[LCS(word1, word2)].append([word1,word2])
			else:
				LCSDistanceMap[LCS(word1, word2)] = [[word1,word2]]
			# lst.append([word2,LCS(word1, word2)])
		# LCSDistanceMap[word1] = lst
	# print("LCSDistanceMap : ",LCSDistanceMap)	
	
	for bigWord in EditDistanceMap:
		for smallWord in EditDistanceMap[bigWord]:
		# for key2, distance in lst:
			if EditDistanceMap[bigWord][smallWord] == 0:
				print("bigWord : ",bigWord," smallWord : ",smallWord," distance : ",EditDistanceMap[bigWord][smallWord])
				if smallFile[smallWord] < bigFile[bigWord]:
	#				print("first")
					bigFile[bigWord] = bigFile[bigWord] - smallFile[smallWord]
					smallFile[smallWord] = 0
					
				else:
	#				print("second")
					smallFile[smallWord] = smallFile[smallWord] - bigFile[bigWord]
					bigFile[bigWord] = 0
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	costToChangeLargeFileToSmallFile = 0
	print("Size : ",len(LCSDistanceMap))
	# ab = reversed(sorted(LCSDistanceMap.keys()))
	for key in reversed(sorted(LCSDistanceMap.keys())):
		allCovered = False
		while allCovered == False:
			allCovered = True
			smallKey1 = ''
			bigKey1 = None
			for bigKey, smallKey in LCSDistanceMap[key]:
				# print(key)
				if EditDistanceMap[bigKey][smallKey] != 0 and bigFile[bigKey] > 0 and smallFile[smallKey] > 0 and len(smallKey) > len(smallKey1) :
					smallKey1 = smallKey
					bigKey1 = bigKey
					allCovered = False
					#for word in EditDistanceMap:
				# lst = EditDistanceMap[word]
				# for key2, distance in lst:
				# 	if distance != 0 and distance < minDistance and smallFile[key2] > 0:
				# 		smallKey1 = key2
				# 		bigKey1 = word
				# 		minDistance = distance
				# 		# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
				# 	if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
				# 		#print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
				# 		smallKey1 = key2
				# 		bigKey1 = word
				# 		minDistance = distance
				# 		# print("same : ",word," key2 : ",key2," distance : ",distance)
				#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
		# print("FWord : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
			if bigKey1 != None:
				print("FWord : ",bigKey1," key2 : ",smallKey1," distance : ",EditDistanceMap[bigKey1][smallKey1],' LCS : ',key)
				# print("=================")
				# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[key])
				# print(bigFile)
				# print(smallFile)
				# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
				# print("===================")
				if smallFile[smallKey1] < bigFile[bigKey1]:
					#print("first")
					costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[smallKey1]*EditDistanceMap[bigKey1][smallKey1])
					bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
					smallFile[smallKey1] = 0
					# print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
					
				else:
					#print("second")
					costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1]*EditDistanceMap[bigKey1][smallKey1])
					smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
					bigFile[bigKey1] = 0
					# print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("small : ",smallFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("big : ",bigFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			# else:
			# 	break
	# print("LCSDistanceMap : ",LCSDistanceMap)
	# for keys in LCSDistanceMap.key():
	# 	print(keys)
	# words = bigFile.keys()
	# costToChangeLargeFileToSmallFile = 0
	
	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			#for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 					# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					#print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 					# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 			#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	# print("FWord : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 	if smallKey1 != None:
	# 		print("=================")
	# 		print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		print(smallFile)
	# 		print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			#print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[smallKey1]*minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
				
	# 		else:
	# 			#print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1]*minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 		# print("small : ",smallFile)
	# 		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 		# print("big : ",bigFile)
	# 		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word]*len(word))
			bigFile[word] = 0
	# #print("charLength : ", charactersOfFile2)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)	
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in smallFile:
		if smallFile[word] > 0:
			print('Small : ',word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	print("smallFileChars : ",smallFileChars)
	print("bigFileChars : ",bigFileChars)
	print("Percentage Distance : ",	(costToChangeLargeFileToSmallFile * 100)/bigFileChars)
	# # print("LCSDistanceMap : ",LCSDistanceMap)
	return True if ((costToChangeLargeFileToSmallFile * 100)/bigFileChars) < 41.0 else False


def DetectPlagarismInTextFiles(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file1))
	file2WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file2))
	#smallFile = file1WordBag if len(file1WordBag) < len(file2WordBag) else file2WordBag
	#bigFile = file2WordBag if len(file2WordBag) > len(file1WordBag) else file1WordBag
	#print("SmallFile : ",len(smallFile))
	#print("BigFile : ",len(bigFile))
	charactersOfFile1 = 0
	for word in file1WordBag:
		charactersOfFile1 = charactersOfFile1 + (file1WordBag[word]*len(word))
		
	charactersOfFile2 = 0
	for word in file2WordBag:
		charactersOfFile2 = charactersOfFile2 + (file2WordBag[word]*len(word))
	
	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag
		
	EditDistanceMap = {}
	for word1 in bigFile:
		lst = []
		for word2 in smallFile:
			lst.append([word2,EditDistanceProblem(word1, word2)])
		EditDistanceMap[word1] = lst
	print("small : ",len(smallFile)," charactersOfFile1 : ",charactersOfFile1," Temp : ",len(file1WordBag))
	print("big : ",len(bigFile)," charactersOfFile2 : ",charactersOfFile2," Temp : ",len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ",smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ",bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	LCSDistanceMap = {}
	for word1 in bigFile:
		lst = []
		for word2 in smallFile:
			lst.append([word2,LCS(word1, word2)])
		LCSDistanceMap[word1] = lst
	
	
	for word in EditDistanceMap:
		lst = EditDistanceMap[word]
		for key2, distance in lst:
			if distance == 0:
				print("Word : ",word," key2 : ",key2," distance : ",distance)
				if smallFile[key2] < bigFile[word]:
	#				print("first")
					bigFile[word] = bigFile[word] - smallFile[key2]
					smallFile[key2] = 0
					
				else:
	#				print("second")
					smallFile[key2] = smallFile[key2] - bigFile[word]
					bigFile[word] = 0
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0
	
	while len(words) > 0:
		smallKey1 = None
		bigKey1 = None
		minDistance = 1000000
		for word in words:
			if bigFile[word] > 0:
				#for word in EditDistanceMap:
				lst = EditDistanceMap[word]
				for key2, distance in lst:
					if distance != 0 and distance < minDistance and smallFile[key2] > 0:
						smallKey1 = key2
						bigKey1 = word
						minDistance = distance
						# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
					if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
						#print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
						smallKey1 = key2
						bigKey1 = word
						minDistance = distance
						# print("same : ",word," key2 : ",key2," distance : ",distance)
				#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
		print("FWord : ",bigKey1," key2 : ",smallKey1," distance : ",minDistance)
		if smallKey1 != None:
			# print("=================")
			# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
			# print(smallFile)
			# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
			# print("===================")
			if smallFile[smallKey1] < bigFile[bigKey1]:
				#print("first")
				costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[smallKey1]*minDistance)
				bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
				smallFile[smallKey1] = 0
				
			else:
				#print("second")
				costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1]*minDistance)
				smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
				bigFile[bigKey1] = 0
			# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			# print("small : ",smallFile)
			# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			# print("big : ",bigFile)
			# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		else:
			break
	print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word]*len(word))
			
		bigFile[word] = 0
	#print("charLength : ", charactersOfFile2)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# for word in smallFile:
	# 	if smallFile[word] > 0:
	# 		print(word)
	# 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	print("smallFileChars : ",smallFileChars)
	print("bigFileChars : ",bigFileChars)
	print("Percentage Distance : ",	(costToChangeLargeFileToSmallFile * 100)/bigFileChars)
	# print("LCSDistanceMap : ",LCSDistanceMap)
	return True if ((costToChangeLargeFileToSmallFile * 100)/bigFileChars) < 41.0 else False


def DetectPlagarismInTextFiles3(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file1))
	file2WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file2))
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

	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag

	EditDistanceMap = {}
	for word1 in bigFile:
		# tempDict = {}
		for word2 in smallFile:
			if EditDistanceProblem(word1, word2) in EditDistanceMap:
				EditDistanceMap[EditDistanceProblem(word1, word2)].append([word1, word2])
			else:
				EditDistanceMap[EditDistanceProblem(word1, word2)]=[[word1, word2]]

	print(EditDistanceMap)
			# tempDict[word2] = EditDistanceProblem(word1, word2);
			# lst.append([word2, EditDistanceProblem(word1, word2)])
		# EditDistanceMap[word1] = tempDict
	print("small : ", len(smallFile), " charactersOfFile1 : ", charactersOfFile1, " Temp : ", len(file1WordBag))
	print("big : ", len(bigFile), " charactersOfFile2 : ", charactersOfFile2, " Temp : ", len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ", smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ", bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

	# LCSDistanceMap = {}
	# for word1 in bigFile:
	# 	lst = []
	# 	for word2 in smallFile:
	# 		lst.append([word2, LCS(word1, word2)])
	# 	LCSDistanceMap[word1] = lst
	#
	for word, key2 in EditDistanceMap[0]:
		# lst = EditDistanceMap[word]
		# for key2, distance in lst:
		# 	if distance == 0:
		print("Word : ", word, " key2 : ", key2)
		if smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] < bigFile[word]:
			#				print("first")
			bigFile[word] = bigFile[word] - smallFile[key2]
			smallFile[key2] = 0

		elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] > bigFile[word]:
			#				print("second")
			smallFile[key2] = smallFile[key2] - bigFile[word]
			bigFile[word] = 0
		elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] == bigFile[word]:
			smallFile[key2] = 0
			bigFile[word] = 0

	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	#
	words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0

	for distanceKey in sorted(EditDistanceMap.keys()):
		if distanceKey != 0:
			some_edit_exists = True
			while some_edit_exists:
				smallKey1 = None
				bigKey1 = None
				charLength = None
				for word, key2 in EditDistanceMap[distanceKey]:
					if bigFile[word] > 0 and smallFile[key2] > 0 and charLength == None:
						charLength = len(key2)
						bigKey1 = word
						smallKey1 = key2
					elif bigFile[word] > 0 and smallFile[key2] > 0 and charLength < len(key2):
						charLength = len(key2)
						bigKey1 = word
						smallKey1 = key2
				if smallKey1 != None:
					# print("=================")
					print(bigKey1," -> ",smallKey1," -> ",distanceKey)
					# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
					# print(smallFile)
					# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
					# print("===================")
					if smallFile[smallKey1] < bigFile[bigKey1]:
						# print("first")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
								smallFile[smallKey1] * distanceKey)
						bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
						smallFile[smallKey1] = 0

					else:
						# print("second")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
									bigFile[bigKey1] * distanceKey)
						smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
						bigFile[bigKey1] = 0
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("small : ",smallFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("big : ",bigFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				else:
					some_edit_exists = False

	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			# for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 				# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					# print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 			# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	print("FWord : ", bigKey1, " key2 : ", smallKey1, " distance : ", minDistance)
	# 	if smallKey1 != None:
	# 		# print("=================")
	# 		# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		# print(smallFile)
	# 		# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		# print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			# print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 						smallFile[smallKey1] * minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
	#
	# 		else:
	# 			# print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1] * minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("small : ",smallFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("big : ",bigFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word] * len(word))
			bigFile[word] = 0

	# 	bigFile[word] = 0
	# # print("charLength : ", charactersOfFile2)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # for word in smallFile:
	# # 	if smallFile[word] > 0:
	# # 		print(word)
	# # 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("smallFileChars : ", smallFileChars)
	print("bigFileChars : ", bigFileChars)
	print("Percentage Distance : ", (costToChangeLargeFileToSmallFile * 100) / bigFileChars)
	# print("LCSDistanceMap : ",LCSDistanceMap)
	return True if ((costToChangeLargeFileToSmallFile * 100) / bigFileChars) < 41.0 else False


def get_len(key):
    return len(key[0])

def DetectPlagarismInTextFiles4(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file1))
	file2WordBag = prepareBagOfWordsWithFrequency(readDataFromFile(file2))
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

	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag

	test_dict_list = list(smallFile.items())
	test_dict_list.sort(key=get_len)
	res = {ele[0]: ele[1] for ele in reversed(test_dict_list)}
	smallFile = res
	EditDistanceMap = {}
	for word2 in smallFile:
		# tempDict = {}
		# print(word2)
		for word1 in bigFile:
			temp = EditDistanceProblem(word1, word2)
			if temp in EditDistanceMap:
				EditDistanceMap[temp].append([word1, word2])
			else:
				EditDistanceMap[temp]=[[word1, word2]]

	print(EditDistanceMap)
			# tempDict[word2] = EditDistanceProblem(word1, word2);
			# lst.append([word2, EditDistanceProblem(word1, word2)])
		# EditDistanceMap[word1] = tempDict
	print("small : ", len(smallFile), " charactersOfFile1 : ", charactersOfFile1, " Temp : ", len(file1WordBag))
	print("big : ", len(bigFile), " charactersOfFile2 : ", charactersOfFile2, " Temp : ", len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ", smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ", bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

	# LCSDistanceMap = {}
	# for word1 in bigFile:
	# 	lst = []
	# 	for word2 in smallFile:
	# 		lst.append([word2, LCS(word1, word2)])
	# 	LCSDistanceMap[word1] = lst
	#
	for word, key2 in EditDistanceMap[0]:
		# lst = EditDistanceMap[word]
		# for key2, distance in lst:
		# 	if distance == 0:
		print("Word : ", word, " key2 : ", key2)
		if smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] < bigFile[word]:
			#				print("first")
			bigFile[word] = bigFile[word] - smallFile[key2]
			smallFile[key2] = 0

		elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] > bigFile[word]:
			#				print("second")
			smallFile[key2] = smallFile[key2] - bigFile[word]
			bigFile[word] = 0
		elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] == bigFile[word]:
			smallFile[key2] = 0
			bigFile[word] = 0

	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	#
	words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0

	for distanceKey in sorted(EditDistanceMap.keys()):
		if distanceKey != 0:
			some_edit_exists = True
			# while some_edit_exists:
			smallKey1 = None
			bigKey1 = None
			charLength = None
			for word, key2 in EditDistanceMap[distanceKey]:
				if bigFile[word] > 0 and smallFile[key2] > 0 and charLength == None:
					charLength = len(key2)
					bigKey1 = word
					smallKey1 = key2
				# elif bigFile[word] > 0 and smallFile[key2] > 0 and charLength < len(key2):
				# 	charLength = len(key2)
				# 	bigKey1 = word
				# 	smallKey1 = key2
				# if smallKey1 != None:
					# print("=================")
					print(bigKey1," -> ",smallKey1," -> ",distanceKey)
					# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
					# print(smallFile)
					# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
					# print("===================")
					if smallFile[smallKey1] < bigFile[bigKey1]:
						# print("first")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
								smallFile[smallKey1] * distanceKey)
						bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
						smallFile[smallKey1] = 0

					else:
						# print("second")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
									bigFile[bigKey1] * distanceKey)
						smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
						bigFile[bigKey1] = 0
					charLength = None
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("small : ",smallFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("big : ",bigFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# else:
					# some_edit_exists = False

	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			# for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 				# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					# print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 			# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	print("FWord : ", bigKey1, " key2 : ", smallKey1, " distance : ", minDistance)
	# 	if smallKey1 != None:
	# 		# print("=================")
	# 		# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		# print(smallFile)
	# 		# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		# print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			# print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 						smallFile[smallKey1] * minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
	#
	# 		else:
	# 			# print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1] * minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("small : ",smallFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("big : ",bigFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word] * len(word))
			bigFile[word] = 0

	# 	bigFile[word] = 0
	# # print("charLength : ", charactersOfFile2)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # for word in smallFile:
	# # 	if smallFile[word] > 0:
	# # 		print(word)
	# # 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("smallFileChars : ", smallFileChars)
	print("bigFileChars : ", bigFileChars)
	print("Percentage Distance : ", (costToChangeLargeFileToSmallFile * 100) / bigFileChars)
	# print("LCSDistanceMap : ",LCSDistanceMap)
	return True if ((costToChangeLargeFileToSmallFile * 100) / bigFileChars) < 41.0 else False

def DetectPlagarismInTextFiles5(file1, file2):
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

	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag

	test_dict_list = list(smallFile.items())
	test_dict_list.sort(key=get_len)
	res = {ele[0]: ele[1] for ele in reversed(test_dict_list)}
	smallFile = res
	EditDistanceMap = {}
	for word2 in smallFile:
		# tempDict = {}
		# print(word2)
		for word1 in bigFile:

			temp = EditDistanceProblem(word1, word2)
			if temp == 0:
				if smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] < bigFile[word1]:
					#				print("first")
					bigFile[word1] = bigFile[word1] - smallFile[word2]
					smallFile[word2] = 0

				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] > bigFile[word1]:
					#				print("second")
					smallFile[word2] = smallFile[word2] - bigFile[word1]
					bigFile[word1] = 0
				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] == bigFile[word1]:
					smallFile[word2] = 0
					bigFile[word1] = 0
			elif bigFile[word1] > 0 and smallFile[word2] > 0:
				if temp in EditDistanceMap:
					EditDistanceMap[temp].append([word1, word2])
				else:
					EditDistanceMap[temp]=[[word1, word2]]

	print(EditDistanceMap)
			# tempDict[word2] = EditDistanceProblem(word1, word2);
			# lst.append([word2, EditDistanceProblem(word1, word2)])
		# EditDistanceMap[word1] = tempDict
	print("small : ", len(smallFile), " charactersOfFile1 : ", charactersOfFile1, " Temp : ", len(file1WordBag))
	print("big : ", len(bigFile), " charactersOfFile2 : ", charactersOfFile2, " Temp : ", len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ", smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ", bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

	# LCSDistanceMap = {}
	# for word1 in bigFile:
	# 	lst = []
	# 	for word2 in smallFile:
	# 		lst.append([word2, LCS(word1, word2)])
	# 	LCSDistanceMap[word1] = lst
	#
	# for word, key2 in EditDistanceMap[0]:
	# 	# lst = EditDistanceMap[word]
	# 	# for key2, distance in lst:
	# 	# 	if distance == 0:
	# 	print("Word : ", word, " key2 : ", key2)
	# 	if smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] < bigFile[word]:
	# 		#				print("first")
	# 		bigFile[word] = bigFile[word] - smallFile[key2]
	# 		smallFile[key2] = 0
	#
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] > bigFile[word]:
	# 		#				print("second")
	# 		smallFile[key2] = smallFile[key2] - bigFile[word]
	# 		bigFile[word] = 0
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] == bigFile[word]:
	# 		smallFile[key2] = 0
	# 		bigFile[word] = 0

	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	#
	# words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0

	for distanceKey in sorted(EditDistanceMap.keys()):
		if distanceKey != 0:
			some_edit_exists = True
			# while some_edit_exists:
			smallKey1 = None
			bigKey1 = None
			charLength = None
			for word, key2 in EditDistanceMap[distanceKey]:
				if bigFile[word] > 0 and smallFile[key2] > 0 and charLength == None:
					charLength = len(key2)
					bigKey1 = word
					smallKey1 = key2
				# elif bigFile[word] > 0 and smallFile[key2] > 0 and charLength < len(key2):
				# 	charLength = len(key2)
				# 	bigKey1 = word
				# 	smallKey1 = key2
				# if smallKey1 != None:
					# print("=================")
					print(bigKey1," -> ",smallKey1," -> ",distanceKey)
					# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
					# print(smallFile)
					# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
					# print("===================")
					if smallFile[smallKey1] < bigFile[bigKey1]:
						# print("first")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
								smallFile[smallKey1] * distanceKey)
						bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
						smallFile[smallKey1] = 0

					else:
						# print("second")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
									bigFile[bigKey1] * distanceKey)
						smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
						bigFile[bigKey1] = 0
					charLength = None
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("small : ",smallFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("big : ",bigFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# else:
					# some_edit_exists = False

	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			# for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 				# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					# print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 			# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	print("FWord : ", bigKey1, " key2 : ", smallKey1, " distance : ", minDistance)
	# 	if smallKey1 != None:
	# 		# print("=================")
	# 		# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		# print(smallFile)
	# 		# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		# print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			# print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 						smallFile[smallKey1] * minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
	#
	# 		else:
	# 			# print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1] * minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("small : ",smallFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("big : ",bigFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word] * len(word))
			bigFile[word] = 0

	# 	bigFile[word] = 0
	# # print("charLength : ", charactersOfFile2)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # for word in smallFile:
	# # 	if smallFile[word] > 0:
	# # 		print(word)
	# # 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("smallFileChars : ", smallFileChars)
	print("bigFileChars : ", bigFileChars)
	print("Percentage Distance : ", (costToChangeLargeFileToSmallFile * 100) / bigFileChars)
	# print("LCSDistanceMap : ",LCSDistanceMap)
	return True if ((costToChangeLargeFileToSmallFile * 100) / bigFileChars) < 41.0 else False

def DetectPlagarismInTextFiles6(file1, file2):
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
	test_dict_list = list(smallFile.items())
	test_dict_list.sort(key=get_len)
	res = {ele[0]: ele[1] for ele in reversed(test_dict_list)}
	smallFile = res
	EditDistanceMap = {}
	for word2 in smallFile:
		# tempDict = {}
		# print(word2)
		for word1 in bigFile:

			temp = EditDistanceProblem(word1, word2)
			if temp == 0:
				if smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] < bigFile[word1]:
					#				print("first")
					bigFile[word1] = bigFile[word1] - smallFile[word2]
					smallFile[word2] = 0

				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] > bigFile[word1]:
					#				print("second")
					smallFile[word2] = smallFile[word2] - bigFile[word1]
					bigFile[word1] = 0
				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] == bigFile[word1]:
					smallFile[word2] = 0
					bigFile[word1] = 0
			elif bigFile[word1] > 0 and smallFile[word2] > 0:
				if temp in EditDistanceMap:
					EditDistanceMap[temp].append([word1, word2])
				else:
					EditDistanceMap[temp]=[[word1, word2]]

	print(EditDistanceMap)
			# tempDict[word2] = EditDistanceProblem(word1, word2);
			# lst.append([word2, EditDistanceProblem(word1, word2)])
		# EditDistanceMap[word1] = tempDict
	print("small : ", len(smallFile), " charactersOfFile1 : ", charactersOfFile1, " Temp : ", len(file1WordBag))
	print("big : ", len(bigFile), " charactersOfFile2 : ", charactersOfFile2, " Temp : ", len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ", smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ", bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

	# LCSDistanceMap = {}
	# for word1 in bigFile:
	# 	lst = []
	# 	for word2 in smallFile:
	# 		lst.append([word2, LCS(word1, word2)])
	# 	LCSDistanceMap[word1] = lst
	#
	# for word, key2 in EditDistanceMap[0]:
	# 	# lst = EditDistanceMap[word]
	# 	# for key2, distance in lst:
	# 	# 	if distance == 0:
	# 	print("Word : ", word, " key2 : ", key2)
	# 	if smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] < bigFile[word]:
	# 		#				print("first")
	# 		bigFile[word] = bigFile[word] - smallFile[key2]
	# 		smallFile[key2] = 0
	#
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] > bigFile[word]:
	# 		#				print("second")
	# 		smallFile[key2] = smallFile[key2] - bigFile[word]
	# 		bigFile[word] = 0
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] == bigFile[word]:
	# 		smallFile[key2] = 0
	# 		bigFile[word] = 0

	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	#
	# words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0

	for distanceKey in sorted(EditDistanceMap.keys()):
		if distanceKey != 0:
			some_edit_exists = True
			# while some_edit_exists:
			smallKey1 = None
			bigKey1 = None
			charLength = None
			for word, key2 in EditDistanceMap[distanceKey]:
				if bigFile[word] > 0 and smallFile[key2] > 0 and charLength == None:
					charLength = len(key2)
					bigKey1 = word
					smallKey1 = key2
				# elif bigFile[word] > 0 and smallFile[key2] > 0 and charLength < len(key2):
				# 	charLength = len(key2)
				# 	bigKey1 = word
				# 	smallKey1 = key2
				# if smallKey1 != None:
					# print("=================")
					print(bigKey1," -> ",smallKey1," -> ",distanceKey)
					# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
					# print(smallFile)
					# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
					# print("===================")
					if smallFile[smallKey1] < bigFile[bigKey1]:
						# print("first")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
								smallFile[smallKey1] * distanceKey)
						bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
						smallFile[smallKey1] = 0

					else:
						# print("second")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
									bigFile[bigKey1] * distanceKey)
						smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
						bigFile[bigKey1] = 0
					charLength = None
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("small : ",smallFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("big : ",bigFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# else:
					# some_edit_exists = False

	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			# for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 				# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					# print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 			# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	print("FWord : ", bigKey1, " key2 : ", smallKey1, " distance : ", minDistance)
	# 	if smallKey1 != None:
	# 		# print("=================")
	# 		# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		# print(smallFile)
	# 		# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		# print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			# print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 						smallFile[smallKey1] * minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
	#
	# 		else:
	# 			# print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1] * minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("small : ",smallFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("big : ",bigFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word] * len(word))
			bigFile[word] = 0

	# 	bigFile[word] = 0
	# # print("charLength : ", charactersOfFile2)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # for word in smallFile:
	# # 	if smallFile[word] > 0:
	# # 		print(word)
	# # 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("smallFileChars : ", smallFileChars)
	print("bigFileChars : ", bigFileChars)
	print("Percentage Distance : ", (costToChangeLargeFileToSmallFile * 100) / bigFileChars)
	# print("LCSDistanceMap : ",LCSDistanceMap)
	return True if ((costToChangeLargeFileToSmallFile * 100) / bigFileChars) < 39.0 else False


def DetectPlagarismInTextFiles7(file1, file2):
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

	#
	# if len(smallRefFile) > 0:
	# 	smallRefFileTemp = {}
	# 	smallRefFileTemp2 = {}
	# 	for word in smallRefFile:
	# 		for word2 in smallFile:
	# 			temp2 = EditDistanceProblem(word, word2)
	# 			temp = LCS(word, word2)
	#
	# 			if temp2 == 0:
	# 				smallFile[word2] = 0
	# 			elif temp > (len(word) * 66 // 100) and smallRefFile[word] > 0 and word not in ["https", "http", "www",
	# 																						  "google", "wikipedia",
	# 																						  "wiki", "com", "en",
	# 																						  "org"]:
	# 				smallFile[word2] = 0
	# 				if temp in smallRefFileTemp:
	# 					smallRefFileTemp[temp].append([word, word2])
	# 				else:
	# 					smallRefFileTemp[temp] = [[word, word2]]
	# 			elif temp2 < (len(word) * 82 // 100) and smallRefFile[word] > 0 and word not in ["https", "http", "www",
	# 																						   "google", "wikipedia",
	# 																						   "wiki", "com", "en",
	# 																						   "org"]:
	# 				smallFile[word2] = 0
	# 				if temp2 in smallRefFileTemp2:
	# 					smallRefFileTemp2[temp2].append([word, word2])
	# 				else:
	# 					smallRefFileTemp2[temp2] = [[word, word2]]
	# 	print("@@ MEME @@ : SMALL ", smallRefFileTemp)
	# 	print("@@ MEME @@ : SMALL 2", smallRefFileTemp2)
	#
	# if len(bigRefFile) > 0:
	# 	bigRefFileTemp = {}
	# 	bigRefFileTemp2 = {}
	# 	for word in bigRefFile:
	# 		for word2 in bigFile:
	# 			temp2 = EditDistanceProblem(word, word2)
	# 			temp = LCS(word, word2)
	#
	# 			if temp2 == 0:
	# 			# 	if bigFile[word2] > bigRefFile[word]:
	# 			# 		bigFile[word2] = bigFile[word2] - bigRefFile[word]
	# 			# 		bigRefFile[word] = 0
	# 			# 	else:
	# 			# 		bigRefFile[word] = bigRefFile[word] - bigFile[word2]
	# 					bigFile[word2] = 0
	# 			elif temp > (len(word) * 66 //100) and bigRefFile[word]>0 and word not in ["https","http","www","google","wikipedia","wiki","com","en","org"]:
	# 				bigFile[word2] = 0
	# 				if temp in bigRefFileTemp:
	# 					bigRefFileTemp[temp].append([word, word2])
	# 				else:
	# 					bigRefFileTemp[temp] = [[word, word2]]
	# 			elif temp2 < (len(word) * 82 // 100) and bigRefFile[word]>0 and word not in ["https","http","www","google","wikipedia","wiki","com","en","org"]:
	# 				bigFile[word2] = 0
	# 				if temp2 in bigRefFileTemp2:
	# 					bigRefFileTemp2[temp2].append([word, word2])
	# 				else:
	# 					bigRefFileTemp2[temp2] = [[word, word2]]
	# 	print("@@ MEME @@ : BIG ", bigRefFileTemp)
	# 	print("@@ MEME @@ : BIG 2", bigRefFileTemp2)
	test_dict_list = list(smallFile.items())
	test_dict_list.sort(key=get_len)
	res = {ele[0]: ele[1] for ele in reversed(test_dict_list)}
	smallFile = res
	EditDistanceMap = {}
	for word2 in smallFile:
		# tempDict = {}
		# print(word2)
		for word1 in bigFile:

			temp = EditDistanceProblem(word1, word2)
			if temp == 0:
				if smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] < bigFile[word1]:
					#				print("first")
					bigFile[word1] = bigFile[word1] - smallFile[word2]
					smallFile[word2] = 0

				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] > bigFile[word1]:
					#				print("second")
					smallFile[word2] = smallFile[word2] - bigFile[word1]
					bigFile[word1] = 0
				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] == bigFile[word1]:
					smallFile[word2] = 0
					bigFile[word1] = 0
			elif bigFile[word1] > 0 and smallFile[word2] > 0 and len(word2) > (len(word1) *80//100) and len(word2) < (len(word1) *120//100):
				if temp in EditDistanceMap:
					EditDistanceMap[temp].append([word1, word2])
				else:
					EditDistanceMap[temp]=[[word1, word2]]

	print(EditDistanceMap)
			# tempDict[word2] = EditDistanceProblem(word1, word2);
			# lst.append([word2, EditDistanceProblem(word1, word2)])
		# EditDistanceMap[word1] = tempDict
	print("small : ", len(smallFile), " charactersOfFile1 : ", charactersOfFile1, " Temp : ", len(file1WordBag))
	print("big : ", len(bigFile), " charactersOfFile2 : ", charactersOfFile2, " Temp : ", len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ", smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ", bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

	# LCSDistanceMap = {}
	# for word1 in bigFile:
	# 	lst = []
	# 	for word2 in smallFile:
	# 		lst.append([word2, LCS(word1, word2)])
	# 	LCSDistanceMap[word1] = lst
	#
	# for word, key2 in EditDistanceMap[0]:
	# 	# lst = EditDistanceMap[word]
	# 	# for key2, distance in lst:
	# 	# 	if distance == 0:
	# 	print("Word : ", word, " key2 : ", key2)
	# 	if smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] < bigFile[word]:
	# 		#				print("first")
	# 		bigFile[word] = bigFile[word] - smallFile[key2]
	# 		smallFile[key2] = 0
	#
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] > bigFile[word]:
	# 		#				print("second")
	# 		smallFile[key2] = smallFile[key2] - bigFile[word]
	# 		bigFile[word] = 0
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] == bigFile[word]:
	# 		smallFile[key2] = 0
	# 		bigFile[word] = 0

	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	#
	# words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0

	for distanceKey in sorted(EditDistanceMap.keys()):
		if distanceKey != 0:
			some_edit_exists = True
			# while some_edit_exists:
			smallKey1 = None
			bigKey1 = None
			charLength = None
			for word, key2 in EditDistanceMap[distanceKey]:
				if bigFile[word] > 0 and smallFile[key2] > 0 and charLength == None:
					charLength = len(key2)
					bigKey1 = word
					smallKey1 = key2
				# elif bigFile[word] > 0 and smallFile[key2] > 0 and charLength < len(key2):
				# 	charLength = len(key2)
				# 	bigKey1 = word
				# 	smallKey1 = key2
				# if smallKey1 != None:
					# print("=================")
					print(bigKey1," -> ",smallKey1," -> ",distanceKey)
					# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
					# print(smallFile)
					# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
					# print("===================")
					if smallFile[smallKey1] < bigFile[bigKey1]:
						# print("first")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
								smallFile[smallKey1] * distanceKey)
						bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
						smallFile[smallKey1] = 0

					else:
						# print("second")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
									bigFile[bigKey1] * distanceKey)
						smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
						bigFile[bigKey1] = 0
					charLength = None
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("small : ",smallFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("big : ",bigFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# else:
					# some_edit_exists = False

	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			# for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 				# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					# print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 			# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	print("FWord : ", bigKey1, " key2 : ", smallKey1, " distance : ", minDistance)
	# 	if smallKey1 != None:
	# 		# print("=================")
	# 		# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		# print(smallFile)
	# 		# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		# print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			# print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 						smallFile[smallKey1] * minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
	#
	# 		else:
	# 			# print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1] * minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("small : ",smallFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("big : ",bigFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word] * len(word))
			bigFile[word] = 0

	# 	bigFile[word] = 0
	# # print("charLength : ", charactersOfFile2)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # for word in smallFile:
	# # 	if smallFile[word] > 0:
	# # 		print(word)
	# # 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("smallFileChars : ", smallFileChars)
	print("bigFileChars : ", bigFileChars)
	print("Percentage Distance : ", (costToChangeLargeFileToSmallFile * 100) / bigFileChars)
	# print("LCSDistanceMap : ",LCSDistanceMap)
	return True if ((costToChangeLargeFileToSmallFile * 100) / bigFileChars) < 39.0 else False



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


	# test_dict_list = list(smallFile.items())
	# test_dict_list.sort(key=get_len)
	# res = {ele[0]: ele[1] for ele in reversed(test_dict_list)}
	# smallFile = res
	# EditDistanceMap = {}
	# for word2 in smallFile:
	# 	# tempDict = {}
	# 	# print(word2)
	# 	for word1 in bigFile:
	#
	# 		temp = EditDistanceProblem(word1, word2)
	# 		if temp == 0:
	# 			if smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] < bigFile[word1]:
	# 				#				print("first")
	# 				bigFile[word1] = bigFile[word1] - smallFile[word2]
	# 				smallFile[word2] = 0
	#
	# 			elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] > bigFile[word1]:
	# 				#				print("second")
	# 				smallFile[word2] = smallFile[word2] - bigFile[word1]
	# 				bigFile[word1] = 0
	# 			elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] == bigFile[word1]:
	# 				smallFile[word2] = 0
	# 				bigFile[word1] = 0
	# 		elif bigFile[word1] > 0 and smallFile[word2] > 0 and len(word2) > (len(word1) *80//100) and len(word2) < (len(word1) *120//100):
	# 			if temp in EditDistanceMap:
	# 				EditDistanceMap[temp].append([word1, word2])
	# 			else:
	# 				EditDistanceMap[temp]=[[word1, word2]]

	# print(EditDistanceMap)
			# tempDict[word2] = EditDistanceProblem(word1, word2);
			# lst.append([word2, EditDistanceProblem(word1, word2)])
		# EditDistanceMap[word1] = tempDict
	print("small : ", len(smallFile), " charactersOfFile1 : ", charactersOfFile1, " Temp : ", len(file1WordBag))
	print("big : ", len(bigFile), " charactersOfFile2 : ", charactersOfFile2, " Temp : ", len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ", smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ", bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

	# LCSDistanceMap = {}
	# for word1 in bigFile:
	# 	lst = []
	# 	for word2 in smallFile:
	# 		lst.append([word2, LCS(word1, word2)])
	# 	LCSDistanceMap[word1] = lst
	#
	# for word, key2 in EditDistanceMap[0]:
	# 	# lst = EditDistanceMap[word]
	# 	# for key2, distance in lst:
	# 	# 	if distance == 0:
	# 	print("Word : ", word, " key2 : ", key2)
	# 	if smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] < bigFile[word]:
	# 		#				print("first")
	# 		bigFile[word] = bigFile[word] - smallFile[key2]
	# 		smallFile[key2] = 0
	#
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] > bigFile[word]:
	# 		#				print("second")
	# 		smallFile[key2] = smallFile[key2] - bigFile[word]
	# 		bigFile[word] = 0
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] == bigFile[word]:
	# 		smallFile[key2] = 0
	# 		bigFile[word] = 0

	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	#
	# words = bigFile.keys()
	# costToChangeLargeFileToSmallFile = 0
	#
	# for distanceKey in sorted(EditDistanceMap.keys()):
	# 	if distanceKey != 0:
	# 		some_edit_exists = True
	# 		# while some_edit_exists:
	# 		smallKey1 = None
	# 		bigKey1 = None
	# 		charLength = None
	# 		for word, key2 in EditDistanceMap[distanceKey]:
	# 			if bigFile[word] > 0 and smallFile[key2] > 0 and charLength == None:
	# 				charLength = len(key2)
	# 				bigKey1 = word
	# 				smallKey1 = key2
	# 			# elif bigFile[word] > 0 and smallFile[key2] > 0 and charLength < len(key2):
	# 			# 	charLength = len(key2)
	# 			# 	bigKey1 = word
	# 			# 	smallKey1 = key2
	# 			# if smallKey1 != None:
	# 				# print("=================")
	# 				print(bigKey1," -> ",smallKey1," -> ",distanceKey)
	# 				# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 				# print(smallFile)
	# 				# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 				# print("===================")
	# 				if smallFile[smallKey1] < bigFile[bigKey1]:
	# 					# print("first")
	# 					costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 							smallFile[smallKey1] * distanceKey)
	# 					bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 					smallFile[smallKey1] = 0
	#
	# 				else:
	# 					# print("second")
	# 					costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 								bigFile[bigKey1] * distanceKey)
	# 					smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 					bigFile[bigKey1] = 0
	# 				charLength = None
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("small : ",smallFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# print("big : ",bigFile)
				# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				# else:
					# some_edit_exists = False

	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			# for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 				# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					# print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 			# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	print("FWord : ", bigKey1, " key2 : ", smallKey1, " distance : ", minDistance)
	# 	if smallKey1 != None:
	# 		# print("=================")
	# 		# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		# print(smallFile)
	# 		# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		# print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			# print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 						smallFile[smallKey1] * minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
	#
	# 		else:
	# 			# print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1] * minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("small : ",smallFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("big : ",bigFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	# print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# for word in bigFile:
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
	# 	if bigFile[word] > 0:
	# 		print(word)
	# 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word] * len(word))
	# 		bigFile[word] = 0
	#
	# # 	bigFile[word] = 0
	# # # print("charLength : ", charactersOfFile2)
	# # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # print(smallFile)
	# # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # print(bigFile)
	# # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# # # for word in smallFile:
	# # # 	if smallFile[word] > 0:
	# # # 		print(word)
	# # # 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	# bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	# smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	# print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	# print("smallFileChars : ", smallFileChars)
	# print("bigFileChars : ", bigFileChars)
	# print("Percentage Distance : ", (costToChangeLargeFileToSmallFile * 100) / bigFileChars)
	# print("LCSDistanceMap : ",LCSDistanceMap)





def DetectPlagarismInCodeFiles3(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequencyForCode(readDataFromCode(file1))
	file2WordBag = prepareBagOfWordsWithFrequencyForCode(readDataFromCode(file2))
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

	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag
	# print("SmallFile : ",len(smallFile))
	# print("BigFile : ",len(bigFile))

	#
	# smallFile, smallRefFile = {},{}
	# bigFile, bigRefFile = {},{}
	# smallFile, smallRefFile = file1WordBag,file1RefLinkWords if charactersOfFile1 < charactersOfFile2 else file2WordBag, file2RefLinkWords
	# bigFile, bigRefFile = file2WordBag, file2RefLinkWords if charactersOfFile2 > charactersOfFile1 else file1WordBag, file1RefLinkWords
	# if charactersOfFile1 < charactersOfFile2:
	# 	smallFile, smallRefFile = file1WordBag, file1RefLinkWords
	# else:
	# 	smallFile, smallRefFile = file2WordBag, file2RefLinkWords
	#
	# if charactersOfFile2 > charactersOfFile1:
	# 	bigFile, bigRefFile = file2WordBag, file2RefLinkWords
	# else:
	# 	bigFile, bigRefFile = file1WordBag, file1RefLinkWords


	# if len(smallRefFile) > 0:
	# 	smallRefFileTemp = {}
	# 	smallRefFileTemp2 = {}
	# 	for word in smallRefFile:
	# 		for word2 in smallFile:
	# 			temp2 = EditDistanceProblem(word, word2)
	# 			temp = LCS(word, word2)
	#
	# 			if temp2 == 0:
	# 				smallFile[word2] = 0
				# elif temp > (len(word) * 66 // 100) and smallRefFile[word] > 0 and word not in ["https", "http", "www",
				# 																			  "google", "wikipedia",
				# 																			  "wiki", "com", "en",
				# 																			  "org"]:
				# 	smallFile[word2] = 0
				# 	if temp in smallRefFileTemp:
				# 		smallRefFileTemp[temp].append([word, word2])
				# 	else:
				# 		smallRefFileTemp[temp] = [[word, word2]]
				# elif temp2 < (len(word) * 82 // 100) and smallRefFile[word] > 0 and word not in ["https", "http", "www",
				# 																			   "google", "wikipedia",
				# 																			   "wiki", "com", "en",
				# 																			   "org"]:
				# 	smallFile[word2] = 0
				# 	if temp2 in smallRefFileTemp2:
				# 		smallRefFileTemp2[temp2].append([word, word2])
				# 	else:
				# 		smallRefFileTemp2[temp2] = [[word, word2]]
		# print("@@ MEME @@ : SMALL ", smallRefFileTemp)
		# print("@@ MEME @@ : SMALL 2", smallRefFileTemp2)

	# if len(bigRefFile) > 0:
	# 	bigRefFileTemp = {}
	# 	bigRefFileTemp2 = {}
	# 	for word in bigRefFile:
	# 		for word2 in bigFile:
	# 			temp2 = EditDistanceProblem(word, word2)
	# 			temp = LCS(word, word2)
	#
	# 			if temp2 == 0:
				# 	if bigFile[word2] > bigRefFile[word]:
				# 		bigFile[word2] = bigFile[word2] - bigRefFile[word]
				# 		bigRefFile[word] = 0
				# 	else:
				# 		bigRefFile[word] = bigRefFile[word] - bigFile[word2]
				# 		bigFile[word2] = 0
				# elif temp > (len(word) * 66 //100) and bigRefFile[word]>0 and word not in ["https","http","www","google","wikipedia","wiki","com","en","org"]:
				# 	bigFile[word2] = 0
				# 	if temp in bigRefFileTemp:
				# 		bigRefFileTemp[temp].append([word, word2])
				# 	else:
				# 		bigRefFileTemp[temp] = [[word, word2]]
				# elif temp2 < (len(word) * 82 // 100) and bigRefFile[word]>0 and word not in ["https","http","www","google","wikipedia","wiki","com","en","org"]:
				# 	bigFile[word2] = 0
				# 	if temp2 in bigRefFileTemp2:
				# 		bigRefFileTemp2[temp2].append([word, word2])
				# 	else:
				# 		bigRefFileTemp2[temp2] = [[word, word2]]
		# print("@@ MEME @@ : BIG ", bigRefFileTemp)
		# print("@@ MEME @@ : BIG 2", bigRefFileTemp2)
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


def DetectPlagarismInCodeFiles(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequency(readDataFromCode(file1))
	file2WordBag = prepareBagOfWordsWithFrequency(readDataFromCode(file2))
	#smallFile = file1WordBag if len(file1WordBag) < len(file2WordBag) else file2WordBag
	#bigFile = file2WordBag if len(file2WordBag) > len(file1WordBag) else file1WordBag
	#print("SmallFile : ",len(smallFile))
	#print("BigFile : ",len(bigFile))
	charactersOfFile1 = 0
	for word in file1WordBag:
		charactersOfFile1 = charactersOfFile1 + (file1WordBag[word]*len(word))
		
	charactersOfFile2 = 0
	for word in file2WordBag:
		charactersOfFile2 = charactersOfFile2 + (file2WordBag[word]*len(word))
	
	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag
		
	EditDistanceMap = {}
	for word1 in bigFile:
		lst = []
		for word2 in smallFile:
			lst.append([word2,EditDistanceProblem(word1, word2)])
		EditDistanceMap[word1] = lst
	print("small : ",len(smallFile)," charactersOfFile1 : ",charactersOfFile1," Temp : ",len(file1WordBag))
	print("big : ",len(bigFile)," charactersOfFile2 : ",charactersOfFile2," Temp : ",len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ",smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ",bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	
	for word in EditDistanceMap:
		lst = EditDistanceMap[word]
		for key2, distance in lst:
			if distance == 0:
				print("Word : ",word," key2 : ",key2," distance : ",distance)
				if smallFile[key2] < bigFile[word]:
	#				print("first")
					bigFile[word] = bigFile[word] - smallFile[key2]
					smallFile[key2] = 0
					
				else:
	#				print("second")
					smallFile[key2] = smallFile[key2] - bigFile[word]
					bigFile[word] = 0
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	
	words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0
	
	while len(words) > 0:
		smallKey1 = None
		bigKey1 = None
		minDistance = 1000000
		for word in words:
			if bigFile[word] > 0:
				#for word in EditDistanceMap:
				lst = EditDistanceMap[word]
				for key2, distance in lst:
					if distance != 0 and distance < minDistance and smallFile[key2] > 0:
						smallKey1 = key2
						bigKey1 = word
						minDistance = distance
						# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
					if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
						#print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
						smallKey1 = key2
						bigKey1 = word
						minDistance = distance
						# print("same : ",word," key2 : ",key2," distance : ",distance)
				#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
		# print("FWord : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
		if smallKey1 != None:
			if smallFile[smallKey1] < bigFile[bigKey1]:
				#print("first")
				costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[smallKey1]*minDistance)
				bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
				smallFile[smallKey1] = 0
				
			else:
				#print("second")
				costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1]*minDistance)
				smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
				bigFile[bigKey1] = 0
			# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			# print("small : ",smallFile)
			# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			# print("big : ",bigFile)
			# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		else:
			break
	print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		#costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word]*len(word))
			
		bigFile[word] = 0
	#print("charLength : ", charactersOfFile2)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# for word in smallFile:
	# 	if smallFile[word] > 0:
	# 		print(word)
	# 		costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (smallFile[word]*len(word))
	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ",costToChangeLargeFileToSmallFile)
	print("smallFileChars : ",smallFileChars)
	print("bigFileChars : ",bigFileChars)
	print("Percentage Distance : ",	(costToChangeLargeFileToSmallFile * 100)/bigFileChars)
	print("From Code Comparision")
	return True if ((costToChangeLargeFileToSmallFile * 100)/bigFileChars) < 58.0 else False


def DetectPlagarismInCodeFiles2(file1, file2):
	file1WordBag = prepareBagOfWordsWithFrequencyForCode(readDataFromCode(file1))
	file2WordBag = prepareBagOfWordsWithFrequencyForCode(readDataFromCode(file2))
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

	smallFile = file1WordBag if charactersOfFile1 < charactersOfFile2 else file2WordBag
	bigFile = file2WordBag if charactersOfFile2 > charactersOfFile1 else file1WordBag

	test_dict_list = list(smallFile.items())
	test_dict_list.sort(key=get_len)
	res = {ele[0]: ele[1] for ele in reversed(test_dict_list)}
	smallFile = res
	EditDistanceMap = {}
	for word2 in smallFile:
		# tempDict = {}
		# print(word2)
		for word1 in bigFile:
			temp = EditDistanceProblem(word1, word2)
			if temp == 0:
				if smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] < bigFile[word1]:
					#				print("first")
					bigFile[word1] = bigFile[word1] - smallFile[word2]
					smallFile[word2] = 0

				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] > bigFile[word1]:
					#				print("second")
					smallFile[word2] = smallFile[word2] - bigFile[word1]
					bigFile[word1] = 0
				elif smallFile[word2] != 0 and bigFile[word1] != 0 and smallFile[word2] == bigFile[word1]:
					smallFile[word2] = 0
					bigFile[word1] = 0
			elif temp in EditDistanceMap:
				EditDistanceMap[temp].append([word1, word2])
			else:
				EditDistanceMap[temp] = [[word1, word2]]

	print(EditDistanceMap)
	# tempDict[word2] = EditDistanceProblem(word1, word2);
	# lst.append([word2, EditDistanceProblem(word1, word2)])
	# EditDistanceMap[word1] = tempDict
	print("small : ", len(smallFile), " charactersOfFile1 : ", charactersOfFile1, " Temp : ", len(file1WordBag))
	print("big : ", len(bigFile), " charactersOfFile2 : ", charactersOfFile2, " Temp : ", len(file2WordBag))
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("small : ", smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print("big : ", bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

	# LCSDistanceMap = {}
	# for word1 in bigFile:
	# 	lst = []
	# 	for word2 in smallFile:
	# 		lst.append([word2, LCS(word1, word2)])
	# 	LCSDistanceMap[word1] = lst
	#
	# for word, key2 in EditDistanceMap[0]:
	# 	# lst = EditDistanceMap[word]
	# 	# for key2, distance in lst:
	# 	# 	if distance == 0:
	# 	print("Word : ", word, " key2 : ", key2)
	# 	if smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] < bigFile[word]:
	# 		#				print("first")
	# 		bigFile[word] = bigFile[word] - smallFile[key2]
	# 		smallFile[key2] = 0
	#
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] > bigFile[word]:
	# 		#				print("second")
	# 		smallFile[key2] = smallFile[key2] - bigFile[word]
	# 		bigFile[word] = 0
	# 	elif smallFile[key2] != 0 and bigFile[word] !=0 and smallFile[key2] == bigFile[word]:
	# 		smallFile[key2] = 0
	# 		bigFile[word] = 0

	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(smallFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# print(bigFile)
	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	#
	# words = bigFile.keys()
	costToChangeLargeFileToSmallFile = 0

	for distanceKey in sorted(EditDistanceMap.keys()):
		if distanceKey != 0:
			some_edit_exists = True
			# while some_edit_exists:
			smallKey1 = None
			bigKey1 = None
			charLength = None
			for word, key2 in EditDistanceMap[distanceKey]:
				if bigFile[word] > 0 and smallFile[key2] > 0 and charLength == None:
					charLength = len(key2)
					bigKey1 = word
					smallKey1 = key2
					# elif bigFile[word] > 0 and smallFile[key2] > 0 and charLength < len(key2):
					# 	charLength = len(key2)
					# 	bigKey1 = word
					# 	smallKey1 = key2
					# if smallKey1 != None:
					# print("=================")
					print(bigKey1, " -> ", smallKey1, " -> ", distanceKey)
					# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
					# print(smallFile)
					# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
					# print("===================")
					if smallFile[smallKey1] < bigFile[bigKey1]:
						# print("first")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
								smallFile[smallKey1] * distanceKey)
						bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
						smallFile[smallKey1] = 0

					else:
						# print("second")
						costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
								bigFile[bigKey1] * distanceKey)
						smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
						bigFile[bigKey1] = 0
					charLength = None
		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		# print("small : ",smallFile)
		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		# print("big : ",bigFile)
		# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		# else:
		# some_edit_exists = False

	# while len(words) > 0:
	# 	smallKey1 = None
	# 	bigKey1 = None
	# 	minDistance = 1000000
	# 	for word in words:
	# 		if bigFile[word] > 0:
	# 			# for word in EditDistanceMap:
	# 			lst = EditDistanceMap[word]
	# 			for key2, distance in lst:
	# 				if distance != 0 and distance < minDistance and smallFile[key2] > 0:
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 				# print("Word : ",word," key2 : ",bigKey1," distance : ",minDistance)
	# 				if distance != 0 and distance == minDistance and smallFile[key2] > 0 and len(smallKey1) < len(key2):
	# 					# print("Word : ",smallKey1," key2 : ",bigKey1," distance : ",minDistance)
	# 					smallKey1 = key2
	# 					bigKey1 = word
	# 					minDistance = distance
	# 			# print("same : ",word," key2 : ",key2," distance : ",distance)
	# 	# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + 1
	# 	print("FWord : ", bigKey1, " key2 : ", smallKey1, " distance : ", minDistance)
	# 	if smallKey1 != None:
	# 		# print("=================")
	# 		# print("LCSDistanceMap [",bigKey1,",",smallKey1,"] = ",LCSDistanceMap[bigKey1])
	# 		# print(smallFile)
	# 		# print("EDITDISTANCE [",bigKey1,",",smallKey1,"] = ",EditDistanceMap[bigKey1])
	# 		# print("===================")
	# 		if smallFile[smallKey1] < bigFile[bigKey1]:
	# 			# print("first")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (
	# 						smallFile[smallKey1] * minDistance)
	# 			bigFile[bigKey1] = bigFile[bigKey1] - smallFile[smallKey1]
	# 			smallFile[smallKey1] = 0
	#
	# 		else:
	# 			# print("second")
	# 			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[bigKey1] * minDistance)
	# 			smallFile[smallKey1] = smallFile[smallKey1] - bigFile[bigKey1]
	# 			bigFile[bigKey1] = 0
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("small : ",smallFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	# print("big : ",bigFile)
	# 	# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	# 	else:
	# 		break
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(smallFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	print(bigFile)
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	for word in bigFile:
		# costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + bigFile[word]
		if bigFile[word] > 0:
			print(word)
			costToChangeLargeFileToSmallFile = costToChangeLargeFileToSmallFile + (bigFile[word] * len(word))
			bigFile[word] = 0


	bigFileChars = charactersOfFile1 if charactersOfFile1 > charactersOfFile2 else charactersOfFile2
	smallFileChars = charactersOfFile2 if charactersOfFile1 > charactersOfFile2 else charactersOfFile1
	print("costToChangeLargeFileToSmallFile : ", costToChangeLargeFileToSmallFile)
	print("smallFileChars : ", smallFileChars)
	print("bigFileChars : ", bigFileChars)
	print("Percentage Distance : ", (costToChangeLargeFileToSmallFile * 100) / bigFileChars)
	print("From Code Comparision")
	return True if ((costToChangeLargeFileToSmallFile * 100) / bigFileChars) < 58.0 else False
	
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
#print("File 1 Name : ",sys.argv[1],',File 2 Name : ',sys.argv[2])

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
	# 	plagarism_detected = DetectPlagarismInCodeFiles(sys.argv[1], sys.argv[2]) 
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
	
