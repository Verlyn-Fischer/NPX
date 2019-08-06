import requests
import os

# This serves to push data into ElasticSearch on Verlyn's machine or on a remote instance.
source_directory = '/Users/verlynfischer/NPXResults'
source_directory_remote = '/Users/verlynfischer/NPXResultsUpdated'

headers = {
    'Content-Type': 'application/x-ndjson',
}

def postToLocal():
    for dirpath, dirnames, filenames in os.walk(source_directory):
        for file in filenames:
            if file != '.DS_Store':
                filePath = os.path.join(dirpath,file)
                data = open(filePath, 'rb').read()
                response = requests.post('http://10.10.138.98:9200/_bulk', headers=headers, data=data)
                # 'http://10.10.138.98:5601'

def postToRemote():
    for dirpath, dirnames, filenames in os.walk(source_directory_remote):
        for file in filenames:
            if file != '.DS_Store':
                filePath = os.path.join(dirpath,file)
                data = open(filePath, 'rb').read()
                response = requests.post('http://10.10.138.98:9200/_bulk', headers=headers, data=data)
                print(response)

def main():
    # postToLocal()
    postToRemote()

# main()
