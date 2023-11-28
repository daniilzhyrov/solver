import sys
import math
from abc import ABC, abstractmethod

from pyibex import Interval

import model

class AbstractHeuristic(ABC):
    
    @staticmethod
    @abstractmethod
    def contract(dataset: model.DataSet, distances: model.DistanceSet) -> model.DistanceSet:
        pass


class TriangleInequality(AbstractHeuristic):

    @staticmethod
    def contract(dataset: model.DataSet, distances: model.DistanceSet) -> model.DistanceSet:
        for i in range(dataset.numPoints):
            for j in range(dataset.numPoints):
                if i != j and distances.getMaxDistance(i, j) < sys.float_info.max:
                    for k in range(dataset.numPoints):
                        if k != i and k != j and distances.getMaxDistance(j, k) < sys.float_info.max:
                            distances.updateDistance(i, k, Interval (max(0, max(distances.getMinDistance(i, j) - distances.getMaxDistance(j, k), distances.getMinDistance(2, 3) - distances.getMaxDistance(1, 2))), distances.getMaxDistance(i, j) + distances.getMaxDistance(j, k)))
        return distances
    
class PyramidInequality:

    @staticmethod
    def contract(dataset: model.DataSet, distances: model.DistanceSet) -> model.DistanceSet:
        for i in range(dataset.numPoints):
            for j in range(dataset.numPoints):
                if i < j and distances.getMaxDistance(i, j) < sys.float_info.max:
                    for k in range(dataset.numPoints):
                        if k != i and k != j and distances.getMaxDistance(j, k) < sys.float_info.max:
                            for l in range(dataset.numPoints):
                                if l != i and l != j and l < k and distances.getMaxDistance(l, i) < sys.float_info.max and distances.getMaxDistance(l, j) < sys.float_info.max and distances.getMinDistance(k, l) != 0:
                                    arg1 = (distances.getMaxDistance(k, j) ** 2 + distances.getMaxDistance(l, j) ** 2 - distances.getMinDistance(k, l) ** 2) / (2 * distances.getMaxDistance(k, j) * distances.getMaxDistance(l, j))
                                    arg2 = (distances.getMaxDistance(k, i) ** 2 + distances.getMaxDistance(l, i) ** 2 - distances.getMinDistance(k, l) ** 2) / (2 * distances.getMaxDistance(k, i) * distances.getMaxDistance(l, i))
                                    if (arg1 > 1 or arg1 < -1 or arg2 > 1 or arg2 < -1):
                                        continue
                                    alpha = math.acos(arg1)
                                    gamma = math.acos(arg2)
                                    maxValue = math.sqrt ((distances.getMaxDistance(j, k) * distances.getMaxDistance(i, l) + distances.getMaxDistance(j, l) * distances.getMaxDistance(i, k)) ** 2 - 4 * distances.getMaxDistance(j, k)*distances.getMaxDistance(i, k) * distances.getMaxDistance(j, l) * distances.getMaxDistance(i, l) * math.cos((alpha + gamma) / 2) ** 2) / distances.getMinDistance(k, l)
                                    if math.isnan(maxValue):
                                        distances.updateDistance(i, k, Interval (0, maxValue))
        return distances
    
