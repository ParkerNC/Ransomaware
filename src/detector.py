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

        names = ["read_count", "write_count", "read_bytes", "write_bytes", "read_time", "write_time", "read_merged_count", "write_merged_count", "busy_time"]
        for item in self.count():
            self.data.append([item])
        
        while(1):
            counts = self.count()
            print(counts)

            self.update(counts)

            with open(self.file + '.csv', "w") as avgfile:
                for i, avg in enumerate(self.data):
                    a = 0
                    for x in avg:
                        a += x
                    a /= len(avg)
                    avgfile.write("{}, {:.2f}\n".format(names[i], a))

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