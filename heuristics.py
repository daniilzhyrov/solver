import sys
from pyibex import Interval

import model

class TriangleInequality:

    @staticmethod
    def contract(dataset: model.DataSet, distances: model.DistanceSet):
        for i in range(dataset.numPoints):
            for j in range(dataset.numPoints):
                if i != j and distances.getMaxDistance(i, j) < sys.float_info.max:
                    for k in range(dataset.numPoints):
                        if k != i and k != j and distances.getMaxDistance(j, k) < sys.float_info.max:
                            distances.updateDistance(i, k, Interval (max(0, distances.getMinDistance(i, j) - distances.getMaxDistance(j, k)), distances.getMaxDistance(i, j) + distances.getMaxDistance(j, k)))
        return distances