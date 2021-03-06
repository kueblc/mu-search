import urllib
import string
import re
import remove_tags

def countWords(URL):

	##pageContent is a string holding the contents of the webpage
	pageContent = urllib.urlopen(URL).read()
	
	#pageContent = remove_tags.remove_tags(pageContent)
	
	
	##separatedWords is an array of strings used to hold the split contents of the page
	separateWords = pageContent.split()
	
	##get rid of punctuation
	strippedWords = []
	for word in separateWords:
		word = re.sub('[%s]'%re.escape(string.punctuation),'',word)
		strippedWords.append(word)
	
	wordCount = {}
	
	for word in strippedWords:
		if word in wordCount:
			count = wordCount[word]
			wordCount[word] += 1
		else:
			wordCount[word] = 1
			
		
	return wordCount
	
	
def countWordsFast(URL, keyWords):

	##pageContent is a string holding the contents of the webpage
	pageContent = urllib.urlopen(URL).read()
	
	#pageContent = remove_tags.remove_tags(pageContent)
	
	
	##separatedWords is an array of strings used to hold the split contents of the page
	separateWords = pageContent.split()
	
	##get rid of punctuation
	strippedWords = []
	for word in separateWords:
		word = re.sub('[%s]'%re.escape(string.punctuation),'',word)
		strippedWords.append(word)
	
	wordCount = {}
	
	count = 0;
	for word in strippedWords:
		count += 1;
		if word in keyWords:
			if word in wordCount:
				wordCount[word] += 1
			else:
				wordCount[word] = 1
			
		
	return wordCount, count

	
def wordPerLength(wordCounter, word):
	#wordCounter = countWords(URL)
	counter = 0.0
	for eachWord in wordCounter:
		counter += wordCounter[eachWord]
	
	ratio = wordCounter[word]/counter
	#print wordCounter[word]
	#print counter
	#print ratio
	return ratio
		
def numAppearances(wordCounter, word):
	#wordCounter = countWords(URL)
	count = wordCounter[word]
	return count
	
def testCount(arg):

	wordList = countWords(arg)
	
	for word in wordList:
		print word + "\n"
		print wordList[word]
