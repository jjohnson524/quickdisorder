from . import double_group

class MonoidInGroup(object):
    def __init__(self, elements, ball, saturate=True):
        self.ball = ball
        if saturate:
            self.elements = set()
            self._has_one = self.saturate(elements)
        else:
            self.elements = elements.copy()
        
    def saturate(self, new_elements):
        """
        Returns whether 1 is in self after saturation
        """
        active = set(new_elements)
        ans = self.elements | set(active)
        while len(active) > 0:
            new_elts = set()
            for x in ans:
                for y in active:
                    for z in [x*y, y*x]:
                        if z in self.ball.elements and z not in ans:
                            # The next application of the "identity" map is
                            # to try to prevent accumulation of numerical error.
                            z = self.ball.element_dict[z]
                            new_elts.add(z)
                            if z.is_one():
                                self.elements = ans | new_elts
                                self._has_one = True
                                return True

            ans = ans | new_elts
            active = new_elts

        self.elements = ans
        return False

    def has_one(self):
        return self._has_one

    def copy(self):
        M = MonoidInGroup(self.elements, self.ball, False)
        M._has_one = self._has_one
        return M
        
    def words(self):
        ans = [a.word for a in self.elements]
        ans.sort(key=lambda x: (len(x), x))
        return ans

    def __contains__(self, x):
        return x in self.elements

    def __len__(self):
        return len(self.elements)

def printer(depth, string):
    print('  '*depth + '%d: ' % depth + string)
    
def ball_has_order(B, P, recur_depth):
    printer(recur_depth, 'Size of P is %d' % len(P.elements))
    if P.has_one():
        printer(recur_depth, "Contradiction: 1 in P")
        #words = [e.word for e in P.elements if e.is_one()]
        #printer(recur_depth, repr(words))
        return False, P

    # If we get close to building a full P, we almost always get
    # there.  It is better to stop now and later try again with an
    # increased radius, because adding those last few elements is very
    # expensive.
    if len(P) > 0.9 * 0.5 * len(B.elements):
        return True, P

    for x, y in B.non_id_element_pairs:
        if (x not in P) and (y not in P):
            printer(recur_depth, 'Adding %s' % x.word)
            newP = P.copy()
            newP.saturate([x])
            ans = ball_has_order(B, newP, recur_depth+1)
            if ans[0]:
                return ans
            else:
                printer(recur_depth, 'Adding %s' % y.word)
                newP = P.copy()
                newP.saturate([y])
                return ball_has_order(B, newP, recur_depth+1)

    return True, P

def has_non_orderable_group(manifold, ball_radius=3,min_bits_accuracy=15,
                            fundamental_group_args = [True, True, False]):
    """
    >>> import snappy
    >>> M = snappy.Manifold('m003(-3,1)')
    >>> has_non_orderable_group(M)
    0: Ball has 151 elements
    0: Size of P is 3
    0: Adding b
      1: Size of P is 104
      1: Contradiction: 1 in P
    0: Adding B
      1: Size of P is 14
      1: Adding c
        2: Size of P is 97
        2: Contradiction: 1 in P
      1: Adding C
        2: Size of P is 54
        2: Contradiction: 1 in P
    True

    >>> N = snappy.Manifold('m004(1, 2)')
    >>> has_non_orderable_group(N)
    0: Ball has 159 elements
    0: Size of P is 3
    0: Adding b
      1: Size of P is 14
      1: Adding c
        2: Size of P is 36
        2: Adding aB
          3: Size of P is 49
          3: Adding aC
            4: Size of P is 67
            4: Adding bC
              5: Size of P is 70
              5: Adding aBB
                6: Size of P is 72
    False
    """
    G = double_group.Double3ManifoldGroup(
              manifold, min_bits_accuracy, fundamental_group_args)
    a = G('a')
    B = G.ball(ball_radius)
    printer(0, 'Ball has %d elements' % len(B.elements))
    P = MonoidInGroup([a], B)
    return not ball_has_order(B, P, 0)[0]

