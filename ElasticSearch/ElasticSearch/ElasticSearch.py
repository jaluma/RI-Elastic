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

    #query = raw_input("\tIntroduzca los terminos a buscar >>")
    query = "alcohol"

    query.replace(' ', " OR ")
    #est = input("\tIntroduzca estadistico (JSON) >>")
    est = "'gnd': {}"
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
                "size":number,
              }
            },
            "Text": {
              "significant_terms": {
                "field": "selftext",
                "size": number,
              }
            },
            "Subreddit": {
              "significant_terms": {
                "field": "subreddit",
                "size": number,
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
            "from": 0,
            "size": 100,
            "query": {
                "query_string": {
                    "query": ' or '.join(words),
                }
            }
        })


if __name__ == '__main__':
    main()