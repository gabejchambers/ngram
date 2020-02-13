#Gabe Chambers - V00774588
#cmsc 416 -- NLP
#Project 2: Ngram
#on own machine to run: 
# cd "C:\Users\gabej\OneDrive\Documents\vcu\2020\spring\416\Programming Projects\ngrams\ngram"; python ngram.py 3 10 texty.txt textfile.txt quran.txt
######################################################HEADER######################################################################
#
# 1) describe the problem to be solved well enough so that someone not familiar with our class could understand:
#
#   The goal of this program is to generate sentences based on a corpus as input.
#   In this context, a corpus is a large set of text, in the case of this project novels from gutenburg.org totaling
#   approximately 1,000,000 words was used.
#   In order to generate the output sentences, the program scans through the corpus and creates a table of N-grams.
#   An N-gram in this context is a set of n words from a given peice of text. 
#   For example if N were to be 3, all sequences of 2 consecutive words would be stored, along with the frequencies of 
#   the following 3rd word.
#   By the user providing a corpus, a value of N for the ngram, and a number of output sentences, the program will build
#   a table and then generate the output sentences by choosing one word at a time given the previously generated words
#   based on the relative frequency of that word. 
#   For example, in a trigram model, if a corpus had "cold dark" followed 3 times by "night", and once by "room",
#   there would be a 75% chance for night to be produced following "cold dark", and a 25% chance of "room". The
#   sentence ends when a punctuation is hit.
#
#
#   2)  give actual examples of program input and output, along with usage instructions
#
#   Instruction: run with command arguments: [ngram size] [number output sentences] [textfile1] [textfile2] ... [textfileN]
#
#   Ex:
#   input: python ngram.py 5 10 texty.txt textfile.txt quran.txt 
#   Where 5 is the ngram size, 10 is the number of sentences to be output, and the three textfiles are 
#   the full text of moby dick, the bible, and the quran.
#
#   output:
#   And for the unbelievers is a disgraceful chastisement.
#   Afterward he brought me to the gate even the gate that looketh toward the north where was the seat of the beast and upon them which worshipped his image.
#   Of the sons also of bigvai uthai and zabbud and with them seventy males.
#   But as for those who led the way the first of the muslims.
#   And the sons of lotan hori and homam and timna was lotans sister.
#   Ye have no other god that i know of but myself.
#   We appointed the kebla which thou formerly hadst only that we might know him who followeth the right guidance.
#   If thou return to the almighty thou shalt be built and to the temple thy foundation shall be laid.
#   Thus saith the lord god behold i will raise up unto them.
#   Benjamin shall ravin as a wolf in the morning he came again into the temple and when he had called the saints and widows presented her alive.
#
#  
#   3) describe the algorithm you have used to solve the problem, specified in a stepwise or point by point fashion:
#
#   Read in all commandline args and store in variables, with all text files being stored in a list.
#   Read full text of files into list as single strings per file.
#   Format text into all lowercase, and splitting each string into a list of tokens while stripping 
#   all non-punctuation symbols.
#   The rest is handled slightly differently if it is a unigram versus any other n-gram. I will  
#   explain general n-gram but unigram is almost identical.
#   A table is created in the form of a nested dictionary.
#   The outer keys are tuples containing preceeding word groups, where the start of sentences is 
#   buffered with '<START>' strings.
#   The values of these keys is another dictionary, where the key is any preceeding word to the
#   given phrase, and it's value is the number of times the word occurs after that phrase.
#   The dictionary is then converted from frequency to a ratio. The value of this ratio is 
#   the its frequency divided by the total number of occurances of words after the given ngram phrase.
#   This decimal is added to the value of the previous until all are summed, giving hte final value 1.0000
#   To illustrate with an example: "dark cold" occurs 4 times in the corpus. Once followed by "room", twice by "night",
#   and once by "presence". Below is what the dictionary would look like before and after converstion to ratio:
#   Before:
#   { ...
#       ("cold", "night") : {"room": 1
#                            "night": 2
#                            "presence": 1} 
#   ... } 
#
#   After:
#   { ...
#       ("cold", "night") : {"room": .250
#                            "night": .750
#                            "presence": 1.000} 
#   ... } 
#   Next, sentences are generated. A List is created to be populated with sentences.
#   Then a loop starts, which occurs the number of times as sentences which need to be generated.
#   In this loop, another loop checks the inner dictionary of the current ngram phrase, starting with 
#   All '<START>' tags. For the comparison, a random number between 0 and 1 is generated, and then the 
#   value of each word is compared against it in order. If a numbers value is greater than the random number,
#   it is added to the sentence, the ngram phrase is updated, and a new random number is selected.
#   When a punctuation is hit, the sentence is flagged as complete and it goes onto the new sentence
#   until all are complete. The sentences are then formatted with capitalization, and the individual words 
#   are stung together into a single string.
#   Each of these sentences is then printed as output, and the program ends.


