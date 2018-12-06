from __future__ import print_function

import json
import pprint
import sys
from elasticsearch import Elasticsearch


def main():
    while True:
        menu()

        opcionMenu = raw_input("inserta un numero valor >> ")
        print("")
        if opcionMenu == "1":   
            ejercicio1()
        elif opcionMenu=="2":
            ejercicio2();
        elif opcionMenu == "3":
            ejercicio3();
        elif opcionMenu == "4":
            ejercicio4();
        elif opcionMenu == "5":
            exit()
        else:
            input("Opcion incorrecta")

def menu():
    print("---ElasticSearch---")
    print(" 1 - Ejercicio1")
    print(" 2 - Ejercicio2")
    print(" 3 - Ejercicio3")
    print(" 4 - Ejercicio4")
    print(" 5 - Salir")
    print("Escoja un ejercicio (1-5):")


def ejercicio1():
    pp = pprint.PrettyPrinter(indent=2)

    es = Elasticsearch()

    query = raw_input("\tIntroduzca los terminos a buscar separados por espacios >>")
    query.replace(' ', " OR ")


    properties = selectEstadistico()
    est = properties[0]
    properties_est = properties[1]

    number=5

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
        for i in results["aggregations"][j]["buckets"]:
            if (i["key"] not in words):
                words.append(i["key"])

    results = es.search(index="reddit-mentalhealth",
        body = {
            "query": {
                "query_string": {
                    "query": ' or '.join(words),
                }
            }
        })

    serializer(results['hits']['hits'], 'Ejercicio1.json')

def selectEstadistico():
    ests = ['gnd', 'mutual_information', 'jlh', 'chi_square', 'porcentage']
    while True:
        print("---Escoja estadistico---")
        print(" 1 -", ests[0])
        print(" 2 -", ests[1])
        print(" 3 -", ests[2])
        print(" 4 -", ests[3])
        print(" 5 -", ests[4])

        est = ests[raw_input("Escoja un estadistico (1-5): >> ")-1]

        switcher = {
            "gnd": {},
            "mutual_information": {'include_negatives':'true'},
            "jlh": {},
            "chi_square": {},
            "percentage": {},
        }

        if (switcher.get(est, "error") != "error"):
            return est, switcher.get(est, "error") 


def serializer(results, filename):
    with open(filename, 'w') as outfile:
        json.dump(results, outfile, sort_keys=True, indent=3)
    print("Cargado correctamente los resultados.")



# script
if __name__ == '__main__':
    main()