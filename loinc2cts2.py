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


change_set = converter.create_changeset()

reader = LoincReader("test/loinc.csv")


def row_callback(row):
    change_set.add_member(converter.row2entity(row, uri_converter.umls_uri, "LNC", "LNC-244"))


reader.read(row_callback)

#put_changeset(change_set)