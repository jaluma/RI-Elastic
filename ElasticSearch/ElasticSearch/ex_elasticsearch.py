from __future__ import print_function
from util import serializer

from elasticsearch import Elasticsearch

import util
import wikidataquery

import json
import pprint
import sys
import codecs

def main():
    while True:
        menu()

        opcionMenu = raw_input("Inserta un numero >> ")
        print()
        if opcionMenu == "1":   
            ejercicio1()
        elif opcionMenu == "2":
            ejercicio2()
        elif opcionMenu == "3":
            ejercicio3()
        elif opcionMenu == "4":
            ejercicio4()
        elif opcionMenu == "5":
            return
        else:
            input("Opcion incorrecta")

def menu():
    print("--- ElasticSearch ---")
    print(" 1 - Ejercicio 1")
    print(" 2 - Ejercicio 2")
    print(" 3 - Ejercicio 3")
    print(" 4 - Ejercicio 4")
    print(" 5 - Salir")
    print("Escoja un ejercicio (1-5):")

def config():
    pp = pprint.PrettyPrinter(indent=2)

    es = Elasticsearch()

    #configuracion usada en el indice
    argumentos = {
      "properties": {
        "author": {
            "type": "text",
            "term_vector": "yes",
            "fielddata": "true"
        },
        "selftext": {
            "type":"text",
            "term_vector": "yes",
            "fielddata": "true"
        },
        "title": {
            "type":"text",
            "term_vector": "yes",
            "fielddata": "true"
        },
        "subreddit": {
            "type":"text",
            "term_vector": "yes",
            "fielddata": "true"
        }
      }
    }

    es.indices.put_mapping(index="reddit-mentalhealth",doc_type="put",body=argumentos,ignore=400)

    return es

def ejercicio1():
    es = config()

    query = raw_input("Introduzca los terminos a buscar separados por espacios >> ")
    print()
    query.replace(' ', " OR ")


    properties = select_estadistico()
    est = properties[0]
    properties_est = properties[1]

    number = 25

    results = es.search(index="reddit-mentalhealth",
    body = {
        "size": 0,
        "query": {
            "query_string": {
                "default_field": "selftext",
                "query": query,
            }
        }, 
          "aggs": {
            "Title": {
              "significant_terms": {
                "field": "title",
                "size": number,
                 est: properties_est
              }
            },
            "Text": {
              "significant_terms": {
                "field": "selftext",
                "size": number,
                 est: properties_est
              }
            },
            "Subreddit": {
              "significant_terms": {
                "field": "subreddit",
                "size": number,
                 est: properties_est
              }
            }
          }
    })

    stops_words = []

    #quitar palabras vacias
    with open("stop.txt") as f:
        for line in f:
            stops_words.append(line.split(" ",1)[0])
    stops_words = list(filter(lambda x: x!= "\n" and x!= "", stops_words))

    words = []
    for j in ["Subreddit", "Text", "Title"]:
        for i in results["aggregations"][j]["buckets"]:
            if (i["key"] not in stops_words and i["key"] not in words):
                words.append(i["key"])

    results = es.search(index="reddit-mentalhealth",
        body = {
            "query": {
                "query_string": {
                    "query": ' OR '.join(words),
                }
            }
        })

    json_data=[]
    for element in results['hits']['hits']:
        data = {}
        element = element['_source']
        data['selftext'] = element['selftext']
        data['title'] = element['title']
        data['subreddit'] = element['subreddit']
        json_data.append(data)


    util.serializer(json_data, 'Ejercicio1.json')

def ejercicio2():
    es = config()

    query = raw_input("Introduzca un termino/frase a buscar >> ")
    print()

    util.install_and_import("elasticsearch-dsl", "elasticsearch_dsl")
    from elasticsearch_dsl import Search
    from elasticsearch_dsl.query import MoreLikeThis

    number = 1000

    s = Search(using=es, index="reddit-mentalhealth")
    s = s.query(MoreLikeThis(like={query}, fields=["selftext","title","subreddit"])) \

    results = s.execute().to_dict()['hits']
    print(results)

    #words = []
    #for j in ["Subreddit", "Text", "Title"]:
    #    for i in results["aggregations"][j]["buckets"]:
    #        if (i["key"] not in words):
    #            words.append(i["key"])

    #results = es.search(index="reddit-mentalhealth",
    #    body = {
    #        "query": {
    #            "query_string": {
    #                "query": ' OR '.join(words),
    #            }
    #        }
    #    })
    
    util.serializer(results, 'Ejercicio2.json')


