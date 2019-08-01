import requests
import os

source_directory = '/Users/verlynfischer/NPXResults'

headers = {
    'Content-Type': 'application/x-ndjson',
}

for dirpath, dirnames, filenames in os.walk(source_directory):
    for file in filenames:
        if file != '.DS_Store':
            filePath = os.path.join(dirpath,file)
            data = open(filePath, 'rb').read()
            response = requests.post('http://localhost:9200/_bulk', headers=headers, data=data)

