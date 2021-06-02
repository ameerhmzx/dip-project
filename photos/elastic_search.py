from os import environ
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

ES_URL = environ.get('ELASTIC_URL', default="http://{}:{}@{}:{}".format(
    environ.get('ELASTIC_USERNAME', 'elastic'),
    environ.get('ELASTIC_PASSWORD', 'password'),
    environ.get('ELASTIC_HOSTNAME', 'localhost'),
    environ.get('ELASTIC_PORT', '9200'),
))

es = None


def connect_es():
    global es

    if es is not None:
        return

    es = Elasticsearch(hosts=ES_URL)
    body = {
        'mappings': {
            'properties': {
                'face_id': {'type': 'integer'},
                'person_id': {'type': 'integer'},
                'vector': {
                    'type': 'dense_vector',
                    'dims': 128
                }
            }
        }
    }

    try:
        es.indices.create(index='face_embeddings', body=body)
    except RequestError:
        pass


def save_embeddings(vector, face_id, person_id=-1):
    global es
    connect_es()

    es.create('face_embeddings', id=face_id, body={
        'face_id': face_id,
        'person_id': person_id,
        'vector': vector
    })


def delete_embeddings(face_id):
    connect_es()
    es.delete('face_embeddings', id=face_id)


def set_person(face_id, person_id):
    connect_es()
    res = es.update('face_embeddings', id=face_id, body={'doc': {'person_id': person_id}})


def recognize_person(vector):
    connect_es()

    response = es.search(index='face_embeddings', body={
        "size": 5,
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "must_not": {
                            "term": {
                                "person_id": -1
                            }
                        }
                    },
                },
                "script": {
                    "source": "cosineSimilarity(params.qVector, 'vector') + 1",
                    "params": {
                        "qVector": vector
                    }
                }
            }
        }
    })

    results = sorted(response['hits']['hits'], key=lambda x: x['_score'], reverse=True)
    results = list(filter(lambda x: x['_score'] > 1.2, results))

    return None if len(results) == 0 else results[0]['_source']['person_id']
