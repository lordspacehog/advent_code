from __future__ import annotations
from typing import List
from dataclasses import dataclass, field


@dataclass
class Point:
    x: int
    y: int


@dataclass
class LineSegment:
    start: Point
    end: Point
    __orientation: bool = field(init=False)

    def __post_init__(self):
        self.__orientation = False if self.start.x == self.end.x else True

    def orientation(self) -> str:
        return 'horizontal' if self.__orientation else 'vertical'

    def is_horizontal(self) -> bool:
        return self.__orientation

    def is_vertical(self) -> bool:
        return not self.__orientation

    def intersects(self, target) -> bool:
        if self.is_vertical() and target.is_horizontal():
            return (
                self.start.x in range(
                    *sorted((target.start.x, target.end.x)))
                and
                target.start.y in range(
                    *sorted((self.start.y, self.end.y)))
            )
        elif self.is_horizontal() and target.is_vertical():
            return (
                self.start.y in range(
                    *sorted((target.start.y, target.end.y)))
                and
                target.start.x in range(
                    *sorted((self.start.x, self.end.x)))
            )
        return False


class Wire(List[LineSegment]):
    def __init__(self, point_list: List[str]):
        current = [0, 0]
        for point in point_list:
            direction, distance = (point[0], int(point[1:]))
            if direction == "R":
                tmp = [current[0]+distance, current[1]]
                self.append(LineSegment(Point(*current), Point(*tmp)))
                current = tmp
                continue
            if direction == "L":
                tmp = [current[0]-distance, current[1]]
                self.append(LineSegment(Point(*current), Point(*tmp)))
                current = tmp
                continue
            if direction == "U":
                tmp = [current[0], current[1]+distance]
                self.append(LineSegment(Point(*current), Point(*tmp)))
                current = tmp
                continue
            if direction == "D":
                tmp = [current[0], current[1]-distance]
                self.append(LineSegment(Point(*current), Point(*tmp)))
                current = tmp
                continue

    def get_intersections(self, wire) -> List[Point]:
        points: List[Point] = []
        for segment in wire:
            if segment.is_horizontal():
                filtered = filter(lambda x: x.is_vertical(), self)
                points.extend([
                    Point(i.start.x, segment.start.y)
                    for i in filtered if segment.intersects(i)
                ])
            else:
                filtered = filter(lambda x: x.is_horizontal(), self)

                points.extend([
                    Point(segment.start.x, i.start.y)
                    for i in filtered if segment.intersects(i)
                ])

        return points[1:]
