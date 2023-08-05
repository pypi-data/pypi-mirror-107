import click
from common_func import generate_data as gd
from common_func import main as m
from common_func import load_testing_measurements as ms
import os


@click.group()
def main():
    pass

@main.command()
def process_one():
    m.main()

@main.command()
@click.option('--start', default=5)
@click.option('--end', default=22)
@click.option('--step', default=1)
@click.option('--count', default=2)
def generate_data(start: int, end: int, step: int, count: int):
    try:
        os.mkdir('load_testing_data')
    except OSError:
        pass
    gd.generate_data(start, end, step, count)


@main.command()
def measure_time():
    try:
        os.mkdir('load_testing_measurements')
    except OSError:
        pass
    ms.measure_time()


@main.command()
@click.option('--file')
def create_chart(file: str):
    ms.draws_graph(file)


if __name__ =='__main__':
    main()