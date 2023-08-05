import csv
from timeit import Timer
import os
import shutil
import time
import statistics


def create_dir():
    if os.path.exists("load_testing_measurements"):
        shutil.rmtree("load_testing_measurements")
    os.mkdir("load_testing_measurements")


def time_of_program(function, arg1, arg2):
    t = Timer("""{0}""".format(function(arg1, arg2)), setup="""x = range(1000)""")
    time = t.timeit()
    return round(time, 5)


def measure_time(func):
    create_dir()

    lst = os.listdir(path='load_testing_data/')

    lst.sort()
    elem = 0
    data_sizes_qt = 0  # кол-во размеров данных

    sizes = []

    for i in range(len(lst)):

        if lst[i].split('_')[0] != elem:
            sizes.append(int(lst[i].split('_')[0]))
            data_sizes_qt += 1
            elem = lst[i].split('_')[0]

    count = len(lst) // data_sizes_qt  # кол-во наборов данных опр.размера

    sizes.sort()

    start = int(sizes[0])

    end = int(sizes[-1]) + 1

    step = int(sizes[1]) - int(sizes[0])

    times = [0] * data_sizes_qt

    for i in range(data_sizes_qt):
        times[i] = [0] * count

    for m in range(start, end, step):

        for i in range(count):
            with open('load_testing_data/{0}_{1}.txt'.format(m, i), 'r') as f:
                linelist = (f.readlines())

    for m in range(data_sizes_qt):

        for i in range(count):
            times[m][i] = (time_of_program(func, linelist[0][:-1:], linelist[1]))

    timestamp = int(time.time())
    filename = "%s.csv" % timestamp

    data_sizes = len(range(start, end, step))

    with open('load_testing_measurements/{0}'.format(filename), 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=' ',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['size', 'min', 'max', 'avg', 'median'])
        size = start
        for i in range(data_sizes):
            times[i].sort()
            elem = times[i]

            mn = min(elem)
            mx = max(elem)
            avg = round(sum(elem) / len(elem), 5)

            md = round(statistics.median(elem), 5)

            filewriter.writerow([size, mn, mx, avg, md])

            size += step
