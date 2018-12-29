import util

def get_results(endpoint_url, query):
    util.install_and_import('sparqlwrapper', "SPARQLWrapper")

    from SPARQLWrapper import SPARQLWrapper, JSON
    
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()["results"]["bindings"]

def get_medicamentos():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?medicationLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    ?medication wdt:P31 wd:Q12140.
    }
    LIMIT 100000"""

    json = get_results(endpoint_url, query)

    meds = []
    for e in json:
        for value in e.values():
            meds.append(value['value'])
    return meds