#Gabe Chambers - V00774588
#cmsc 416 -- NLP
#Project 2: Ngram
#to run: 
# cd "C:\Users\gabej\OneDrive\Documents\vcu\2020\spring\416\Programming Projects\ngrams\ngram"; python ngram.py 3 10 texty.txt textfile.txt

import sys, re, os


#strip all symbols except [.?!]. also keeps alphanumeric and spaces
def stripSymbols(text):
    text = re.sub(r'[^a-zA-Z\d\s.!?]', '', text)
    return text


#splits str into sentences, returns list of sentences
def splitToSentences(text):
    sentences = re.split(r'[.!?]', text)
    sentences.pop() #removes trailing empty "sentnece"
    for index in range(len(sentences)):
        if re.search(r'^ (.*?)$', sentences[index]) is not None:
            tokens = re.search(r'^ (.*?)$', sentences[index])
            sentences[index] = tokens.group(1)
    return sentences




#read in commandline args
sys.argv.pop(0) #get rid of "ngram.py" arg
gramNum = sys.argv.pop(0)
opSentences = sys.argv.pop(0)
inputFiles = sys.argv
fileText = []

#reads full text of file into single str in list "fileText"
#therefore list "fileText" will have a single entry for each .txt file consisting of the entire text of that file
for files in inputFiles:
    with open(files, 'r+') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        fileText.append(' '.join(lines))

#calls stripSymbols() for each text
for index in range(len(fileText)):
    fileText[index] = stripSymbols(fileText[index])

for index in range(len(fileText)):
    fileText[index] = splitToSentences(fileText[index])

print(fileText)