import sys, re, os, json, random

#strip all symbols except [.?!]. also keeps alpha and spaces
def stripSymbols(text):
    text = re.sub(r'[^a-zA-Z\s.!?]', '', text)#DIGITS REMOVED, TO ADD INSERT \d INTO REGEX
    return text


#takes full input of full text of one manuscript and splits into sentences 
#with no space at the beginning, and punctuation at the end
def splitToSentences(text):
    sentences = re.split(r'([.!?])', text)
    sentences.pop() #removes trailing empty "sentnece"
    return pastePuncToSentence(sentences)


#takes a list of strings which is a sentence, followed by its punctuation, 
#and concats them so that it is a list of complete sentences
def pastePuncToSentence(sentences):
    phrases = []
    for index in range(len(sentences)):
        if re.search(r'^ +(.*?)$', sentences[index]) is not None:
            tokens = re.search(r'^ +(.*?)$', sentences[index])
            sentences[index] = tokens.group(1)
        if index % 2 != 0:
            sentence = [sentences[index-1] + sentences[index]]
            phrases.append(sentence)
    return phrases


#takes a list of strings and splits each into list of all word tokens
def splitToWords(sentences):
    for sentence in range(len(sentences)):
        sentences[sentence][0] = sentences[sentence][0].replace('.', ' .')
        sentences[sentence][0] = sentences[sentence][0].replace('?', ' ?')
        sentences[sentence][0] = sentences[sentence][0].replace('!', ' !')
        sentences[sentence] = re.split(r'\s', sentences[sentence][0])
    return sentences


#prints a readable version of the nested dictionary
def pretty(nestedDict):
   print(json.dumps(nestedDict, sort_keys=True, indent=8))


def createUnigramTable(fullTexts, N):
    uniDict = {}
    for book in fullTexts:
        for sentence in book:
            if len(sentence) >= N:
                for word in sentence:
                    if word in uniDict:
                        uniDict[word] += 1
                    else:
                        uniDict[word] = 1
    return uniDict


#creates the Ngram frequency table, implimentation is a nested dictionary
def createNgramTable(fullTexts, N):
    prev = getInitiatedTuple(N)
    START = list(prev)
    bigramTable = {prev: {}}

    for book in fullTexts:
        for sentence in book:
            if len(sentence) >= N: #break if the sentence is shorter than the specified Ngram size
                for word in sentence:  
                    #add occurance bigram table
                    if prev in bigramTable:
                        if word in bigramTable[prev]:
                            bigramTable[prev][word] += 1
                        else:
                            bigramTable[prev][word] = 1
                    else:
                        bigramTable[prev] = {word: 1}
                    #modify tracker of previous tokens ie the key in outer dictionary
                    prev = updateNgramTuple(prev, word)
                    #print(prev)
                    #tacks on '<END>' if reach punctuation
                    if prev[-1] == '.' or prev[-1] == '!' or prev[-1] == '?':
                        word = '<END>'
                        if prev in bigramTable:
                            if word in bigramTable[prev]:
                                bigramTable[prev][word] += 1
                            else:
                                bigramTable[prev][word] = 1
                        else:
                            bigramTable[prev] = {word: 1}
                        prev = tuple(START)
    #pretty(bigramTable)
    #pretty(bigramTable[('he', 'said', 'who')])
    #print(bigramTable[('see',)])
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
    #pretty(nestedDict[('<START>',)])
    return(nestedDict)


