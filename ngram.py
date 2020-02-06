#Gabe Chambers - V00774588
#cmsc 416 -- NLP
#Project 2: Ngram
#to run: 
# cd "C:\Users\gabej\OneDrive\Documents\vcu\2020\spring\416\Programming Projects\ngrams\ngram"; python ngram.py 3 10 texty.txt textfile.txt

#Note: thinking that tables should be in structure: myTable = {'dark': {'night':3,'storm':2}, 'storm': {'night':0,'dark':5}, 'night': {'sorm':8,'dark':0}}
# https://www.w3schools.com/python/python_dictionaries.asp
# https://www.programiz.com/python-programming/nested-dictionary

import sys, re, os, json, random


#strip all symbols except [.?!]. also keeps alphanumeric and spaces
def stripSymbols(text):
    text = re.sub(r'[^a-zA-Z\d\s.!?]', '', text)
    return text


def splitToSentences(text):
    sentences = re.split(r'([.!?])', text)
    sentences.pop() #removes trailing empty "sentnece"
    phrases = []
    for index in range(len(sentences)):
        if re.search(r'^ +(.*?)$', sentences[index]) is not None:
            tokens = re.search(r'^ +(.*?)$', sentences[index])
            sentences[index] = tokens.group(1)
        if index % 2 != 0:
            sentence = [sentences[index-1] + sentences[index]]
            phrases.append(sentence)
    return phrases


def splitToWords(sentences):
    for sentence in range(len(sentences)):
        sentences[sentence][0] = sentences[sentence][0].replace('.', ' .')
        sentences[sentence][0] = sentences[sentence][0].replace('?', ' ?')
        sentences[sentence][0] = sentences[sentence][0].replace('!', ' !')
        sentences[sentence] = re.split(r'\s', sentences[sentence][0])
    return sentences



def pretty(nestedDict):
   print(json.dumps(nestedDict, sort_keys=True, indent=8))




def createNgramTable(fullTexts, N):
    bigramTable = {'<START>': {},
                    '<END>': {}}
    prev = '<START>'
    for book in fullTexts:
        for sentence in book:
            if len(sentence) >= N: #break if the sentence is shorter than the specified Ngram size
                for word in sentence:  
                    if prev in bigramTable:
                        if word in bigramTable[prev]:
                            bigramTable[prev][word] += 1
                        else:
                            bigramTable[prev][word] = 1
                    else:
                        bigramTable[prev] = {word: 1}
                    prev = word

                    if prev == '.' or prev == '!' or prev == '?':
                        word = '<END>'
                        if prev in bigramTable:
                            if word in bigramTable[prev]:
                                bigramTable[prev][word] += 1
                            else:
                                bigramTable[prev][word] = 1
                        else:
                            bigramTable[prev] = {word: 1}
                        prev = '<START>'
    #pretty(bigramTable)

    return(freqToAscendRatio(bigramTable))

                    
            
def freqToAscendRatio(nestedDict):
    for word, freqDict in nestedDict.items():
        total = 0
        prev = 0
        for key in freqDict:
            total += freqDict[key]
        for key in freqDict:
            prev += freqDict[key]/total
            freqDict[key] = prev
    return(nestedDict)



def generateSentences(num, nestedDict):
    sentence = []
    word = '<START>'
    seed = random.random()
    finished = 'false'
    while word != '<END>':
        finished = 'false'
        for key, value in nestedDict[word].items():
            if value >= seed and finished == 'false':
                seed = random.random()
                if word != '<START>':
                    sentence.append(word)
                word = key
                finished = 'true'
    return ' '.join(sentence)


#PROGRAM START
#read in commandline args
sys.argv.pop(0) #get rid of "ngram.py" arg
gramNum = int(sys.argv.pop(0))
opSentenceNum = sys.argv.pop(0)
inputFiles = sys.argv
fullTexts = []


#reads full text of file into single str in list "fullTexts"
#therefore list "fullTexts" will have a single entry for each .txt file consisting of the entire text of that file
for files in inputFiles:
    with open(files, 'r+') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        fullTexts.append(' '.join(lines))


#calls stripSymbols() and splitToWords() for each body of text
#also puts to lower case
for book in range(len(fullTexts)):
    fullTexts[book] = stripSymbols(fullTexts[book].lower())
    fullTexts[book] = splitToSentences(fullTexts[book])
    fullTexts[book] = splitToWords(fullTexts[book])

#print(fullTexts)#TESTING


bigramTable = createNgramTable(fullTexts, gramNum)

#pretty(bigramTable['<START>'])
#pretty(bigramTable['white'])

print(generateSentences(opSentenceNum, bigramTable))