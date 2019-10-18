from random import randint
from sys import argv
from time import time
import matplotlib.pyplot as plt


def buildListToSort(size):
    array = [randint(1, 10000) for _ in range(size)]
    return array


def shellSort(n, to_sort):
    gaps = [1, 4, 9, 20, 46, 103, 233, 525, 1182, 2660, 5985, 13467, 30301, 68178, 153401, 345152, 776591, 1747331,
            3931496, 8845866, 19903198, 44782196, 100759940, 226709866, 510097200, 1147718700, 2582367076, 5810325920,
            13073233321, 29414774973]
    gaps.reverse()
    for gap in gaps:
        for i in range(gap, n):
            temp = to_sort[i]
            j = i
            while j >= gap and to_sort[j-gap] > temp:
                to_sort[j] = to_sort[j-gap]
                j -= gap
            to_sort[j] = temp


if __name__ == '__main__':
    if len(argv) > 1:
        n = int(argv[1])
        to_sort = buildListToSort(n)
        start = time()
        shellSort(n, to_sort)
        end = time()
        print(end - start)
    else:
        # performs automated testing
        x = []
        y = []
        sizes = [10, 50, 100, 200, 500, 1000, 1200, 1500, 2000, 2500, 3000, 5000, 6000, 7000, 8000, 9000, 10000, 20000,
                 30000, 40000]
        for sz in sizes:
            t = 0
            print("running size", sz)
            for _ in range(10):
                arr = [randint(1, 10000) for _ in range(sz)]
                start = time()
                shellSort(sz, arr)
                end = time()
                print(arr)
                t += (end - start) * 1000
            x.append(sz)
            y.append(t // 10)

        # Plot results of tests
        plt.plot(x, y)
        plt.xlabel("n (size of array)")
        plt.ylabel("time (ms)")
        plt.show()

