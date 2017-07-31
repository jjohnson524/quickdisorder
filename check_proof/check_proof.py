"""
Each nonordering proof tree is stored as a JSON string.  Here is
one which matches the figure in the paper illustrating the nonordering
tree for the fundamental group of the Weeks manifold. 
"""

sample_weeks = """\
{
    "name": "m003(-3,1)",
    "gens": "a.b", 
    "rels": ["ababaBaaB", "ababAbbAb"],
    "proof": [
        ["a.b.aB", "a.b.a.b.aB.a.aB"],
        ["a.b.bA", "b.a.b.a.bA.b.bA"],
        ["a.B", "B.a.B.B.a.a.B.a.a.B"]
    ],
    "group_args":[1,1,1]
}
"""



import random, json, os
import snappy
import word_problem
import networkx as nx


sample1 = """{"rels":["abbcb","ccAcAB","aabcc"],"group_args":[1,1,0],
"proof":[["a.b","b.a.b.a.b.b.a.a.a.b"],["a.B.c","a.B.c.a.a.c.c"],
["a.B.C","C.a.C.a.a.B"]],"name":"m003(-3,1)","gens":"a.b.c"}"""

def invert_word(word):
    return word.swapcase()[::-1]

def paths_to_root(claims):
    return [c[0] for c in claims]

def build_graph(claims):
    paths = paths_to_root(claims)
    T = nx.DiGraph()
    T.add_node('1')
    leaves = ['1']
    for path in paths:
        vert = '1'
        for g in path:
            new_vert = vert + '.' + g
            T.add_edge(vert, new_vert, label=g)
            vert = new_vert
        leaves.append(vert)
    return T, leaves
    
        
def tree_ok(claims):
    T, leaves = build_graph(claims)

    # A branching is a directed forest where every vertex has in-degree
    # a most 1.            
    if not nx.is_branching(T):
        return False

    # Now check that the tree is trivalent.
    degrees = T.degree()
    leaf_count = 0
    for v in T.nodes():
        if v in leaves:
            if degrees[v] != 1:
                return False
            leaf_count += 1
        else:
            if degrees[v] != 3:
                return False
            # Check the outgoing edges of this interior vertex
            # labelled by inverse words.
            w0, w1 = [attr['label'] for attr in T.adj[v].values()]
            if invert_word(w0) != w1:
                return False

    # Make sure there wasn't any redundancy in the path data.
    if leaf_count != len(leaves):
        return False

    # This should be redundant, but might as well check. 
    paths_from_root = nx.single_source_shortest_path(T, '1')
    for v, path in paths_from_root.items():
        for p in path:
            if not v.startswith(p):
                return False
    return True
    
def all_nontrivial_edge_labels(solver, claims):
    edge_labels = set(sum(paths_to_root(claims), []))
    return all(solver.is_nontrivial(e) for e in edge_labels)

def check_claim(solver, claim):
    path_to_root, trivial_word = claim
    is_one = solver.is_trivial(''.join(trivial_word))    
    valid_words = set(path_to_root)
    return set(trivial_word).issubset(valid_words) and is_one

def check_proof(proof, bits_prec=100):
    if isinstance(proof, str):
        proof = json.loads(proof)
    M = snappy.Manifold(proof['name'])
    solver = word_problem.WordProblemSolver(M, bits_prec=bits_prec,
                                            fundamental_group_args=proof['group_args'])

    # We never actually use these assertions when checking the proof,
    # but it's hard to imagine that we will succeed if they fail.
    assert solver.rho.generators() == proof['gens'].split('.')
    assert solver.rho.relators() == proof['rels']

    claims = proof['proof']
    claims = [(a.split('.'), b.split('.')) for a, b in claims]
    a0 = tree_ok(claims)
    if not a0:
        return False
    a1 = all_nontrivial_edge_labels(solver, claims)
    a2 = all(check_claim(solver, c) for c in claims)
    return a0 and a1 and a2

def check_proof_harder(proof, max_bits=1000):
    bits = 100
    while bits <= 1000:
        try:
            ans = check_proof(proof, bits)
            return ans, bits
        except word_problem.WordProblemError:
            bits = 2*bits
    return False, bits

def proof_sizes():
    dir = '/pkgs/tmp/proofs/'
    num_edges = []
    num_leaves = []
    max_edges = 0
    max_leaves = 0
    max_non_trivial_word = 0    
    
    for f in os.listdir(dir):
        proof = json.loads(open(dir + f).read())
        claims = proof['proof']
        claims = [(a.split('.'), b.split('.')) for a, b in claims]
        T, leaves = build_graph(claims)
        e = T.number_of_edges()
        l = len(leaves)
        num_edges.append(e)
        num_leaves.append(l)
        
        if e > max_edges:
            max_edges = e
            print('edges', e, f)

        if l > max_leaves:
            max_leaves = l
            print('leaves', l, f)

        trivial_words_lengths = [len(c[1]) for c in claims]
        max_trival_word = max(max_trival_word, max(trivial_words_lengths))
        
    return num_edges, num_leaves, max_trival_word

def random_proof():
    dir = '/pkgs/tmp/proofs/'
    d = os.listdir(dir)
    f = random.choice(d)
    proof = open(dir + f).read()
    bits = 100
    while bits <= 1000:
        try:
            ans = check_proof(proof, bits)
            return (f, ans, bits)
        except word_problem.WordProblemError:
            bits = 2*bits
    return (f, False, bits)
        

