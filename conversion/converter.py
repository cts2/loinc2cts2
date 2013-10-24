import uuid

from cts2_types import *


def row2entity(row, about_fn, code_system, code_system_version):
    name = row['LOINC_NUM']
    return Entity(name=name, namespace=code_system, about=about_fn(name),
                  code_system=code_system, code_system_version=code_system_version)


def create_changeset(change_set_uri=str(uuid.uuid4())):
    return ChangeSet(change_set_uri)