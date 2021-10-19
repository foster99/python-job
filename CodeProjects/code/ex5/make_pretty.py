from pprint import pprint, pformat
import json

path = "./data/ikea_sofas.json"
with open(path) as f:
    contents = f.read()
    print(contents[-1])

    