import gspread
from pydrive.auth import GoogleAuth
from oauth2client.service_account import ServiceAccountCredentials
from rdflib import ConjunctiveGraph


def __get_class_name(temp_uri):
    return temp_uri.replace("http://schema.org/","")


def __add_property(props_dic, prop_desc):
    sdo_uri="http://schema.org/"
    if prop_desc['prop_name'] in props_dic:
        t_prop_name = prop_desc['prop_name']
        props_dic[t_prop_name]['exp_type'].append(prop_desc['exp_type'].replace(sdo_uri,""))
    else:
        props_dic[prop_desc['prop_name']]=prop_desc
        props_dic[prop_desc['prop_name']]['exp_type'] = [prop_desc['exp_type'].replace(sdo_uri,"")]
    return props_dic


def __get_class_props(class_name, graph):
    print("Quering properties of  %s in Schema.org" % class_name)

    qres = graph.query("""prefix schema: <http://schema.org/>
                        select distinct * where { 
                            ?property schema:domainIncludes  schema:%s .
                            ?property schema:rangeIncludes  ?exp_type .
                            ?property rdfs:label ?prop_name.
                            ?property rdfs:comment ?description
                        }""" % class_name)
    temp_dic = {}

    for row in qres:
        labels=row.labels.keys()
        labels_dic = {}
        print('Parsing %s property.' % row['prop_name'])
        for label in labels:
            labels_dic[label] = str(row[label])
        temp_dic=__add_property(temp_dic, labels_dic)

    return temp_dic


def __get_parent_type(class_name, graph):

    print("Find parent type of %s in Schema.org" % class_name)

    qres = graph.query("""prefix schema: <http://schema.org/>
                          select ?supclass where{
                          ?class rdfs:label ?label .
                          ?class rdfs:subClassOf ?supclass .
                          filter (?label='%s')
                        }""" % class_name)
    resp_arr=[]

    for row in qres:
        resp_arr.append(str(row['supclass']))
    return resp_arr[0].replace('http://schema.org/', '')


def __get_properties(class_name, graph, properties):

    if(class_name=='Thing'):
        properties[class_name]=__get_class_props(class_name, graph)
        return properties
    else:
        temp_props = __get_class_props(class_name, graph)
        properties[class_name] = temp_props
        parent_type = __get_parent_type(class_name, graph)
        __get_properties(parent_type, graph, properties)


def get_properties_in_hierarchy(type_name):
    query_type = type_name
    g = ConjunctiveGraph()
    g.parse('http://schema.org/version/latest/schema.jsonld', format='json-ld')
    props_dic={}
    __get_properties(query_type, g, props_dic)
    return props_dic


def get_hierarchy(props_dic):
    type_hierarchy = []
    for h_type in props_dic:
        type_hierarchy.append(h_type)
    return type_hierarchy


# Function that receives an string with expected types and generates an array with each expected pype
def get_expected_type(expected_types):

    expected_types = expected_types.strip()
    expected_types = expected_types.replace('\n', '')
    expected_types = expected_types.replace(' OR ', ' or ')
    list_of_types = expected_types.split(' or ')
    i = 0
    for type in list_of_types:
        list_of_types[i] = type.strip()
        i += 1

    return list_of_types


def _parse_controlled_vocabulary(temp_cont_vocab):
    cv_parsed = {'terms':[] , 'ontologies':[]}
    element_list = temp_cont_vocab.split(',')
    for element in element_list:
        if ':' in element:
            temp_onto = element.split(":",1)
            ontology = {}
            ontology['name'] = temp_onto[0].strip()
            ontology['url'] = temp_onto[1].strip()
            cv_parsed['ontologies'].append(ontology)
        elif element != '':
            cv_parsed['terms'].append(element)
    return cv_parsed


def __get_dic_from_sheet_row(c_property):

    property_as_dic = {}

    # Set Bioschemas attributes

    property_as_dic['bsc_dec'] = c_property['BSC Description'].strip().replace('\n', ' ')
    property_as_dic['marginality'] = c_property['Marginality'].replace('\n', ' ')
    property_as_dic['cardinality'] = c_property['Cardinality'].strip().strip('\n').replace('\n', ' ')
    temp_cont_vocab = c_property['Controlled Vocabulary'].strip().replace('\n', ' ')
    property_as_dic['controlled_vocab'] = _parse_controlled_vocabulary(temp_cont_vocab)


    # Set schema.org attributes

    property_as_dic['name'] = c_property['Property'].strip().strip('\n')
    property_as_dic['expected_type'] = get_expected_type(c_property['Expected Type'])
    property_as_dic['sdo_desc'] = c_property['Description'].strip().replace('\n', ' ')

    return property_as_dic
