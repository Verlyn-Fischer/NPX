import spacy
import os
import csv
from spacy import displacy
from spacy.symbols import nsubj, VERB, dobj

source_directory = '/Users/verlynfischer/COH_interesting'
output_file = '/Users/verlynfischer/VerbResults/verb_phrase_results.csv'
vis_file = '/Users/verlynfischer/Desktop/exampleRender.html'

nlp = spacy.load('en_core_web_sm')

fileCounter = 0

def extractPhrases(source_directory):
    global nlp

    noun_chunkList = []
    verb_chunkList = []


    for dirpath, dirnames, filenames in os.walk(source_directory):

        for file in filenames:
            if file != '.DS_Store':

                path = os.path.join(dirpath, file)
                f = open(path, "r")
                contents = f.read()
                if len(contents) > 1000000:
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
                        noun_chunkList.append([chunk.text,file,'Noun Phrase'])

                for verb in [token for token in doc if token.pos == VERB]:
                    for child in verb.children:
                        if child.dep == dobj:
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
                            if output[:4] == 'Sent':
                                keep = False
                            if output.isupper():
                                keep = False
                            if keep:
                                verb_chunkList.append([output,file,'Verb Phrase'])



        # Deduplicate list of NP within a file
        # noun_chunkList = list(dict.fromkeys(noun_chunkList))

    return noun_chunkList, verb_chunkList

def writeResults(noun_phrases,verb_phrases,output_file):

    with open(output_file,'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(noun_phrases)
        csv_writer.writerows(verb_phrases)

def visualizeParseTree(vis_file):
    doc = nlp(u"I then called the 24:7 tech number a bit ago and spoke with a guy named Herman. He said he tried to\
    call Jerry and left him voice mails on multiple phone numbers.")

    # doc = nlp(u'When we encounter patients in crisis we evaluate and transfer to psychiatric facilities.\
    # I think it would be helpful for us to have a meeting to better understand the scope of the\
    # problem and the current processes in places.')

    html = displacy.render(doc,style="dep")

    with open(vis_file, 'w') as f:
        f.write(html)

    # for token in doc:
    #     print(token.text, token.dep_, token.head.text, token.head.pos_,
    #           [child for child in token.children])


    # Find all roots that are VERBS
    # Find children of these that are connected as dobj
    # Find all children of these regardless of type
    # Get the span between the leftmost and rightmost token

    for verb in [token for token in doc if token.pos == VERB]:
        print('------ New Sentence ------ ')
        print(verb)
        print('Index: ', str(verb.i))
        for child in verb.children:
            if child.dep == dobj:
                span = doc[min(child.left_edge.i,verb.i): max(child.right_edge.i + 1,verb.i)]
                print(span)

    # span = doc[doc[6].left_edge.i: doc[6].right_edge.i + 1]
    # print(span)

    # # Finding a verb with a subject from below — good
    # verbs = set()
    # for possible_subject in doc:
    #     if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
    #         verbs.add(possible_subject.head)
    # print(verbs)

def main():
    global output_file
    global vis_file

    # Get list of noun phrases
    noun_phrases, verb_phrases = extractPhrases(source_directory)

    # Write results to a file
    writeResults(noun_phrases,verb_phrases,output_file)

    # visualizeParseTree(vis_file)

main()