from __future__ import annotations

from enum import IntEnum
from typing import Any, Tuple, TypedDict

from pydantic import BaseModel


class Coordinate(BaseModel):
    lat: float
    lon: float

    class Config:
        allow_mutation = False


class Waypoint(Coordinate):
    alt: float = 5.0

    class Config:
        allow_mutation = False


class FenceType(IntEnum):
    """Enumeration of the different geofence types.

    An inclusive fence creates a boundary that the PX4 may not exit. An exclusive fence creates a boundary the PX4
    may not enter.
    """

    INCLUSIVE = 1
    EXCLUSIVE = 2


class Geofence(BaseModel):
    vertices: Tuple[Coordinate, ...] = ()
    fence_type: FenceType = FenceType.EXCLUSIVE

    class Config:
        allow_mutation = False

    def add_vertex(self, vertex: Coordinate) -> Geofence:
        return Geofence(vertices=self.vertices + (vertex,), fence_type=self.fence_type)


class Mission(BaseModel):
    waypoints: Tuple[Waypoint, ...] = ()
    geofences: Tuple[Geofence, ...] = ()

    class Config:
        allow_mutation = False

    def add_waypoint(self, waypoint: Waypoint) -> Mission:
        return Mission(waypoints=self.waypoints + (waypoint,), geofences=self.geofences)

    def remove_waypoint(self, index: int) -> Mission:
        if index < 0 or index >= len(self.waypoints):
            raise ValueError(f"Index {index} is out of bounds for waypoints")

        waypoints = tuple(waypoint for i, waypoint in enumerate(self.waypoints) if i != index)
        geofences = self.geofences

        return Mission(waypoints=waypoints, geofences=geofences)

    def add_geofence(self, geofence: Geofence) -> Mission:
        return Mission(waypoints=self.waypoints, geofences=self.geofences + (geofence,))

    def remove_geofence(self, index: int) -> Mission:
        if index < 0 or index >= len(self.geofences):
            raise ValueError(f"Index {index} is out of bounds for geofences")

        waypoints = self.waypoints
        geofences = tuple(geofence for i, geofence in enumerate(self.geofences) if i != index)

        return Mission(waypoints=waypoints, geofences=geofences)

    @property
    def empty(self) -> bool:
        return len(self.waypoints) == 0
