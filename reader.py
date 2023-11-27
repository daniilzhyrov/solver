import model

class DataReader:
    @staticmethod
    def read(filename: str) -> model.DataSet:
        dataset = []
        with open(filename) as f:
            for line in f:
                line = line.strip()
                pointA, pointB, distanceMin, distanceMax = line.split()
                distanceMin = float(distanceMin)
                distanceMax = float(distanceMax)
                dataset.append(model.DataEntry(int(pointA), int(pointB), distanceMin, distanceMax))
        return model.DataSet(dataset)