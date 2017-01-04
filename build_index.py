from requests import Request, Session
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
    request = Request('POST', url, data=body, headers=headers)
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
    mapping = load_mapping(mapping_file_path)
    index_properties = load_index_properties(index_properties_file_path)
    url = '{}/{}?pretty'.format(endpoint, index_name)
    request = generate_index_create_request(url, mapping, index_properties)
    request_prepared = request.prepare()
    #response = session.send(request_prepared)
    response = None
    if response:
        return response
    else:
        return request


def main():
    endpoint = 'http://localhost:9200'
    index_name = 'nutry_items'
    mapping_file = 'nutry_items_mapping.json.props'
    properties_file = 'nutry_items_properties.json.props'
    resp = create_index(endpoint, index_name, mapping_file, properties_file)
    if isinstance(resp, Request):
        print('-----Request--------')
        print('Request url: {}'.format(resp.url))
        print('Reqest body:')
        print(json.dumps(
            json.loads(resp.data),
            sort_keys=True,
            indent=4))
    else:
        print('-----Response--------')
        print('Response code: {}'.format(resp.status_code))
        print('Response body:\n{}'.format(resp.text))


if __name__=='__main__':
    main()
