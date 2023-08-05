import time
import os
import re
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tragic_semester_work_2.quicksort import quicksort
from tragic_semester_work_2.counts_sort import SimpleCountingSort
from collections import defaultdict
import csv
from pathlib import Path


# Принимает название сортировки
def measure_times(pathing):
    os.makedirs('./tragic_semester_work_2/load_testing_measurements', exist_ok=True)
    if pathing == 'quick_sort':
        sort_func = quicksort
    elif pathing == 'counting_sort':
        sort_func = SimpleCountingSort
    else:
        print('ТЫ ЧО ВВЁЛ, А?')
        return

    dict_sheets = defaultdict(list)
    list_txt_name = os.listdir(Path("tragic_semester_work_2") / 'load_testing_data')

    for index in range(len(list_txt_name)):
        # Достаём размерность массива и номер массива\
        list_txt = re.split('[_.]', list_txt_name[index][:])
        current_size, number_test = list_txt[0], list_txt[1]

        with open(Path("tragic_semester_work_2") / 'load_testing_data' / f'{current_size}_{number_test}.txt') as file:
            a = file.read()
            arr = [int(num) for num in a.split()]

        start = time.time()
        sort_func(arr)
        end = time.time() - start
        dict_sheets[current_size].append(end)
    return dict_creation(dict_sheets)


# Делает csv файл
def dict_creation(dict_sheets):
    name = int(datetime.datetime.now().timestamp())
    with open(Path("tragic_semester_work_2") / 'load_testing_measurements' / f'{name}.csv', mode='a',
              encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow(["size", "min", "max", "avg", "median"])
    for key, value in dict_sheets.items():
        mas = sorted(value[:])
        with open(Path("tragic_semester_work_2") / 'load_testing_measurements' / f'{name}.csv', mode="a",
                  encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow([key, mas[0], mas[-1], sum(i for i in mas) / len(mas), mas[len(mas) // 2]])

    return name


# Рисуем график
def create_graph(csv_file_path: str):
    try:
        os.makedirs('./tragic_semester_work_2/load_testing_plots', exist_ok=True)
        data = pd.read_csv(Path("tragic_semester_work_2") / 'load_testing_measurements' / f"{csv_file_path}.csv")
        data.set_index("size", inplace=True)
        data.head()
        data.plot()
        plt.savefig(
            Path("tragic_semester_work_2") / 'load_testing_plots' / f'{int(datetime.datetime.now().timestamp())}.jpg')
    except Exception as e:
        print(e)
        print('Кароч, он тебе там какую-то хрень написал наверное. Я так думаю, что ты просто послушал, то что я '
              'говорил тебе и написал фигню, чтобы график не строился. Красавчик!👍')


def main():
    path = input('quick_sort or counting_sort\n')
    name_csv = measure_times(path)
    create_graph(str(name_csv))
    # output_dict = measure_time(path)
    # dict_creation(output_dict)
    # path_csv = input('Если хотите увидеть график, то введите сюда название файлика csv без .csv '
    #                  'А если не хотите, ну это ваши проблемы, напишите сюда какую-то хрень\n')
    # create_chart(path_csv)


if __name__ == '__main__':
    main()
