"""
21849    v2841(-4, 1)
27964    v3284(-4, 3)
30829     v3478(1, 5)
"""

import pandas as pd
import json, os

dir = '/pkgs/tmp/proofs/'

def save_as_file(row):
    file = open(dir + row['name'], 'w')
    file.write(row['proof_nonord'] + '\n')
    file.close()
    
def save_redis_result(result):
    result = json.loads(result)
    try:
        proof = result['examples'][2][0]
        name = json.loads(proof)['name'].replace(',', ', ')
        file = open(dir + name, 'w')
        file.write(proof + '\n')
        file.close()
        print(name)
    except KeyError:
        pass

def done():
    return os.listdir(dir)
    
