import json
import sys
from random import randint


count = int(sys.argv[1])
fieldname = str(sys.argv[2])
randomstart = False


with open('data.json', 'r') as f:
    json_dict = json.load(f)

if randomstart:
    rand = randint(0, len(json_dict) - count)
else:
    rand = 0
for i in range(rand, rand+count):
    try:
        field = json_dict[i]['fields'][fieldname]
    except:
        print(f'{i} No value {fieldname}')
    print(f'{i} {fieldname}: {field}')