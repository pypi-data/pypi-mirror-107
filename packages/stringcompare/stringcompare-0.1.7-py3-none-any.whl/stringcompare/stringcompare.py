from hashing_search import hashing_search
from linear_search import linear_search
from create_chart import create_chart
from generate_data import generate_data
from measure_time import measure_time

import click


@click.group()
def main():
    pass


@main.command()
@click.option('--data', nargs=2, help='enter 2 strings')
def process1(data):
    data1 = data[0]
    data2 = data[1]
    print(linear_search(data1, data2))


@main.command()
@click.option('--data', nargs=2, help='enter 2 strings')
def process2(data):
    data1 = data[0]
    data2 = data[1]
    print(hashing_search(data1, data2))


@main.command()
@click.option('--start', help='enter START value')
@click.option('--end', help='enter END value')
@click.option('--step', help='enter STEP value')
@click.option('--count', help='enter COUNT value')
def generate(start, end, step, count):
    generate_data(int(start), int(end), int(step), int(count))


@main.command()
@click.option('--func', help='enter func name: linear_search or hashing_search')
def measure_algo(func):
    pass



@main.command()
@click.option('--file', help='enter path to csv table')
def chart(file: str):
    create_chart(file)


if __name__ == '__main__':
    main()
