import spacy
import os
import csv

# Load domain expert annotations for comparison to noun phrase extraction algorithm

annotationPath = '/Users/verlynfischer/PycharmProjects/NPX/annotations.csv'
annotationDict = dict()

with open(annotationPath) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            annotationDict.update({row[0] : row[1]})
            line_count += 1

desired_dict = {k:v for (k,v) in annotationDict.items() if 'TRUE' in v}
notDesired_dict = {k:v for (k,v) in annotationDict.items() if 'FALSE' in v}

# Perform Noun Phrase Extraction

# rootdir = '/Users/verlynfischer/Documents/PythonPrograms/NPXData/English'
rootdir = 'clusterSnippets'
nlp = spacy.load('en_core_web_sm')

chunkList = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file != '.DS_Store':
            path = os.path.join(subdir, file)
            f = open(path, "r")
            contents = f.read()
            doc = nlp(contents)
            # print('===============================')
            # print(os.path.join(subdir, file))
            # print()

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

                lastToken = chunk[len(chunk)-1].text

                while nlp.vocab[lastToken].is_stop and len(chunk) > 1:
                    chunk = chunk[0:len(chunk)-1]
                    lastToken = chunk[len(chunk)-1].text

                if len(chunk) == 1:
                    keep = False

                for token in chunk:
                    if not token.is_alpha:
                        keep = False

                if chunk.text.isupper():
                    keep = False

                if keep:
                    chunkList.append(chunk.text)

            # List Named Entities
            # print(">>>>>>>>>>>>>>>>>>>>>>>>")
            # for ent in doc.ents:
            #     print(ent.text,":",ent.label_)

# Deduplicate list of NP
chunkList = list(dict.fromkeys(chunkList))

# Test against annotations

inDesired = []
inNotDesired = []
inNothing = []
missing = []

for testNP in chunkList:
    found = False
    if testNP in desired_dict.keys():
        inDesired.append(testNP)
        found = True
    if testNP in notDesired_dict.keys():
        inNotDesired.append(testNP)
        found = True
    if not found:
        inNothing.append(testNP)

for testNP in desired_dict.keys():
    if testNP not in chunkList:
        missing.append(testNP)

successes = len(inDesired)
failures = len(inNotDesired) + len(missing)
undetermined = len(inNothing)
successRate = successes / (successes + failures)

print('----------------')
print('SUMMARY')
print(f'Success: {successes}')
print(f'Failures: {failures}')
print(f'Undetermined: {undetermined}')
print(f'Success Rate: {successRate}')
print('----------------')
print('PRODUCED : ON EXPERT -DESIRED- LIST')
for npChunk in inDesired:
    print(npChunk)
print('----------------')
print('PRODUCED : ON EXPERT -NOT DESIRED- LIST')
for npChunk in inNotDesired:
    print(npChunk)
print('----------------')
print('PRODUCED : NOT ON EXPERT LIST')
for npChunk in inNothing:
    print(npChunk)
# print('----------------')
# print('NOT PRODUCED : ON EXPERT -DESIRED- LIST')
# for npChunk in missing:
#     print(npChunk)