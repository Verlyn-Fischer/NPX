# In order to load noun phrases into Elastic on new instance,
# it's necessary to convert the file to be compatible with the version of Elastic
# on the instance.

import os
import json

source_directory = '/Users/verlynfischer/NPXResults'
target_directory = '/Users/verlynfischer/NPXResultsUpdated'



for dirpath, dirnames, filenames in os.walk(source_directory):
    for file in filenames:
        if file != '.DS_Store':
            filePath = os.path.join(dirpath, file)
            data = open(filePath, 'r').readlines()
            dataOut = ''
            myJson = {}
            newFileContent = []
            fileString = ''
            for dataLine in data:
                myJson = json.loads(dataLine)
                if 'create' in myJson.keys():
                    myJson['index']=myJson['create']
                    del myJson['create']
                    value = myJson['index']
                    del value['_type']
                jsonString = str(myJson)
                jsonString = jsonString.replace('\'','\"')
                newFileContent.append(jsonString)
            for contentItem in newFileContent:
                fileString = fileString + contentItem + '\n'
            NewfilePath = os.path.join(target_directory, file)
            open(NewfilePath, 'w').writelines(fileString)
