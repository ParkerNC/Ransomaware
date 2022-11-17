import psutil
import time
import sys

class Counter():
    def __init__(self, length: int, filename: str) -> None:
        self.length = length
        self.data = []
        self.file = filename
        self.load_thresholds()
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

        secs = 0

        while(1):
            counts = self.count()

            self.update(counts)

            with open("max_" + self.file + '.csv', "w") as avgfile:
                for i, avg in enumerate(self.data):
                    d = avg[-1]
                    d -= avg[0]
                    
                    if maxes[i] < d:
                        maxes[i] = d
                    else:
                        if d == 0:
                            d += 1
                        if maxes[i] != 0 and maxes[i]/d > 3:
                            secs += 1

                    if secs > 5:
                        maxes[i] = 0
                        secs = 0

                    avgfile.write("{}, {:.2f}\n".format(names[i], d))

                for i, m in enumerate(maxes):
                    avgfile.write("MAX, {}, {:.2f}\n".format(names[i], m))

            with open(self.file + ".csv", 'a') as totfile:
                for i, data in enumerate(counts):
                    totfile.write("{:.2f}, ".format(data))

                totfile.write('\n')

            if self.check_mal(maxes):
                print("Malicious Behavior Detected: Disconnect from the internet and shutdown the device.")

            time.sleep(1)

    def count(self) -> tuple:
        counts = psutil.disk_io_counters(perdisk=False)

        return counts

    def update(self, counts: tuple) -> None:
        for i, item in enumerate(counts):
            self.data[i].append(item)
            if len(self.data[i]) > self.length:
                self.data[i].pop(0)
        
    def load_thresholds(self) -> None:
        self.bases = []
        with open("max_base.csv", 'r') as basefile:
            for line in basefile:
                if len(line.split(',')) > 2:
                    self.bases.append(float(line.split(',')[-1].strip()))

    def check_mal(self, maxes: list) -> bool:
        for i in range(0, 4):
            if maxes[i] > self.bases[i]:
                if maxes[i]/self.bases[i] > 14:
                    if ((maxes[0]+1)/(maxes[1]+1) < 1.8) and ((maxes[0]+1)/(maxes[1]+1) > 0.3):
                        return True
        return False

if __name__  == "__main__":
    c = Counter(2, sys.argv[1])