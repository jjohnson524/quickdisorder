import json
import snappy
import word_problem

sample1 = """{"rels":["abbcb","ccAcAB","aabcc"],"group_args":[1,1,0],
"proof":[["a.b","b.a.b.a.b.b.a.a.a.b"],["a.B.c","a.B.c.a.a.c.c"],
["a.B.C","C.a.C.a.a.B"]],"name":"m003(-3,1)","gens":"a.b.c"}"""

sample2 = """ {"rels":["aacbc","bcBcbA","abcccbabccbabccb"],"group_args":[1,1,0],"proof":[["a.b.c","b.c.a.a.c"],["a.b.C.aB","a.aB.a.a.b.C.a.aB.aB.C.b.aB.a.a.b"],["a.b.C.bA.ca","ca.ca.a.b.a.a"],["a.b.C.bA.AC.Ab.cb.ac","cb.cb.a.ac.ac.a.a.a.a"],["a.b.C.bA.AC.Ab.cb.CA.bc","bc.cb.a.bc.cb.a.bc.cb.cb.a.bc.cb.a.bc.cb.a.a.a.bc.cb.a.bc.cb.a.a.a.bc.cb.a.bc.cb.a.bc"],["a.b.C.bA.AC.Ab.cb.CA.CB","CB.a.a.bA.AC.CB.a.a.bA.AC.CB.a.a.bA.AC.CB.a"],["a.b.C.bA.AC.Ab.cb.CA.BC","bA.AC.a.a.BC.a.BC.bA.AC.a.a.BC.bA.AC.a.a.BC"],["a.b.C.bA.AC.Ab.cb.CA.Ba","AC.Ba.Ba.AC.b.a"],["a.b.C.bA.AC.Ab.cb.CA.B.c.aC","a.a.c.a.c.a.c.a.aC.a.a.c.a.c.a.c.a.aC.a.a.c.a.c.a.c.a.c.a.aC.a.a.c.a.c.a.c.a.aC.a.a.c.a.c.a.c.a.aC.a.aC"],["a.b.C.bA.AC.Ab.cb.CA.B.c.cA","a.a.cA.c.a.a.a.a.cA.c.a.a.a.a.a.a.cA.c.a.a.a.a.cA.c.a.a.a.a.cA.cA.c.a.a.a.a.cA.c.a.a.a.a.cA.c.a.a.a.a"],["a.b.C.bA.AC.Ab.cb.CA.B.c.C.ba","a.B.a.a.ba.a.B.a.B.C.C.ba"],["a.b.C.bA.AC.Ab.cb.CA.B.c.C.AB","AB.C.C.C.B.AB.C.C.C.C.C.C.C.B.AB.B.a.B.C.a.B.C.a.B.C"]],"name":"m007(-4,3)","gens":"a.b.c"}"""

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

