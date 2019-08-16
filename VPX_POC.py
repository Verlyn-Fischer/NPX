import spacy
import os
from spacy.symbols import nsubj, VERB, dobj

# This extracts verb phrases from all of City of Houston matter and places results into a file
# format this can be imported into ElasticSearch

# Resource and Global Variables

nlp = spacy.load('en_core_web_sm')
fileCounter = 0

# Source
# source_directory = '/Users/verlynfischer/city_of_houston/ocrdata'
source_directory = 'source'

# Target
output_path = 'target/VPXResults/'



def extractPhrases(source_directory):
    global nlp

    verb_chunkList = []

    for dirpath, dirnames, filenames in os.walk(source_directory):

        for dir in dirnames:
            childPath = os.path.join(dirpath,dir)

            for nextPath, nextDir, nextFileName in os.walk(childPath):

                for file in nextFileName:
                    if file != '.DS_Store':

                        path = os.path.join(nextPath, file)
                        f = open(path, "r")
                        contents = f.read()
                        if len(contents) > 1000000:
                            contents = contents[:999998]
                        doc = nlp(contents)

                        for verb in [token for token in doc if token.pos == VERB]:
                            for child in verb.children:
                                if child.dep == dobj:

                                    # TO DO: remove phrases that are substrings of other phrases with a document
                                    # TO DO: Consider removing phrases where most words are not in vocabulary

                                    keep = True
                                    span = doc[min(child.left_edge.i, verb.i): max(child.right_edge.i + 1, verb.i)]
                                    output = span.text
                                    output = output.replace('\n',' ')
                                    output = output.replace('"', '')
                                    output = output.replace(')', '')
                                    output = output.replace('(', '')
                                    output = output.replace(']', '')
                                    output = output.replace('[', '')
                                    output = output.replace(',', '')
                                    output = output.replace(':', '')
                                    if len(output)>60:
                                        keep = False
                                    if output[:4] == 'Sent':
                                        keep = False
                                    if output.isupper():
                                        keep = False
                                    if keep:
                                        verb_chunkList.append([output,file,'Verb Phrase'])

    return verb_chunkList

def writeJSON(verb_phrases,output_path):

    print('Processing JSON')

    global fileCounter

    entryCounter = 0
    output_json = ''
    for vp in verb_phrases:
        output_json = output_json + '{ "index" : { "_index" : "verbphrases"} }\n'
        output_json = output_json + '{ "phrase" : "' + vp[0] + '" }\n'
        if entryCounter == 4000:
            fileName = output_path + 'output_phrases_' + str(fileCounter) + '.json'
            f = open(fileName,'w')
            f.write(output_json)
            f.close()
            fileCounter = fileCounter + 1
            entryCounter = 0
            output_json = ''
        entryCounter = entryCounter + 1

    fileName = output_path + 'output_phrases_' + str(fileCounter) + '.json'
    f = open(fileName, 'w')
    f.write(output_json)
    f.close()

def main():
    global source_directory
    global output_path

    phrases = extractPhrases(source_directory)
    writeJSON(phrases,output_path)


# main()