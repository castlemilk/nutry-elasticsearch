import json

original = {}
with open('food_list_total.json','r') as fp:
    original = json.load(fp)

flat = {}
for item, item_info in original.iteritems():
    flat['ID'] = str(item)
    flat['name'] = str(item_info['name'])
    flat['source'] = str(item_info['source'])
    flat['group'] = str(item_info['group'])
    print json.dumps(flat)

