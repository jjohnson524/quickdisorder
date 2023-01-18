import snappy, quickdisorder

def inverse_word(word):
    return word.swapcase()[::-1]

def next_gen_dict(gens):
    all_gens = gens + [g.swapcase() for g in gens]
    next_gen = { g:[h for h in all_gens if h.swapcase() != g] for g in all_gens }
    return next_gen

def ball_in_free_group(gens,  length):
    next_gen = next_gen_dict(gens)
    curr = gens + [g.swapcase() for g in gens]
    ans = [''] + curr
    for i in range(length - 1):
        new_words = []
        for word in curr:
            new_words += [word + g for g in next_gen[word[-1]]]
        ans += new_words
        curr = new_words
    return ans

class CayleyBall(object):
    """
    Ball about 1 in the Cayley graph of a group.
    """
    def __init__(self, group, radius):
        all_words = ball_in_free_group(group.rho.generators(), radius)
        ordered_elements = [group(w) for w in all_words]
        elements = set(ordered_elements)
        # Create the list of {g, g^-1} pairs
        seen_one = dict()
        non_id_element_pairs = []
        for g in ordered_elements:
            h = g.inverse()
            if h in seen_one:
                h = seen_one[h]
                # Want the words associated to g and h be inverses in
                # the free group.
                if h.word != inverse_word(g.word):
                    g._set_word(inverse_word(h.word))
                non_id_element_pairs.append( (seen_one[h], g) )
            else:
                seen_one[g] = g

        self.ordered_elements = ordered_elements
        self.elements = elements
        self.non_id_element_pairs = non_id_element_pairs
        self.element_dict = {e:e for e in ordered_elements}

    def __len__(self):
        return len(self.elements)


class Double3ManifoldGroup(object):
    """
    >>> M = snappy.Manifold('m004(1,2)')
    >>> G = Double3ManifoldGroup(M)
    >>> G('abcABC')
    <NGE: abcABC; (-0.25857712442742253+0.48081251833270267j) (-0.783996070719998+2.150934815529558j) (-0.2774615146731634+0.23771079574212495j) (-1.8761415167194206-0.4598487432176286j)>
    >>> B = G.ball(2)
    >>> len(B)
    37
    """
    def __init__(self, manifold, min_bits_accuracy=15, fundamental_group_args = [True, True, False]):
        self.manifold = manifold
        self.rho = snappy.snap.polished_holonomy(manifold, 100,
                                                 lift_to_SL2=True,
                                                 fundamental_group_args=fundamental_group_args)
        self.min_bits_accuracy = min_bits_accuracy

    def __call__(self, word):
        A = self.rho(word)
        return quickdisorder.sl2matrix.DoubleGroupElement(A, self.min_bits_accuracy, word)

    def ball(self, radius):
        return CayleyBall(self, radius)


def product_identity(element, conjugates, factors):
    for g in conjugates:
        z = element * g
        if z.is_one():
            return True
        elif factors > 2:
            ans = product_identity(z,conjugates,factors-1)
            if ans:
                return True
    return False

def is_generalized_torsion(element, ball, factors):
    if element.is_one() or factors == 1:
        return False
    conjugates = set()
    for g in ball.elements:
        z = g * element * g.inverse()
        conjugates.add(z)
    

    for h in conjugates:
        ans = product_identity(h, conjugates, factors)
        if ans:
            return True
    return False

def has_generalized_torsion(manifold, ball_radius=3, factors=2,
                            silent=False, track=False, return_proof=False,
                            min_bits_accuracy=15,
                            fundamental_group_args = [True, True, False]):
    """
    >>> import snappy
    >>> M = snappy.Manifold('m003(-3,1)')
    >>> has_non_orderable_group(M, track=True)  # doctest: +SKIP
    0: Ball has 151 elements
    0: Adding a
      1: Size of P is 3
      1: Adding b
        2: Size of P is 104
        2: Contradiction: b*a*b*a*b*b*a*a*a*b = 1 in P
      1: Adding B
        2: Size of P is 14
        2: Adding c
          3: Size of P is 97
          3: Contradiction: a*B*c*a*a*c*c = 1 in P
        2: Adding C
          3: Size of P is 54
          3: Contradiction: C*a*C*a*a*B = 1 in P
    True
    >>> ans, proof = has_non_orderable_group(M, silent=True, return_proof=True)
    >>> ans
    True
    >>> json.loads(proof)['proof']   # doctest: +SKIP
    [[u'a.b', u'b.a.b.a.b.b.a.a.a.b'], [u'a.B.c', u'a.B.c.a.a.c.c'], [u'a.B.C', u'C.a.C.a.a.B']]
    >>> N = snappy.Manifold('m004(1, 2)')
    >>> has_non_orderable_group(N)
    0: Ball has 159 elements
    0: Adding a
      1: Size of P is 3
      1: Adding b
        2: Size of P is 14
        2: Adding c
          3: Size of P is 36
          3: Adding aB
            4: Size of P is 49
            4: Adding aC
              5: Size of P is 67
              5: Adding bC
                6: Size of P is 70
                6: Adding aBB
                  7: Size of P is 72
    False


    >>> names = ['m003(-1, 3)', 'm003(-1, 5)', 'm003(-3, 1)', 'm003(-4, 3)', 'm003(-5, 2)', 'm003(-5, 4)', 'm004(-3, 2)', 'm004(-6, 1)']
    >>> manifolds = [snappy.Manifold(name) for name in names]
    >>> [has_non_orderable_group(M, silent=True) for M in manifolds]
    [False, False, True, True, True, True, False, False]
    """
    #if return_proof:
    #    track = True
    #    printer = ProofPrinter(silent)
    #else:
    #    printer = Printer(silent)
    G = Double3ManifoldGroup(
              manifold, min_bits_accuracy, fundamental_group_args)
    #a = G('a')
    B = G.ball(ball_radius)
    print("Ball has " + str(len(B.elements)))
    for g in B.elements:
        #print(g.word)
        ans = is_generalized_torsion(g,B,factors)
        if ans:
            return ans
    return False
    #printer.size_of_ball(B, 0)
    #printer.add_monoid_gen(a, 0)
    #P = MonoidInGroup([a], B, biorder=biorder, track=track)
    #ans = not ball_has_order(B, P, biorder, printer, 1)[0]

    #if return_proof:
    #    if ans:
    #        return ans, printer.proof_string(manifold, fundamental_group_args)
    #    else:
    #        return ans, None
    #return ans
