def umls_entity_uri(code_system, name):
    return "http://umls.nlm.nih.gov/SAB/%s/%s" % (code_system, name)

def loinc_property_uri(name):
    return "http://id.loinc.org/pr/%s" % name


