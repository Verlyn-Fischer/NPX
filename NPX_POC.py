import spacy
import os
import json

source_directory = '/Users/verlynfischer/partial_city_of_houston'
output_file = '/Users/verlynfischer/NPXResults/city_of_houston_results.json'

nlp = spacy.load('en_core_web_sm')

def extractNP(source_directory):
    global nlp

    global_chunkList = []

    for subdir, dirs, files in os.walk(source_directory):
        for file in files:
            if file != '.DS_Store':

                local_chunkList = []

                path = os.path.join(subdir, file)
                f = open(path, "r")
                contents = f.read()
                doc = nlp(contents)

                for chunk in doc.noun_chunks:
                    # Trim leading stop words (including a few I added)
                    # Trim trailing stop words (including a few I added)
                    # Use NP chunk if every token is alpha
                    # Use NP chunk if token count is two or greater
                    # Discard strings entirely in upper case

                    keep = True

                    firstToken = chunk[0].text

                    while nlp.vocab[firstToken].is_stop and len(chunk) > 1:
                        chunk = chunk[1:len(chunk)]
                        firstToken = chunk[0].text

                    lastToken = chunk[len(chunk) - 1].text

                    while nlp.vocab[lastToken].is_stop and len(chunk) > 1:
                        chunk = chunk[0:len(chunk) - 1]
                        lastToken = chunk[len(chunk) - 1].text

                    if len(chunk) == 1:
                        keep = False

                    for token in chunk:
                        if not token.is_alpha:
                            keep = False

                    if chunk.text.isupper():
                        keep = False

                    if keep:
                        local_chunkList.append(chunk.text)

                # Deduplicate list of NP within a file
                local_chunkList = list(dict.fromkeys(local_chunkList))

        # Add entries from file to global list
        global_chunkList.extend(local_chunkList)

        return global_chunkList

def writeResults(noun_phrases,output_file):
    with open(output_file, 'w') as f:
        for item in noun_phrases:
            f.write("%s\n" % item)

def writeJSON(noun_phrases,output_file):

    output_json = ''
    for np in noun_phrases:
        output_json = output_json + '{ "create" : { "_index" : "phrases", "_type" : "phrase" } }\n'
        output_json = output_json + '{ "phrase" : "' + np + '" }\n'

    f = open(output_file,'w')
    f.write(output_json)
    f.close()

def main():
    # Get list of noun phrases
    noun_phrases = extractNP(source_directory)

    # Write results to a file
    # writeResults(noun_phrases,output_file)

    # Write results to a JSON
    writeJSON(noun_phrases,output_file)


main()

