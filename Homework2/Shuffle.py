from time import time
import array as arr
from random import randint
import matplotlib.pyplot as plt


def knuth_shuffle(to_shuffle, n):
    for i in range(0, n-2):  # #stop before last item
        j = randint(i, n-1)  # #randint is inclusive on both sides and we don't want to include n
        x = to_shuffle[j]
        to_shuffle[j] = to_shuffle[i]
        to_shuffle[i] = x


def build_array(size):
    ret_list = arr.array('i')
    for i in range(0, size-1):
        ret_list.append(i)
    return ret_list


def shuffle_driver():
    # lists to rep x and y plane for plot of size vs time
    x = []  # #size of array
    y = []  # #time (ms)

    sizes = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000, 10000]
    for sz in sizes:
        t = 0
        print("running size", sz)
        for _ in range(10):
            to_shuffle = build_array(sz)
            start = time()
            knuth_shuffle(to_shuffle, len(to_shuffle))
            end = time()
            t += (end - start)*1000
        x.append(sz)
        y.append(t // 10)

    # Plot results of tests
    plt.plot(x, y)
    plt.xlabel("n (size of array)")
    plt.ylabel("time (ms)")
    plt.show()
    # plt.savefig("python_running_times.png", format='png')


if __name__ == '__main__':
    shuffle_driver()









