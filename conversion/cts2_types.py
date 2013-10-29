from datetime import datetime
import abc
import pytz


class Cts2Type():
    @abc.abstractmethod
    def as_dict(self):
        raise NotImplementedError("Please implement the 'as_dict' method on all Cts2Types.")


class ChangeSet(Cts2Type):
    def __init__(self, change_set_uri):
        self.change_set = {
            "ChangeSet": {
                "state": "OPEN",
                "entryCount": 0,
                "creationDate": str(datetime.now(pytz.UTC).isoformat()),
                "changeSetURI": change_set_uri,
                "member": []
            }
        }

    def get_uri(self):
        return self.change_set['ChangeSet']['changeSetURI']

    def add_member(self, member):
        self._validate(member)

        cs = self.change_set['ChangeSet']

        copy = member.as_dict()
        copy['entryOrder'] = cs['entryCount'] + 1
        cs['member'].append(copy)

        count = cs['entryCount']
        cs['entryCount'] = count + 1

    def as_dict(self):
        return self.change_set

    def _validate(self, member):
        if not len(member.as_dict()) == 1: raise Exception("Ill formed Cts2 Member Dict.")


class Entity(Cts2Type):
    statuses_map = {
        "ACTIVE": "ACTIVE",
        "TRIAL": "ACTIVE",
        "DISCOURAGED": "ACTIVE",
        "DEPRECATED": "INACTIVE"
    }

    def __init__(self, about, name, namespace, code_system, code_system_version):
        self.entity = {
            "entityDescription": {
                "namedEntity": {
                    "about": about,
                    "entityID": {
                        "namespace": namespace,
                        "name": name
                    },
                    "describingCodeSystemVersion": {
                        "version": {
                            "content": code_system_version
                        },
                        "codeSystem": {
                            "content": code_system
                        }
                    },
                    "entityType": [
                        {
                            "uri": "http://www.w3.org/2004/02/skos/core#",
                            "namespace": "skos",
                            "name": "Concept"
                        }
                    ]
                }
            }
        }

    def add_description(self, description, type="PREFERRED"):
        if 'designation' not in self.entity['entityDescription']['namedEntity']:
            self.entity['entityDescription']['namedEntity']['designation'] = []
        self.entity['entityDescription']['namedEntity']['designation'].append({"designationRole":type, "value":description})

    def set_status(self, status="ACTIVE"):
        cts2_status = self.statuses_map[status]
        self.entity['entityDescription']['namedEntity']['entryState'] = cts2_status

        if not cts2_status == "ACTIVE":
            status_ref = {'content': status}
            self.entity['entityDescription']['namedEntity']['status'] = status_ref

    def as_dict(self):
        return self.entity


class CodeSystem(Cts2Type):
    def __init__(self, about, name):
        self.code_system = {
            "codeSystem": {
                "codeSystemName": name,
                "about": about
            }
        }

    def as_dict(self):
        return self.code_system