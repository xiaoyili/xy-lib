import math
import numpy

# =============== start Equality checking ============================

DEFAULT_SANITY_CHECK_EPSILON = 1e-6


def sign(x): 1 if x >= 0 else -1


def floateq(a, b, epsilon=DEFAULT_SANITY_CHECK_EPSILON):
    """
    Compare two floats, with some epsilon tolerance.
    """
    return absolute_relative_error(a, b) < epsilon


def absolute_relative_error(a, b, epsilon=DEFAULT_SANITY_CHECK_EPSILON):
    return abs(a - b) / (abs(a) + abs(b) + epsilon)


def double_epsilon_multiplicative_eq(a, b, epsilon=DEFAULT_SANITY_CHECK_EPSILON):
    """
    Determine if doubles are equal to within a multiplicative factor of
    L{epsilon}.
    @note: This function should be preferred over
    L{double_epsilon_additive_eq}, unless the values to be compared may
    have differing signs.
    @precondition: sign(a) == sign(b)
    @rtype: bool
    """
    if a == b: return True
    if a == 0 and b == 0: return True
    assert a != 0
    assert b != 0
    assert sign(a) == sign(b)
    if a > b:
        d = a / b
    else:
        d = b / a
    assert d >= 1
    return True if d <= 1 + epsilon else False


def additive_eq(a, b):
    """
    Determine if doubles are equal to within an additive factor of
    L{SANITY_CHECK_EPSILON}.
    @note: Prefer L{double_epsilon_multiplicative_eq} to this function
    unless the values to be compared may have differing signs.
    """
    if a == b: return True
    if a == 0 and b == 0: return True
    d = math.fabs(a - b)
    return d <= DEFAULT_SANITY_CHECK_EPSILON

# =============== end Equality checking ============================


# =============== start numerical equations ========================

def logistic(x):
    """
    @todo: WRITEME
    """
    return 1. / (1 + math.exp(-x))


def cross_entropy(p):
    '''
    cross entropy
    @param p:
    @return:
    '''
    return -p * numpy.log2(p) - (1 - p) * numpy.log2(1 - p)


def roof(f):
    '''
    round to the next closest integer
    @param f:
    @return:
    '''
    return int(f + 0.5)


def Z_normalize(np_mat):
    # Z normalization
    mu = numpy.mean(np_mat, axis=0)
    sigma = numpy.std(np_mat, axis=0)
    return (data - mu) / (sigma + 1e-8)


def whiten(X, fudge=1E-18):
    from numpy import dot, sqrt, diag
    from numpy.linalg import eigh

    # the matrix X should be observations-by-components

    # get the covariance matrix
    Xcov = dot(X.T, X)

    # eigenvalue decomposition of the covariance matrix
    d, V = eigh(Xcov)

    # a fudge factor can be used so that eigenvectors associated with
    # small eigenvalues do not get overamplified.
    D = diag(1. / sqrt(d + fudge))

    # whitening matrix
    W = dot(dot(V, D), V.T)

    # multiply by the whitening matrix
    X = dot(X, W)

    return X, W


class MovingAverage:
    """
    Moving average.

    Yoshua Bengio:

        My preferred style of moving average is the following. Let's say you
        have a series x_t and you want to estimate the mean m of previous
        (recent) x's:

        m <-- m - (2/t) (m - x_t)

        Note that with (1/t) learning rate instead of (2/t) you get the exact
        historical average. With a larger learning rate (like 2/t) you give
        a bit more importance to recent stuff, which makes sense if x's are
        non-stationary (very likely here [in the setting of computing the
        moving average of the training error]). With a constant learning rate
        (independent of t) you get an exponential moving average.

        You can estimate a running average of the gradient variance by running
        averages of the mean gradient and of the
        square of the difference to the moving mean.

        .mean and .variance expose the moving average estimates.

    """

    def __init__(self, percent=False):
        self.mean = 0.
        self.variance = 0
        self.cnt = 0
        self.percent = percent

    def add(self, v):
        """
        Add value v to the moving average.
        """
        self.cnt += 1
        self.mean = self.mean - (2. / self.cnt) * (self.mean - v)
        # I believe I should compute self.variance AFTER updating the moving average, because
        # the estimate of the mean is better.
        # Yoshua concurs.
        this_variance = (v - self.mean) * (v - self.mean)
        self.variance = self.variance - (2. / self.cnt) * (self.variance - this_variance)

    def __str__(self):
        if self.percent:
            return "(moving average): mean=%.3f%% stddev=%.3f" % (self.mean, math.sqrt(self.variance))
        else:
            return "(moving average): mean=%.3f stddev=%.3f" % (self.mean, math.sqrt(self.variance))

# =============== end numerical equations ========================


# ==================== start sampling ========================

class RandSampling:
    """
    Random sampling routines.

    Here is an example:

    from common.myrandom import build, weighted_sample
    keys = "ABC"
    weights = [1., 3., 2.]
    indexed_weights = build(weights)
    print keys[weighted_sample(indexed_weights)]
    print keys[weighted_sample(indexed_weights)]
    """

    def __init__(self, weights):
        self.weight = weights
        self.indexed_weights = self.__build()


    def __build(self):
        """
        Create an index of weights. Must be done prior to calling weighted_sample.
        """
        indexed_weights = []
        sum = 0.
        for w in self.weight:
            indexed_weights.append(sum)
            sum += w
        return ("indexed_weights", indexed_weights, sum)

    def weighted_sample(self):
        """
        Sample an index, according to the weights in indexed_weights.
        indexed_weights must be obtained from the build() functon.
        Return the index, and its probability.
        """
        assert len(self.indexed_weights) == 3
        assert self.indexed_weights[0] == "indexed_weights"
        tot = self.indexed_weights[2]
        self.indexed_weights = self.indexed_weights[1]
        from bisect import bisect
        import random

        v = random.random()
        v *= tot
        idx = bisect(self.indexed_weights, v)
        idx -= 1
        assert idx >= 0 and idx < len(self.indexed_weights)
        if idx == len(self.indexed_weights) - 1:
            pr = 1. * (tot - self.indexed_weights[idx]) / tot
        else:
            pr = 1. * (self.indexed_weights[idx + 1] - self.indexed_weights[idx]) / tot
        return idx, pr

# ==================== end sampling ========================



if __name__ == '__main__':
    # === test random sampling ===
    # keys = "ABC"
    # weights = [1., 3., 2.]
    #
    # a = RandSampling(weights)
    # idx, prob = a.weighted_sample()
    # print keys[idx], prob

    # === test moving average ===
    # a = MovingAverage()
    # a.add(10)
    # print a.mean, a.variance    # 20, 200
    # a.add(20)
    # print a.mean, a.variance    # 20, 0
    # a.add(30)
    # print a.mean, a.variance    # 26.67, 7.407
    # a.add(40)
    # print a.mean, a.variance    # 33.33, 25.92

    # === test equalities ===
    # a = 3.1415926
    # b = 3.14159
    # print floateq(a,b)  # true
    # a = 3.1415926
    # b = 3.14158
    # print floateq(a,b)  # false
    #
    # a = 3.1415926
    # b = 3.14158
    # print double_epsilon_multiplicative_eq(a,b) # false
    #
    # a = 3.1415926
    # b = 3.14158
    # print additive_eq(a,b)

    pass