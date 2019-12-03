#!/usr/bin/env python3
import argparse
import math
from typing import List
from functools import reduce


def get_fuel_requirements(mass: int) -> int:
    fuel = math.floor(mass/3)-2

    if fuel > 0:
        return fuel + get_fuel_requirements(fuel)

    return 0


def main():
    parser = argparse.ArgumentParser('Calculate Needed Fuel.')
    parser.add_argument('loadout', metavar='module_file', type=str)
    args = parser.parse_args()

    module_list: List[int] = []
    with open(args.loadout, 'r') as filep:
        module_list = list(map(int, filep.read().rstrip().split('\n')))

    result = reduce(lambda a, b: a+b, map(get_fuel_requirements, module_list))
    print(f'total fuel needed is {result}')


if __name__ == '__main__':
    main()
