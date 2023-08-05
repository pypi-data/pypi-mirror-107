import os
import csv
import matplotlib.pyplot as plt
import shutil
import time


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    for row in reader:
        print(" ".join(row))


def create_dir():
    if os.path.exists("load_testing_plots"):
        shutil.rmtree("load_testing_plots")
    os.mkdir("load_testing_plots")


def create_chart(csv_file_path: str):
    path = csv_file_path

    sizes = []

    maxs = []

    mins = []

    medians = []

    avgs = []

    with open(path, encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter=" ")

        count = 0

        for row in file_reader:
            sizes.append(row["size"])

            mins.append(row["min"])

            maxs.append(row["max"])

            avgs.append(row["avg"])

            medians.append(row["median"])

            count += 1

    mins.sort()
    maxs.sort()
    medians.sort()
    avgs.sort()

    plt.figure(figsize=(12, 7))
    plt.subplot(221)
    plt.plot((sizes), (mins), '-', label='minimal')
    plt.legend()
    plt.subplot(222)
    plt.plot((sizes), (maxs), '--', label='maximum')
    plt.legend()
    plt.subplot(223)
    plt.plot((sizes), (medians), '-.', label='median')
    plt.legend()
    plt.subplot(224)
    plt.plot((sizes), (avgs), ':', label='average')
    plt.legend()
    timestamp = int(time.time())

    create_dir()

    plt.savefig('load_testing_plots/{0}'.format(timestamp))
