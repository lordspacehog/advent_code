# coding: utf-8
from itertools import tee
import operator

search_space = range(183564,657474+1)
def is_sorted(num):
    itr = [int(x) for x in str(num)]
    a, b = tee(itr)
    next(b, None)
    return all(map(operator.le, a, b))

filtered = filter(is_sorted, search_space)
def has_doubles(num):
    itr = str(num)
    if len(itr) != len(set(itr)):
        return True
    return False

doubles = filter(has_doubles, filtered)
list(doubles)
filtered = filter(is_sorted, search_space)
doubles = filter(has_doubles, filtered)
out = list(doubles)
out
len(out)
