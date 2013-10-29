import uuid

from cts2_types import *


def row2entity(row, about_fn, code_system, code_system_version):
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

    return entity


def create_changeset(change_set_uri=str(uuid.uuid4())):
    return ChangeSet(change_set_uri)