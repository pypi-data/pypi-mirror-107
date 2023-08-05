import os
import shutil
import random


def create_dir():
    if os.path.exists("load_testing_data"):
        shutil.rmtree("load_testing_data")
    os.mkdir("load_testing_data")


def generate_data(start: int, end: int, step: int, count: int):
    create_dir()

    def tests_generate(size, count):

        def string_generation(size) -> str:
            string = ''
            for i in range(size):
                string += chr(random.randint(97, 122))
            return string

        for i in range(count):
            string1 = string_generation(size)
            string2 = ''
            if random.randint(0, 1):
                string2 = string1
            else:
                string2 = string_generation(size)

            with open('load_testing_data/{0}_{1}.txt'.format(size, i), 'w') as f:
                f.write(string1 + '\n')
                f.write(string2)

    for i in range(start, end, step):
        tests_generate(i, count)
