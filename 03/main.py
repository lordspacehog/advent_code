#!/usr/bin/env python3
import argparse
import wires


def mdist(point: wires.Point) -> int:
    return abs(point.x) + abs(point.y)

def main():
    parser = argparse.ArgumentParser('Find closes crossed wire')
    parser.add_argument('wires', metavar='wire_def', type=str)
    args = parser.parse_args()

    with open(args.wires, 'r') as filep:
        wire_paths = filep.read().rstrip().split('\n')
        wire1 = wires.Wire(wire_paths[0].split(','))
        wire2 = wires.Wire(wire_paths[1].split(','))

    closest = min(map(mdist, wire1.get_intersections(wire2)))
    print(f'distance to nearest point is {closest}')


if __name__ == '__main__':
    main()
