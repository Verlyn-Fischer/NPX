import spacy
import os


nlp = spacy.load('en_core_web_sm')

rootdir = '/Users/verlynfischer/Documents/PythonPrograms/NPXData/English'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        f = open(path, "r")
        contents = f.read()
        doc = nlp(contents)
        print('===============================')
        print(os.path.join(subdir, file))
        print()
        chunkList = []
        for chunk in doc.noun_chunks:
            # Use NP chunk if every token is alpha
            # Use NP chunk if token count is two or greater
            # Do not use chunk if first token is stop word and token count is two
            # Trim first word of chuck if it's a stop work and the chuck token count is three or more
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

            if keep:
                chunkList.append(chunk.text)
                # print(chunk.text)

        # Deduplicate list of NP

        chunkList = list(dict.fromkeys(chunkList))

        for npChunk in chunkList:
            print(npChunk)

        # # List Named Entities
        # print(">>>>>>>>>>>>>>>>>>>>>>>>")
        # for ent in doc.ents:
        #     print(ent.text,":",ent.label_)


