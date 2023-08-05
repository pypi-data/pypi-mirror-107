from math import inf


def input_adjacency_matrix():
    count_of_verts = int(input('Введите количество вершин в графе: '))
    adjacency_matrix = [[inf for _ in range(count_of_verts)] for _ in range(count_of_verts)]
    for i in range(count_of_verts):
        adjacency_matrix[i][i] = 0
    count_of_edges = int(input('Введите количество ребер в графе: '))
    for _ in range(count_of_edges):
        greeting = 'Введите через пробел - номер первой вершины, номер второй вершины, вес ребра: '
        vert1, vert2, weight = map(int, input(greeting).split())
        adjacency_matrix[vert1 - 1][vert2 - 1] = weight
    # adjacency_matrix = [[ 0,   3,  inf,  5 ],
    #                     [ 2,   0,  inf,  4 ],
    #                     [inf,  1,   0,  inf],
    #                     [inf, inf,  2,   0 ]]
    return adjacency_matrix


def floyd_warshall(adjacency_matrix):
    distance = [line.copy() for line in adjacency_matrix]
    verts = list(range(len(adjacency_matrix)))
    pred = [[-1 for _ in verts] for _ in verts]
    for u in verts:
        for neighbor in verts:
            if 0 != adjacency_matrix[u][neighbor] != inf:
                pred[u][neighbor] = u  # ребро u -> neighbor существует
    for k in verts:
        for i in verts:
            for j in verts:
                new_dist = distance[i][k] + distance[k][j]
                if new_dist < distance[i][j]:
                    distance[i][j] = new_dist
                    pred[i][j] = pred[k][j]
    return distance, pred


def path(vert1, vert2, pred_dict):
    path_to_vert = [vert2]
    from_vert = pred_dict[vert2]
    while from_vert != -1:
        path_to_vert = [from_vert] + path_to_vert
        from_vert = pred_dict[from_vert]
    if path_to_vert[0] != vert1:
        return 'Путь отсутствует'
    return ' -> '.join(str(vert + 1) for vert in path_to_vert)


def print_solution(distance, pred):
    print('Кратчайшие пути:')
    for vert1 in range(len(distance)):
        for vert2 in range(len(distance)):
            if vert1 != vert2:
                print(f'{vert1 + 1} -> {vert2 + 1} (вес {distance[vert1][vert2]}):',
                      path(vert1, vert2, pred[vert1]))


def main():
    adjacency_matrix = input_adjacency_matrix()
    print_solution(*floyd_warshall(adjacency_matrix))


if __name__ == '__main__':
    main()
