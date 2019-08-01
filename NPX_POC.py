import spacy
import os

source_directory = '/Users/verlynfischer/city_of_houston/ocrdata'
# source_directory = '/Users/verlynfischer/partial_city_of_houston/ocrdata'
output_file = '/Users/verlynfischer/NPXResults/city_of_houston_results.csv'
output_path = '/Users/verlynfischer/NPXResults/'

nlp = spacy.load('en_core_web_sm')

fileCounter = 0

def extractNP(source_directory,output_path):
    global nlp

    global_chunkList = []
    local_chunkList = []

    docCount = 0

    for dirpath, dirnames, filenames in os.walk(source_directory):

        for dir in dirnames:
            childPath = os.path.join(dirpath,dir)

            for nextPath, nextDir, nextFileName in os.walk(childPath):

                for file in nextFileName:
                    if file != '.DS_Store':

                        local_chunkList = []

                        path = os.path.join(nextPath, file)
                        f = open(path, "r")
                        contents = f.read()
                        if len(contents)>1000000:
                            contents = contents[:999998]
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

                        if docCount % 50 == 0:
                            print('Documents processed by NLP so far: ' + str(docCount))
                            writeJSON(global_chunkList, output_file)
                            global_chunkList = []

                        docCount = docCount + 1

    print('Total documents process by NLP: ' + str(docCount))
    writeJSON(global_chunkList, output_file)
    return global_chunkList

def writeResults(noun_phrases,output_file):
    with open(output_file, 'w') as f:
        for item in noun_phrases:
            f.write("%s\n" % item)

def writeJSON(noun_phrases,output_path):

    print('Processing JSON')

    global fileCounter

    entryCounter = 0
    output_json = ''
    for np in noun_phrases:
        output_json = output_json + '{ "create" : { "_index" : "phrases", "_type" : "phrase" } }\n'
        output_json = output_json + '{ "phrase" : "' + np + '" }\n'
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
    # Get list of noun phrases
    noun_phrases = extractNP(source_directory,output_path)

    # Write results to a file
    # writeResults(noun_phrases,output_file)

    # Write results to a JSON
    # writeJSON(noun_phrases,output_path)


# main()

