import sys
import math
from pyibex import Interval

class Point:
    _x, _y, _z = float, float, float

    def __init__(self, x: float, y: float, z: int):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def z(self) -> float:
        return self._z
    
    def distanceTo(self, p):
        return math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2 + (self.z - p.z) ** 2)

class DataEntry:
    _pointA, _pointB = int, int
    _distanceMin, _distanceMax = float, float

    def __init__(self, pointA: int, pointB: int, distanceMin: float, distanceMax: float):
        self._pointA = pointA
        self._pointB = pointB
        self._distanceMin = distanceMin
        self._distanceMax = distanceMax

    @property    
    def pointA(self) -> int:
        return self._pointA
    
    @property
    def pointB(self) -> int:
        return self._pointB
    
    @property
    def distanceMin(self) -> float:
        return self._distanceMin
    
    @property
    def distanceMax(self) -> float:
        return self._distanceMax

class DataSet:
    _dataset = [DataEntry]
    _numPoints = None

    def __init__(self, entries: [DataEntry]):
        self._dataset = entries

    def __iter__(self):
        return iter(self._dataset)

    def add(self, entry: DataEntry):
        self._dataset.append(entry)
    
    @property
    def numPoints(self) -> int:
        #check if _numPoints is set, otherwise calculate it
        if self._numPoints == None:
            self._numPoints = 0
            for entry in self._dataset:
                if entry.pointA > self._numPoints:
                    self._numPoints = entry.pointA
                if entry.pointB > self._numPoints:
                    self._numPoints = entry.pointB
        return self._numPoints
    
class DistanceSet:
    _distances: [[Interval]]

    def __init__(self, dataset: DataSet):
        self._distances = [[ Interval(0, sys.float_info.max) for _ in range(dataset.numPoints)] for _ in range(dataset.numPoints)]
        for entry in dataset:
            self._distances[entry.pointA - 1][entry.pointB - 1] = self._distances[entry.pointB - 1][entry.pointA - 1] = Interval(entry.distanceMin, entry.distanceMax)

    def getMinDistance(self, pointA: int, pointB: int) -> float:
        return self._distances[pointA][pointB].lb()
    
    def getMaxDistance(self, pointA: int, pointB: int) -> float:
        return self._distances[pointA][pointB].ub()
        #return self._distances[max(pointA, pointB)][min(pointA, pointB)]
    
    def updateDistance(self, pointA: int, pointB: int, interval: Interval):
        self._distances[pointA][pointB] = self._distances[pointB][pointA] = self._distances[pointA][pointB] & interval

    # def updateMaxDistance(self, pointA: int, pointB: int, value: float):
    #     self._maxDistances[pointA][pointB] = self._maxDistances[pointB][pointA] = min (value, self._maxDistances[pointA][pointB])
    #     # self._distances[max(pointA, pointB)][min(pointA, pointB)] = min (value, self._distances[max(pointA, pointB)][min(pointA, pointB)])

    def getMedianDistance(self, pointA: int, pointB: int):
        return (self._minDistances[pointA][pointB] + self._maxDistances[pointA][pointB]) / 2