import uuid

from cts2_types import *
from uri import uri_converter


def row2entity(row, code_system, code_system_version, child_parent):
    not_properties = ['LOINC_NUM','COMPONENT','SHORTNAME','LONG_COMMON_NAME', 'STATUS', 'COMMENTS',
    'EXMPL_ANSWERS', 'EXAMPLE_UNITS', 'EXAMPLE_UCUM_UNITS', 'EXAMPLE_SI_UCUM_UNITS']

    name = row['LOINC_NUM']
    description = row['COMPONENT']
    short_name = row['SHORTNAME']
    long_common_name = row['LONG_COMMON_NAME']
    status = row['STATUS']
    comments = row['COMMENTS']
    example_answers = row['EXMPL_ANSWERS']
    example_units = row['EXAMPLE_UNITS']
    example_ucum_units = row['EXAMPLE_UCUM_UNITS']
    example_si_ucum_units = row['EXAMPLE_SI_UCUM_UNITS']
    copyright = row['EXTERNAL_COPYRIGHT_NOTICE']

    entity = Entity(name=name, namespace=code_system, about=uri_converter.umls_entity_uri(code_system, name),
                  code_system=code_system, code_system_version=code_system_version)

    entity.add_description(description)
    entity.add_description(short_name, "ALTERNATIVE")
    entity.add_description(long_common_name, "ALTERNATIVE")
    entity.add_note(comments)
    entity.add_example(example_answers)
    entity.add_example(example_units)
    entity.add_example(example_ucum_units)
    entity.add_example(example_si_ucum_units)
    entity.set_status(status)

    if name in child_parent:
        for parent in child_parent[name]:
            entity.add_parent(parent, code_system, uri_converter.umls_entity_uri(code_system, parent))

    for property in [item for item in row if (item not in not_properties and row[item])]:
        entity.add_property(property,code_system,uri_converter.loinc_property_uri(property),row[property])

    return entity


def create_changeset(change_set_uri=str(uuid.uuid4())):
    return ChangeSet(change_set_uri)