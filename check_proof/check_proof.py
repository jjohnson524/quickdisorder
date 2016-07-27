import json
import snappy
import word_problem

sample = """{"rels":["abbcb","ccAcAB","aabcc"],"group_args":[1,1,0],
"proof":[["a.b","b.a.b.a.b.b.a.a.a.b"],["a.B.c","a.B.c.a.a.c.c"],
["a.B.C","C.a.C.a.a.B"]],"name":"m003(-3,1)","gens":"a.b.c"}"""

def paths_to_root(claims):
    return [c[0] for c in claims]

def tree_ok(claims):
    print("NEED TO IMPLEMENT")
    return True

def all_nontrivial_edge_labels(solver, claims):
    edge_labels = set(sum(paths_to_root(claims), []))
    return all(solver.is_nontrivial(e) for e in edge_labels)

def check_claim(solver, claim):
    path_to_root, trivial_word = claim
    is_one = solver.is_trivial(''.join(trivial_word))    
    valid_words = set(path_to_root)
    return set(trivial_word).issubset(valid_words) and is_one

def check_proof(proof):
    if isinstance(proof, str):
        proof = json.loads(proof)
    M = snappy.Manifold(proof['name'])
    solver = word_problem.WordProblemSolver(M, bits_prec=100,
                                            fundamental_group_args=proof['group_args'])

    # We never actually use these assertions when checking the proof,
    # but it's hard to imagine that we will succeed if they fail.
    assert solver.rho.generators() == proof['gens'].split('.')
    assert solver.rho.relators() == proof['rels']

    claims = proof['proof']
    claims = [(a.split('.'), b.split('.')) for a, b in claims]
    a0 = tree_ok(claims)
    a1 = all_nontrivial_edge_labels(solver, claims)
    a2 = all(check_claim(solver, c) for c in claims)
    return a0 and a1 and a2

