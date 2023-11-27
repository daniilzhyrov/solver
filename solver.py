import sys
from pyibex import Interval, Function, IntervalVector, CtcFwdBwd

import reader, model

dataset = reader.DataReader.read(sys.argv[1])

response = model.DistanceSet(dataset)

accumulated = 0

for iter in range(10000):
    for i in range(dataset.numPoints):
        for j in range(dataset.numPoints):
            if i != j and response.getMaxDistance(i, j) < sys.float_info.max:
                for k in range(dataset.numPoints):
                    if k != i and k != j and response.getMaxDistance(j, k) < sys.float_info.max:
                        response.updateMinDistance(i, k, max(0, response.getMinDistance(i, j) - response.getMaxDistance(j, k)))
                        response.updateMaxDistance(i, k, response.getMaxDistance(i, j) + response.getMaxDistance(j, k))
                        assert max(0, response.getMinDistance(i, j) - response.getMaxDistance(j, k)) <= response.getMaxDistance(i, k), "Error!!!" + str(i) + " " + str(j) + " " + str(k) + " " + str(response.getMaxDistance(i, k)) + " " + str(response.getMaxDistance(j, k)) + " " + str(response.getMinDistance(i, j))

    print(iter, flush=True)
    oldAccumulated = accumulated
    accumulated = 0
    for p1 in range(dataset.numPoints):
        for p2 in range(p1):
            accumulated += response.getMaxDistance(p1, p2) - response.getMinDistance(p1, p2)
    print(accumulated, flush=True)
    if accumulated == oldAccumulated:
        break
    # change = False
    # if accumulated == oldAccumulated:
    #     for p1 in range(dataset.numPoints):
    #         for p2 in range(p1):
    #             if response.getMaxDistance(p1, p2) > response.getMinDistance(p1, p2) + 0.0001:
    #                 change = True
    #                 response.updateMinDistance(p1, p2, response.getMaxDistance(p1, p2) - 0.00001)
    #     if not change:
    #         break



print(iter, flush=True)
accumulated = 0
for p1 in range(dataset.numPoints):
    for p2 in range(p1):
        accumulated += response.getMaxDistance(p1, p2) - response.getMinDistance(p1, p2)
print(accumulated, flush=True)

