from requests import Request, Session
from requests.auth import HTTPBasicAuth
import json

def load_mapping(mapping_file_path):
    '''
    Load mapping file into script for joining with index creation request
    '''
    mapping_dict = {}
    try:
        with open(mapping_file_path,'r') as fp:
            mapping_dict = json.load(fp)
        return mapping_dict
    except IOError:
        print('mapping file not found')
        return None
def load_index_properties(index_properties_file_path):
    '''
    Load properties file into script for joining with index creation request
    '''
    index_properties_dict = {}
    try:
        with open(index_properties_file_path,'r') as fp:
            index_properties_dict = json.load(fp)
        return index_properties_dict
    except IOError:
        print('properties file not found')
        return None


def generate_index_create_request(url, mapping, index_properties):
    '''
    Generate request for creating index with desired properties
    '''
    props = lambda x: index_properties[x] if index_properties.get(x) else None
    headers = {}
    headers['content-type'] = 'application/json'
    headers['Accept'] = 'application/json'
    body = {}
    body["settings"] = {}
    if index_properties:
        if props("index"):
            body["settings"]["index"] = props("index")
        if props("analysis"):
            body["settings"]["analysis"] = props("analysis")
        if props("similarity"):
            body["settings"]["similarity"] = props("similarity")
    if mapping:
        body["mappings"] = mapping["mappings"]
    body = json.dumps(body)
    request = Request('PUT', url, data=body, headers=headers)
    return request



def create_index(endpoint,
                 index_name,
                 mapping_file_path,
                 index_properties_file_path):
    '''
    Create index in the at the given endpoint with the desired mapping and
    settings
    '''
    session = Session()
    session.auth = ('elastic', 'changeme')
    mapping = load_mapping(mapping_file_path)
    index_properties = load_index_properties(index_properties_file_path)
    url = '{}/{}?pretty'.format(endpoint, index_name)
    request = generate_index_create_request(url, mapping, index_properties)
    prepped = session.prepare_request(request)
    response = session.send(prepped)
    print(prepped.headers)
    if response:
        return (request, response)
    else:
        return (request, response)


def main():
    endpoint = 'http://localhost:9200'
    index_name = 'nutry_items'
    mapping_file = 'nutry_items_mapping.json'
    properties_file = 'nutry_items_properties.json'
    request, response = create_index(endpoint, index_name, mapping_file, properties_file)
    print('-----Request--------')
    print('Request url: {}'.format(request.url))
    print('Request headers:')
    print(request.headers)
    print('Reqest body:')
    print(json.dumps(
            json.loads(request.data),
            sort_keys=True,
            indent=4))
    print('-----Response--------')

    print('Response code: {}'.format(response.status_code))
    print('Response headers: ')
    print(response.headers)
    print('Response body:')
    print(response.text)

if __name__=='__main__':
    main()