def uniFreqToRatio(uniTable):
    total = 0
    prev = 0
    for word, freq in uniTable.items():
        total += freq
    for word, freq in uniTable.items():
        prev += freq/total
        uniTable[word] = prev
    return uniTable
        

def getInitiatedTuple(N):
    START = []
    for index in range(N-1):
        START.append('<START>')
    return tuple(START)


def updateNgramTuple(ngramTuple, newWord):
    moveLeftWord = ''
    insertWord = newWord
    ngramList = list(ngramTuple)
    for index in range(len(ngramList)-1, -1, -1):
        moveLeftWord = ngramList[index]
        ngramList[index] = insertWord
        insertWord = moveLeftWord
    ngramTuple = tuple(ngramList)
    return ngramTuple


def generateSentences(numOpSentences, nestedDict, N):
    sentence = []
    ngramPrev = getInitiatedTuple(N)
    seed = random.random()
    finished = 'false'
    sentenceCount = 0
    while sentenceCount < numOpSentences: 
        finished = 'false'
        for key, value in nestedDict[ngramPrev].items():
            if value >= seed and finished == 'false':
                #print(value)
                #print(seed)
                seed = random.random()
                if ngramPrev != getInitiatedTuple(N):
                    sentence.append(ngramPrev[-1])
                #print(ngramPrev)
                #pretty(nestedDict[ngramPrev])
                ngramPrev = updateNgramTuple(ngramPrev, key)

                finished = 'true'
                if ngramPrev[-1] == '<END>':
                    ngramPrev = getInitiatedTuple(N)
                    sentenceCount += 1
    paragraph = ' '.join(sentence)
    #correctly format punctuation
    paragraph = paragraph.replace(' .', '.')
    paragraph = paragraph.replace(' !', '!')
    paragraph = paragraph.replace(' ?', '?')
    #split long text into seperate sentences to allow seperate line printing
    sentences = re.split('([.!?])', paragraph)
    sentences = pastePuncToSentence(sentences)
    #capatalize sentence
    for index in range(len(sentences)):
        for subindex in range(len(sentences[index])):
            sentences[index][subindex] = capFirstLetter(sentences[index][subindex])
    return sentences


def uniGenerateSentences(numOpSentences, uniTable):
    sentences = []
    sentence = []
    seed = random.random()
    word = ''
    finished = 'false'
    sentenceCount = 0
    while sentenceCount < numOpSentences:
        finished = 'false'
        for word, ratio in uniTable.items():
            if ratio >= seed and finished == 'false':
                seed = random.random()
                sentence.append(word)
                if word == '.' or word == '!' or word == '?':
                    finished = 'true'
                    sentenceCount += 1
                    sentences.append(sentence)
                    sentence = []
    for index in range(len(sentences)):
        sentences[index] = ' '.join(sentences[index])
        sentences[index] = sentences[index].replace(' .', '.')
        sentences[index] = sentences[index].replace(' !', '!')
        sentences[index] = sentences[index].replace(' ?', '?')
        sentences[index] = capFirstLetter(sentences[index])
    return sentences



#capatalizes first letter of a string and returns new string
def capFirstLetter(sentence):
    return sentence[:1].upper() + sentence[1:]




#PROGRAM START
#read in commandline args
sys.argv.pop(0) #get rid of "ngram.py" arg
gramNum = int(sys.argv.pop(0))
opSentenceNum = int(sys.argv.pop(0))
inputFiles = sys.argv
fullTexts = []

#print statements:
print('author: Gabe Chambers - V00774588')
print('This program generates sentences based on input via an ngram model.')
print('command line args: ngram.py', ' ', str(gramNum), ' ', str(opSentenceNum))


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


if gramNum == 1:
    uniTable = createUnigramTable(fullTexts, gramNum)
    uniTable = uniFreqToRatio(uniTable)
    sentences = uniGenerateSentences(opSentenceNum, uniTable)
    for sentence in sentences:
        print(sentence)
else:
    bigramTable = createNgramTable(fullTexts, gramNum)
    #pretty(bigramTable['<START>'])
    #pretty(bigramTable['!'])
    opSentences = generateSentences(opSentenceNum, bigramTable, gramNum)
    for sentence in opSentences:
        for text in sentence:
            print(text)