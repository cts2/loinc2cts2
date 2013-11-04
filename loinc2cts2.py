import json

import requests

from reader.loinc_csv_reader import LoincReader
from conversion import converter
from uri import uri_converter


client = requests.session()


def put_changeset(change_set):
    headers = {'content-type': 'application/json'}
    response = client.put('http://localhost:8080/cts2/changeset/%s' % change_set.get_uri(),
                          data=json.dumps(change_set.as_dict()), headers=headers)
    print response

hierarchy_reader = LoincReader("test/data/loinc-hierarchy.csv")

child_parent = {}

def hierarchy_row_callback(row):
    child = row['CODE'].replace('LP','')
    parent = row['IMMEDIATE_PARENT'].replace('LP','')
    if child not in child_parent:
        child_parent[child] = set()

    child_parent[child].add(parent)

hierarchy_reader.read(hierarchy_row_callback)


entity_reader = LoincReader("test/data/loinc.csv")

change_set = converter.create_changeset()

count = 0

def entity_row_callback(row):
    global count, change_set
    change_set.add_member(converter.row2entity(row, uri_converter.umls_uri, "LNC", "LNC-244", child_parent))
    count += 1
    if count > 1000:
        print "Putting changeset."
        put_changeset(change_set)
        count = 0
        change_set = converter.create_changeset()


entity_reader.read(entity_row_callback)

put_changeset(change_set)