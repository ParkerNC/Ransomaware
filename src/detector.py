import psutil
import time

class Counter():
    def __init__(self) -> None:
        self.run()

    def run(self) -> None:

        c = 1
        data = []
        names = ["read_count", "write_count", "read_bytes", "write_bytes", "read_time", "write_time", "read_merged_count", "write_merged_count", "busy_time"]
        for item in self.count():
            data.append(item)
        
        while(1):
            counts = self.count()
            c += 1
            print(counts)
            for i, item in enumerate(counts):
                data[i] += item

            with open("avgs.csv", "w") as avgfile:
                for j, item in enumerate(data):
                    avgfile.write("{}: {:.2f} \n".format(names[j], item/c))

            time.sleep(1)

    def count(self) -> tuple:
        counts = psutil.disk_io_counters(perdisk=False)

        return counts


if __name__  == "__main__":
    c = Counter()