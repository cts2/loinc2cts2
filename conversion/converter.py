import uuid

from cts2_types import *


def row2entity(row, about_fn, code_system, code_system_version, child_parent):
    name = row['LOINC_NUM']
    description = row['COMPONENT']
    short_name = row['SHORTNAME']
    long_common_name = row['LONG_COMMON_NAME']
    status = row['STATUS']

    entity = Entity(name=name, namespace=code_system, about=about_fn(name),
                  code_system=code_system, code_system_version=code_system_version)

    entity.add_description(description)
    entity.add_description(short_name, "ALTERNATIVE")
    entity.add_description(long_common_name, "ALTERNATIVE")
    entity.set_status(status)

    if name in child_parent:
        for parent in child_parent[name]:
            entity.add_parent(parent, code_system, about_fn(parent))

    for property in [item for item in row if item not in ['LOINC_NUM','COMPONENT','SHORTNAME','LONG_COMMON_NAME', 'STATUS']]:
        entity.add_property(property,code_system,about_fn(property),row[property])

    return entity


def create_changeset(change_set_uri=str(uuid.uuid4())):
    return ChangeSet(change_set_uri)