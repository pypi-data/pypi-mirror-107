import random
import os
from math import inf

"""
Функция должна работать по принципу функции range, принимая параметры start, end, step. 
Эти параметры обозначают размеры нагрузочных тестов. 
В дополнении к этому функция должна принимать параметр count - 
сколько разных нагрузочных тестов одного размера нужно сгенерировать. 

Пример использования - generate(start=1, end=22, step=10, count=5) -
генерирует 5 нагрузочных тестов с размером данных 1, 5 нагрузочных тестов с размером данных 11, 5 нагрузочных тестов 
с размером данных 21.

R.D Вы можете сделать кол-вом (которое фигурирует в задании) кол-во вершин в графе, а рёбра рандомно выставлять
"""


# название файлов РАЗМЕР_НОМЕР.РАСШИРЕНИЕ


def generate_data(start: int, end: int, step: int, count: int):
    for i in range(start, end, step):
        for j in range(1, count + 1):
            with open(f'load_testing_data/{i}_{j}.txt', 'w') as file:
                count_of_verts = random.randint(start, i)
                count_of_edges = random.randint(start, end)
                adjacency_matrix = [['inf' for _ in range(count_of_verts)] for _ in range(count_of_verts)]
                for y in range(count_of_edges):
                    vert1 = random.randint(1, count_of_verts)
                    vert2 = random.randint(1, count_of_verts)
                    weight = random.randint(start, end)
                    adjacency_matrix[vert1 - 1][vert2 - 1] = weight

                for q in range(count_of_verts):
                    adjacency_matrix[q][q] = 0

                file.write(str(adjacency_matrix))

                # adjacency_matrix = [[ 0,   3,  inf,  5 ],
                #                     [ 2,   0,  inf,  4 ],
                #                     [inf,  1,   0,  inf],
                #                     [inf, inf,  2,   0 ]]


def main():
    try:
        os.mkdir('load_testing_data')
    except OSError:
        pass

    start = int(input('start: '))
    end = int(input('end: '))
    step = int(input('step: '))
    count = int(input('count: '))

    generate_data(start, end, step, count)


if __name__ == '__main__':
    main()
