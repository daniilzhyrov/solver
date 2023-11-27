import sys
from pyibex import IntervalVector, CtcFwdBwd, Function, Interval
import math

import reader, model

assert sys.argv[1] is not None, "The data file is not specified!"

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


assert dataset.numPoints > 3, "??? wtf"

result = [model.Point(0, 0, 0), model.Point(response.getMedianDistance(0, 1), 0, 0)]

p2 = response.getMedianDistance(0, 1) + response.getMedianDistance(1, 2) + response.getMedianDistance(0, 2)
p2 /= 2

s2 = math.sqrt(p2 * (p2-response.getMedianDistance(0, 1)) * (p2-response.getMedianDistance(1, 2)) * (p2-response.getMedianDistance(0, 2)))
x2 = 2 * s2 / response.getMedianDistance(0, 1)
y2 = math.sqrt(response.getMedianDistance(0, 2) ** 2 - x2 ** 2)

result.append(model.Point(x2, y2, 0))


for pointNum in range (3, dataset.numPoints):
    # f1 = Function('x', 'y', 'z', f'(x)^2 + (y)^2 + (z)^2 - {response.getMedianDistance(pointNum, 0)}^2')
    # f2 = Function('x', 'y', 'z', f'({result[1].x} - x)^2 + (y)^2 + (z)^2 - {response.getMedianDistance(pointNum, 1)}^2')
    # f3 = Function('x', 'y', 'z', f'({result[2].x} - x)^2 + ({result[2].y} - y)^2 + (z)^2 - {response.getMedianDistance(pointNum, 2)}^2')

    # print(f'(x)^2 + (y)^2 + (z)^2 - {response.getMedianDistance(pointNum, 0)}^2')
    # print(f'({result[1].x} - x)^2 + (y)^2 + (z)^2 - {response.getMedianDistance(pointNum, 1)}^2')
    # print(f'({result[2].x} - x)^2 + ({result[2].y} - y)^2 + (z)^2 - {response.getMedianDistance(pointNum, 2)}^2')

    # ctc1 = CtcFwdBwd(f1)
    # ctc2 = CtcFwdBwd(f2)
    # ctc3 = CtcFwdBwd(f3)

    # ctc = ctc1 & ctc2 & ctc3

    # if pointNum == 3:
    #     domain = IntervalVector([Interval(-response.getMedianDistance(pointNum, 0), response.getMedianDistance(pointNum, 0)), Interval(-response.getMedianDistance(pointNum, 0), response.getMedianDistance(pointNum, 0)), Interval(0, response.getMedianDistance(pointNum, 0))])
    # else:
    #     domain = IntervalVector([Interval(-response.getMedianDistance(pointNum, 0), response.getMedianDistance(pointNum, 0)), Interval(-response.getMedianDistance(pointNum, 0), response.getMedianDistance(pointNum, 0)), Interval(-response.getMedianDistance(pointNum, 0), response.getMedianDistance(pointNum, 0))])

    # for _ in range(100):
    #     ctc.contract(domain)
    #     # ctc3.contract(domain)

    x = (response.getMedianDistance(pointNum, 0) ** 2 + result[1].x ** 2 - response.getMedianDistance(pointNum, 1) ** 2) / (2 * result[1].x)
    y = (result[2].y ** 2 + result[2].x ** 2 - 2 * result[2].x * x - response.getMedianDistance(pointNum, 2) ** 2 + response.getMedianDistance(pointNum, 0) ** 2) / (2 * result[2].y)
    z = math.sqrt (response.getMedianDistance(pointNum, 0) ** 2 - x ** 2 - y ** 2)

    if (pointNum > 3) and (abs((x - result[3].x) ** 2 + (y - result[3].y) ** 2 + (z - result[3].z) ** 2 - response.getMaxDistance(pointNum, 3)) > abs((x - result[3].x) ** 2 + (y - result[3].y) ** 2 + (-z - result[3].z) ** 2 - response.getMaxDistance(pointNum, 3))):
        z = -z
    
    result.append(model.Point(x, y, z))



error = 0
for entry in dataset:
    print(result[entry.pointA - 1].distanceTo(result[entry.pointB - 1]))


    
