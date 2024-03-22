import re

f = open('x.txt', 'r')
data = f.read()
f.close()
from pprint import pprint
pattern = r'\{\s*"444383007"\s*:.+?\}'

matches = re.findall(pattern, data)
import json
ct = 0
urls = []
for match in matches:
    
# print(match)

    pattern = r'http[^ ^"]+'

    try:
        urls.append(re.findall(pattern, match)[1])
    except:
        pass

pprint((urls))