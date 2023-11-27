import sys

class Point:
    _x, _y = float, float
    _pointId = int

    def __init__(self, x: float, y: float, pointId: int):
        self._x = x
        self._y = y
        self._pointId = pointId

    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y

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
    _minDistances: [[float]]
    _maxDistances: [[float]]

    def __init__(self, dataset: DataSet):
        self._minDistances = [[0 for _ in range(dataset.numPoints)] for _ in range(dataset.numPoints)]
        self._maxDistances = [[sys.float_info.max for _ in range(dataset.numPoints)] for _ in range(dataset.numPoints)]
        # for _ in range(dataset.numPoints):
        #     minEntry = []
        #     maxEntry = []
        #     for _ in range(dataset.numPoints):
        #         minEntry.append(0)
        #         maxEntry.append(sys.float_info.max)
        #     self._minDistances.append(entry)
        for entry in dataset:
            self._minDistances[entry.pointA - 1][entry.pointB - 1] = self._minDistances[entry.pointB - 1][entry.pointA - 1] = entry.distanceMin
            self._maxDistances[entry.pointA - 1][entry.pointB - 1] = self._maxDistances[entry.pointB - 1][entry.pointA - 1] = entry.distanceMax

    # def __getitem__(self, key: tuple) -> (float, float):
    #     return self._distances[min(key)][max(key)], self._distances[max(key)][min(key)]
    
    # def __setitem__(self, key: tuple, value: (float, float)):
    #     self._distances[min(key)][max(key)] = value[0]
    #     self._distances[max(key)][min(key)] = value[1]

    def getMinDistance(self, pointA: int, pointB: int) -> float:
        return self._minDistances[pointA][pointB]
    
    def getMaxDistance(self, pointA: int, pointB: int) -> float:
        return self._maxDistances[pointA][pointB]
        #return self._distances[max(pointA, pointB)][min(pointA, pointB)]
    
    def updateMinDistance(self, pointA: int, pointB: int, value: float):
        self._minDistances[pointA][pointB] = self._minDistances[pointB][pointA] = max (value, self._minDistances[pointA][pointB])

    def updateMaxDistance(self, pointA: int, pointB: int, value: float):
        self._maxDistances[pointA][pointB] = self._maxDistances[pointB][pointA] = min (value, self._maxDistances[pointA][pointB])
        # self._distances[max(pointA, pointB)][min(pointA, pointB)] = min (value, self._distances[max(pointA, pointB)][min(pointA, pointB)])