import os
import time
import csv
import ast
import math
from .main import floyd_warshall
import pandas as pd
import matplotlib.pyplot as plt
# %pylab inline


def avg(numbers: list) -> float:
    return float(sum(numbers)) / max(len(numbers), 1)


def median(lst: list) -> int:
    return sorted(lst)[len(lst) // 2]


def file_correction(lst: list) -> list:
    for q in range(len(lst)):
        for e in range(len(lst[0])):
            if lst[q][e] == 'inf':
                lst[q][e] = math.inf
    return lst


def measure_time():
    test_file = os.listdir(path='load_testing_data/')
    result = []
    mini = math.inf
    maxi = 0.0
    with open(f'load_testing_measurements/{time.time()}.csv', 'w') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(['size', 'min', 'max', 'avg', 'median'])
        for i in sorted(test_file, key=lambda x: int(x[:-4])):
            with open(f'load_testing_data/{i}', 'r') as file:
                lst = file_correction(ast.literal_eval(file.read()))
                start = time.time()
                floyd_warshall([lst])
                end = time.time() - start
                result.append(end)
                maxi = max(maxi, end)
                mini = min(mini, end)
                writer.writerow([i, mini, maxi, avg(result), median(result)])
                print('finish:', i)



def draws_graph(name_file):
    data = pd.read_csv(f"load_testing_measurements/{name_file}.csv")
    data.set_index("size", inplace=True)
    data.head()
    data.plot()
    plt.show()


def main():
    try:
        os.mkdir('load_testing_measurements')
    except OSError:
        pass

    name_file = time.time()

    measure_time()

    # draws_graph(name_file)


if __name__ == "__main__":
    main()