def get_property_in_hierarchy(sdo_props, mapping_property):
    prop_type="new_sdo"
    for hierarchy_level in sdo_props:
        if mapping_property['name'] in sdo_props[hierarchy_level].keys():
            prop_type = hierarchy_level
            mapping_property['sdo_desc']=sdo_props[hierarchy_level][mapping_property['name']]['description']
    return {'type':prop_type, 'property': mapping_property}

def get_formatted_props(sdo_props, mapping_props):
    formatted_props = {}
    new_props = []
    extd_props = {}
    for mapping_property in mapping_props:
        temp_prop=get_property_in_hierarchy(sdo_props, mapping_property)
        if temp_prop['type'] == "new_sdo":
            new_props.append(temp_prop['property'])
        else:
            prop_type = temp_prop['type']
            if prop_type in extd_props.keys():
                extd_props[prop_type].append(temp_prop['property'])
            else:
                extd_props[prop_type]=[temp_prop['property']]

    formatted_props['new_props']=new_props
    formatted_props['extended_props']=extd_props

    return formatted_props


def get_mapping_properties(mapping_sheet):
    list_of_hashes = mapping_sheet.get_all_records(head=5)
    type_properties = []
    for c_property in list_of_hashes:
        if(c_property['Expected Type']!="" and c_property['Description']!=""
           and c_property['Marginality']!="" and c_property['Cardinality']!=""):
            print("Parsing %s property from Google Sheets." % c_property['Property'])
            property_as_dic=__get_dic_from_sheet_row(c_property)
            type_properties.append(property_as_dic)
    return type_properties


class GSheetsParser:
    gsheet_id = ''
    cred_file = ''
    gauth = "This variable will have the Google Authorization file"
    scope = []
    spec_metadata={}
    bsc_specification = {}

    def __init__(self):
        self.gsheet_id = '1h0-fgqnRe25-tVCmu2yWNQjthLzgkW4a1TVNMpCABlc'
        #self.cred_file = 'client_secrets.json'
        #self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.spec_metadata={}
        self.bsc_specification = {}
        creds_path="spec2model/mycreds.txt"
        self.gauth = GoogleAuth()
        # Try to load saved client credentials
        self.gauth.LoadCredentialsFile(creds_path)
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
            # Save the current credentials to a file
            self.gauth.SaveCredentialsFile(creds_path)

    def set_gsheet_id(self, gsheet_id):
        self.gsheet_id = gsheet_id

    def set_spec_metadata(self, spec_metadata):
        self.spec_metadata=spec_metadata

    def __get_mapping_description(self, mapping_sheet):
        mapping_description = {}
        mapping_description['name']=self.spec_metadata['name']
        print("Parsing %s Google Sheet" % mapping_description['name'])
        mapping_description['g_mapping_file']=self.spec_metadata['g_mapping_file']
        mapping_description['spec_mapping_url']=self.spec_metadata['spec_mapping_url']
        mapping_description['status']=self.spec_metadata['status']
        mapping_description['spec_type']=self.spec_metadata['spec_type']
        mapping_description['gh_folder']='https://github.com/BioSchemas/Specifications/'+self.spec_metadata['name']
        mapping_description['gh_examples']=mapping_description['gh_folder']+'/Examples'
        mapping_description['gh_tasks']='https://github.com/BioSchemas/bioschemas/labels/type%3A%20'+self.spec_metadata['name']
        mapping_description['edit_url']='https://github.com/BioSchemas/bioschemas.github.io/edit/master/_newSpecs/'+self.spec_metadata['name']+'.md'
        mapping_description['use_cases_url']=self.spec_metadata['use_cases_url']
        mapping_description['version']=self.spec_metadata['version']
        mapping_description['subtitle'] = mapping_sheet.acell('B1').value
        mapping_description['description'] = mapping_sheet.acell('B2').value
        mapping_description['parent_type'] = mapping_sheet.acell('A6').value[8:].strip()
        return mapping_description

    def get_mapping_g_sheets(self):

        #creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_file, self.scope)

        client = gspread.authorize(self.gauth.credentials)

        #client = gspread.authorize(creds)
        print("Parsing %s file." % self.spec_metadata['g_mapping_file'])
        mapping_sheet = client.open_by_key(self.gsheet_id).get_worksheet(0)

        spec_description = self.__get_mapping_description(mapping_sheet)
        sdo_props = get_properties_in_hierarchy(spec_description['parent_type'])

        spec_description ['hierarchy']= get_hierarchy(sdo_props)
        print("Prepared schema.org properties for hierarchy %s" % str(spec_description ['hierarchy']))

        print("Classifing %s properties" % spec_description['name'])
        mapping_props = get_mapping_properties(mapping_sheet)


        formatted_props = get_formatted_props(sdo_props, mapping_props)

        spec_description.update(formatted_props)

        return spec_description
