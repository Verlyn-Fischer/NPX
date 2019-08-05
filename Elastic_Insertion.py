import requests
import os

source_directory = '/Users/verlynfischer/NPXResults'

headers = {
    'Content-Type': 'application/x-ndjson',
}

data = """
{ "index" : { "_index" : "k2"} }
{ "phrase" : "public officals" }
{ "index" : { "_index" : "k2"} }
{ "phrase" : "Dear Mr Bohrer" }
"""
response = requests.post('http://10.10.138.98:9200/k2/_bulk?pretty', headers=headers, data=data)
print(response)

# for dirpath, dirnames, filenames in os.walk(source_directory):
#     for file in filenames:
#         if file != '.DS_Store':
#             filePath = os.path.join(dirpath,file)
#             data = open(filePath, 'rb').read()
#             response = requests.post('http://10.10.138.98:9200/_bulk', headers=headers, data=data)
#             # 'http://10.10.138.98:5601'

