import spacy
import os
import csv


nlp = spacy.load('en_core_web_sm')

annotationPath = '/Users/verlynfischer/Desktop/annotations.csv'
annotationDict = dict()

with open(annotationPath) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            annotationDict.update({row[0] : row[1]})
            #print(f'\t{row[0]} \t {row[1]} \t {row[2]}')
            line_count += 1
    #print(f'Processed {line_count} lines.')

rootdir = '/Users/verlynfischer/Documents/PythonPrograms/NPXData/English'

chunkList = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        f = open(path, "r")
        contents = f.read()
        doc = nlp(contents)
        print('===============================')
        print(os.path.join(subdir, file))
        print()

        for chunk in doc.noun_chunks:
            # Use NP chunk if every token is alpha
            # Use NP chunk if token count is two or greater
            # Do not use chunk if first token is stop word and token count is two
            # Trim first and second word of chunk if it's a stop work and the chuck token count is three or more
            # Discard strings entirely in upper case
            keep = True

            if len(chunk) == 1:
                keep = False

            for token in chunk:
                if not token.is_alpha:
                    keep = False

            firstToken = chunk[0].text

            if nlp.vocab[firstToken].is_stop and len(chunk) == 2:
                keep = False

            if nlp.vocab[firstToken].is_stop and len(chunk) > 2:
                chunk = chunk[1:len(chunk)]

            firstToken = chunk[0].text

            if nlp.vocab[firstToken].is_stop and len(chunk) > 2:
                chunk = chunk[1:len(chunk)]

            if chunk.text.isupper():
                keep = False

            if keep:
                chunkList.append(chunk.text)
                # print(chunk.text)

        # List Named Entities
        # print(">>>>>>>>>>>>>>>>>>>>>>>>")
        # for ent in doc.ents:
        #     print(ent.text,":",ent.label_)

# Deduplicate list of NP
chunkList = list(dict.fromkeys(chunkList))

# Test against annotations
# TBD

# Present results

for npChunk in chunkList:
    print(npChunk)