def ejercicio3():
    lista_medicamentos_wikidata = wikidataquery.get_medicamentos()

    #guardar los medicamentos
    #serializer(lista_medicamentos_wikidata, 'Medicamentos.json')
    
    es = config()

    properties = select_estadistico()
    est = properties[0]
    properties_est = properties[1]

    number = 1000

    results = es.search(index="reddit-mentalhealth",
    body = {
        "size": 0,
        "query": {
            "query_string": {
                "query": "using OR prescribed OR dose OR mg -water",
                "allow_leading_wildcard": "true"
            }
        }, 
          "aggs": {
            "Title": {
              "significant_terms": {
                "field": "title",
                "size": number,
                 est: properties_est
              }
            },
            "Text": {
              "significant_terms": {
                "field": "selftext",
                "size": number,
                 est: properties_est
              }
            }
          }
    })

    meds = []
    for j in ["Text", "Title"]:
        for i in results["aggregations"][j]["buckets"]:
            if (i["key"] not in meds and i["key"] in lista_medicamentos_wikidata):
                meds.append(i["key"])

    print("--- Medicamentos ---")
    for med in meds:
        print("\t",med)
    print()

def ejercicio4():
    data, query = select_problematica()

    es = config()

    properties = select_estadistico()
    est = properties[0]
    properties_est = properties[1]

    number = 5

    results = es.search(index="reddit-mentalhealth",
    body = {
        "size": 0,
        "query": {
            "query_string": {
                "default_field": "selftext",
                "query": query,
            }
        }, 
          "aggs": {
            "Title": {
              "significant_terms": {
                "field": "title",
                "size": number,
                 est: properties_est
              }
            },
            "Text": {
              "significant_terms": {
                "field": "selftext",
                "size": number,
                 est: properties_est
              }
            },
            "Subreddit": {
              "significant_terms": {
                "field": "subreddit",
                "size": number,
                 est: properties_est
              }
            }
          }
    })

    words = []
    for j in ["Subreddit", "Text", "Title"]:
        [words.append(i["key"]) for i in results["aggregations"][j]["buckets"] if i["key"] not in words and any(i["key"] in s for s in data)]

    print("--- Expresiones usadas ---")
    for word in words:
        print("\t",word)
    print()


def select_estadistico():
    ests = ['gnd', 'mutual_information', 'jlh', 'chi_square', 'porcentage']
    while True:
        print("---Escoja estadistico---")
        print(" 1 -", ests[0])
        print(" 2 -", ests[1])
        print(" 3 -", ests[2])
        print(" 4 -", ests[3])
        print(" 5 -", ests[4])

        est = ests[input("Escoja un estadistico (1-5): >> ") - 1]
        print()

        switcher = {
            "gnd": {},
            "mutual_information": {'include_negatives':'true'},
            "jlh": {},
            "chi_square": {},
            "percentage": {},
        }

        if (switcher.get(est, "error") != "error"):
            return est, switcher.get(est, "error") 

def select_problematica():
    print(" 1 - Problematica del suicidio")
    print(" 2 - Problematica de las autolesiones")
    select = input("Escoja un ejercicio (1-2) >> ")
    print()

    if (select == 1):
        data = load_titles_google_scholar('scholar-suicidio.json')
        query = "suicide"
    elif (select == 2):
        data = load_titles_google_scholar('scholar-self-harm.json')
        query = "self-harm"

    return data, query


def load_titles_google_scholar(filename):
    with open(filename, 'r') as json_data:
        bom_maybe = json_data.read(3)
        if bom_maybe != codecs.BOM_UTF8:
            json_data.seek(0)
        data = json.load(json_data)

    titles=[]
    for e in data:
        titles.append(e['title'])
    return titles



# script
if __name__ == '__main__':
    main()