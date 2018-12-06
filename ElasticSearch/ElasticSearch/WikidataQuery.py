import subprocess
import sys

from SPARQLWrapper import SPARQLWrapper, JSON

def get_results(endpoint_url, query):
    install_and_import('sparqlwrapper')

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()["results"]["bindings"]

def install_and_import(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_medicamentos():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?medicamentoLabel WHERE {
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
      OPTIONAL { ?item wdt:P2176 ?medicamento. }
    }"""

    return get_results(endpoint_url, query)

for result in results:
    print(result)