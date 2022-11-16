import psutil
import time
import sys

class Counter():
    def __init__(self, length: int, filename: str) -> None:
        self.length = length
        self.data = []
        self.file = filename
        self.run()

    def run(self) -> None:

        maxes = []
        names = ["read_count", "write_count", "read_bytes", "write_bytes", "read_time", "write_time", "read_merged_count", "write_merged_count", "busy_time"]
        for item in self.count():
            maxes.append(0)
            self.data.append([item])
        
        with open(self.file + ".csv", 'a') as totfile:
            for name in names:
                totfile.write("{}, ".format(name))

            totfile.write('\n')

        while(1):
            counts = self.count()
            print(counts)

            self.update(counts)

            with open("max_" + self.file + '.csv', "w") as avgfile:
                for i, avg in enumerate(self.data):
                    d = avg[-1]
                    d -= avg[0]
                    if maxes[i] < d:
                        maxes[i] = d
                    avgfile.write("{}, {:.2f}\n".format(names[i], d))

                for i, m in enumerate(maxes):
                    avgfile.write("MAX, {}, {:.2f}\n".format(names[i], m))

            with open(self.file + ".csv", 'a') as totfile:
                for i, data in enumerate(counts):
                    totfile.write("{:.2f}, ".format(data))

                totfile.write('\n')

            time.sleep(1)

    def count(self) -> tuple:
        counts = psutil.disk_io_counters(perdisk=False)

        return counts

    def update(self, counts: tuple) -> None:
        for i, item in enumerate(counts):
            self.data[i].append(item)
            if len(self.data[i]) > self.length:
                self.data[i].pop(0)
        


if __name__  == "__main__":
    c = Counter(5, sys.argv[1])