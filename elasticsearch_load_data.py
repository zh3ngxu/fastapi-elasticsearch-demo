from datetime import datetime
from elasticsearch import Elasticsearch
import json
from pprint import pprint


es = Elasticsearch([{"host": "localhost", "port": 9200}])


doc = {
    "title": "AI and LLM",
    "description": "learn how to build a LLM agent using OpenAI o1 model",
}

response = es.index(index="courses", document=doc)
pprint(response)

# WfjKvZMBWel3VliotoqE

# pprint(es.get(index="courses", id="WfjKvZMBWel3VliotoqE"))
