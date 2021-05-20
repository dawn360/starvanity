from handler import handler
import json

with open('event.json') as f:
    data = json.load(f)
    print(handler(data,None))
