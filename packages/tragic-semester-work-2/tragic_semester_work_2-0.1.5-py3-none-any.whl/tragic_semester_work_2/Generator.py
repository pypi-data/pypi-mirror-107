import os
from random import randint
import multiprocessing


def generate_combination(start, end, step, count):
    for i in range(start, end, step):
        for j in range(count):
            yield i, j


def gen_data(start: int, end: int, step: int, count: int):
    os.makedirs('./tragic_semester_work_2/load_testing_data', exist_ok=True)
    for i in range(start, end, step):
        with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
            p.starmap(writing, generate_combination(start, end, step, count))


def writing(i, j):
    with open(f'./tragic_semester_work_2/load_testing_data/{i}_{j + 1}.txt', 'w') as file:
        mass = [randint(-10000000, 100000000) for _ in range(i)]
        for number in mass:
            file.write(f'{number} ')


def main():
    a = [int(i) for i in input().split()]
    gen_data(a[0], a[1], a[2], a[3])

    # a[0] - start - a[0] + a[1] - здесь мы ходим и номер каждого шага обозначает кол-во элементов в нашем массиве
    # a[1] - end
    # a[2] - step
    # a[3] - count - количество массивов на каждой ступеньке


if __name__ == '__main__':
    main()
