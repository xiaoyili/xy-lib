__author__ = 'eric'


def item_count(l, name="value"):
    """
        For the elements of list l, count the occurrences of each value,
        and return a list sorted in decreasing order of {name: "value", count: count}
    """
    from collections import defaultdict

    cnt = defaultdict(int)
    for j in l: cnt[j] += 1
    s = [(cnt[j], j) for j in cnt]
    s.sort()
    s.reverse()
    return [{name: i[1], "count": i[0]} for i in s]


def chop_list(args, lengths):
    """
    Chopping list into tuples of particular lengths.
    If a tuple has length "0", return a single item.

    >>> chop_list(range(7), (0,3,1,2))
    [0, (1, 2, 3), (4,), (5, 6)]
    """
    r = []
    idx = 0
    for l in lengths:
        if l == 0:
            r.append(args[idx])
            idx += 1
        else:
            r.append(tuple(args[idx:idx + l]))
            idx += l
    assert idx == len(args)
    assert len(r) == len(lengths)
    return r


def unique_elements_list_intersection(list1, list2):
    """
    Return the unique elements that are in both list1 and list2
    (repeated elements in listi will not be duplicated in the result).
    This should run in O(n1+n2) where n1=|list1|, n2=|list2|.
    """
    return list(set.intersection(set(list1), set(list2)))


if __name__ == '__main__':

    t1 = ['a','a','b','c']
    # print item_count(t1)

    # print chop_list(t1, (0,2,1))

    t2 = ['a', 'c', 'd']

    # print unique_elements_list_intersection(t1,t2)

    pass

