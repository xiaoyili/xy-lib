import numpy


def to_vector(v):
    """
    Take a matrix, and convert it to a vector.
    Or, if it is a vector, leave it unchanged.
    Regardless, we call the .todense() method if it exists.
    @note: This operation is destructive (I think).
    @note: Reshape is better than resize.
    """
    if "todense" in dir(v):
        v = v.todense()
    if len(v.shape) == 2:
        if v.shape[0] == 1:
            v.resize(v.size)
        if v.shape[0] == 2:
            v = numpy.reshape(v, v.shape[0] * v.shape[1])

    return v


class VStacker:
    """
    Vertically stack matrices as they come in, into self.data.
    """

    def __init__(self, matrices=None):
        if matrices is None:
            self.data = None
        else:
            self.data = numpy.vstack(matrices)

    def add(self, m):
        if self.data is None:
            self.data = m
        else:
            self.data = numpy.vstack([self.data, m])


def get_one_fold(data, label=None, fold_id=0, n_folds=10):
    '''
    split data in to train/test/validation set  (8-1-1)
    @param data: numpy matrix, split on the first dimension
    @param label: numpy ndarray
    @param fold_id:
    @param n_folds: default: 10 fold
    @return:
    '''
    if label is None:
        label = numpy.zeros([data.shape[0], 1])

    n_rows = data.shape[0]

    print '... Generate Fold_' + str(fold_id)

    data_idx = numpy.array(xrange(n_rows))
    tmp_idx = []
    valid_idx = data_idx[numpy.where(data_idx % (n_folds + 1) == fold_id)]
    tmp_idx.extend(valid_idx)
    test_idx = data_idx[numpy.where(data_idx % (n_folds + 1) == fold_id + 1)]
    tmp_idx.extend(test_idx)
    train_idx = numpy.setdiff1d(data_idx, tmp_idx)

    train_set = data[train_idx, :]
    valid_set = data[valid_idx, :]
    test_set = data[test_idx, :]
    train_label = label[train_idx, :]
    valid_label = label[valid_idx, :]
    test_label = label[test_idx, :]

    return train_set, valid_set, test_set, \
           train_label, valid_label, test_label


def get_N_fold(data, label=None, n_fold=10):
    '''
    input data and label, output an iteratable obj containing each fold
    @param data:
    @param label:
    @param n_fold:
    @return:
    '''
    if label is None:
        label = numpy.zeros([data.shape[0], 1])

    for i in xrange(n_fold):
        tr_set, va_set, te_set, \
        tr_label, va_label, te_label = get_one_fold(data, label, i, n_fold)

        train_set = (tr_set, tr_label)
        valid_set = (va_set, va_label)
        test_set = (te_set, te_label)

        yield (train_set, valid_set, test_set)


if __name__ == '__main__':
    # vec = [0, 1, 2]
    #
    # stacker = VStacker()
    # stacker.add(vec)
    # print stacker.data
    # stacker.add(vec)
    # new_v = stacker.data
    # print new_v
    #
    # print to_vector(new_v)

    a = numpy.zeros([100, 5])
    #    label = numpy.zeros([100,1])

    # tr_set, va_set, te_set, \
    # tr_label, va_label, te_label = get_one_fold(a, fold_id=9)
    #
    # print tr_set.shape, va_set.shape, te_set.shape
    # print tr_label

    all_fold = get_N_fold(a,n_fold=10)

    for fold in all_fold:
        train_set, valid_set, test_set = fold
        tr_set, tr_label = train_set
        print tr_set.shape

    pass


