import snappy
from . import sl2matrix, ball

class Double3ManifoldGroup(object):
    """
    >>> M = snappy.Manifold('m004(1,2)')
    >>> G = Double3ManifoldGroup(M)
    >>> G('abcABC')
    <NGE: abcABC; (-0.258577124427+0.480812518333j) (-0.78399607072+2.15093481553j) (-0.277461514673+0.237710795742j) (-1.87614151672-0.459848743218j)>
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
        return sl2matrix.DoubleGroupElement(A, self.min_bits_accuracy, word)

    def ball(self, radius):
        return ball.CayleyBall(self, radius)



