#Gabe Chambers - V00774588
#cmsc 416 -- NLP
#Project 2: Ngram
#to run: 
# cd "C:\Users\gabej\OneDrive\Documents\vcu\2020\spring\416\Programming Projects\ngrams\ngram"; python ngram.py 3 10 texty.txt textfile.txt

#Note: thinking that tables should be in structure: myTable = {'dark': {'night':3,'storm':2}, 'storm': {'night':0,'dark':5}, 'night': {'sorm':8,'dark':0}}
# https://www.w3schools.com/python/python_dictionaries.asp
# https://www.programiz.com/python-programming/nested-dictionary

import sys, re, os


#strip all symbols except [.?!]. also keeps alphanumeric and spaces
def stripSymbols(text):
    text = re.sub(r'[^a-zA-Z\d\s.!?]', '', text)
    return text


def splitToWords(text):
    text = text.replace('.', ' .')
    text = text.replace('?', ' ?')
    text = text.replace('!', ' !')
    return re.split(r'\s', text)



#PROGRAM START
#read in commandline args
sys.argv.pop(0) #get rid of "ngram.py" arg
gramNum = sys.argv.pop(0)
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
    fullTexts[book] = splitToWords(fullTexts[book])



print(fullTexts)


