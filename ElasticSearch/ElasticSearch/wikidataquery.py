import subprocess
import sys


def install_and_import(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    from SPARQLWrapper import SPARQLWrapper, JSON
    global SPARQLWrapper, JSON

def get_results(endpoint_url, query):
    install_and_import('sparqlwrapper')

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

def main():
    install_and_import('sparqlwrapper')

# script
if __name__ == '__main__':
    main()