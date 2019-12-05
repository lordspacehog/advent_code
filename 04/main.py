#!/usr/bin/env python3
import argparse
from itertools import tee, groupby
import operator


def is_sorted(num: int) -> bool:
    itr = [int(x) for x in str(num)]
    a, b = tee(itr)
    next(b, None)
    return all(map(operator.le, a, b))


def has_doubles(num: int) -> bool:
    itr = str(num)
    if len(itr) != len(set(itr)):
        return True
    return False


def check_cons(num: int) -> bool:
    itr = str(num)
    groups = [(k, len(list(g))) for k, g in groupby(itr)]
    if not any(map(lambda x: x[1] == 2, groups)):
        return False
    return True


def main():
    parser = argparse.ArgumentParser('search for password in given range')
    parser.add_argument('--start', '-s', type=int, dest='start', required=True)
    parser.add_argument('--end', '-e', type=int, dest='end', required=True)
    parser.add_argument('--advanced', '-a', dest='adv',
                        action='store_true')
    args = parser.parse_args()

    print('starting search!')
    search_space = range(args.start, args.end+1)
    filtered = filter(is_sorted, search_space)
    doubles = list(filter(has_doubles, filtered))
    dbl_len = len(doubles)

    print(f'{dbl_len} possible passwords found in range')

    if args.adv:
        advanced_list = list(filter(check_cons, doubles))
        adv_len = len(advanced_list)
        print(f'{adv_len} possible passwords using advanced search')


if __name__ == '__main__':
    main()
