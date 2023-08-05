import click
from tests.Generator import gen_data
from tests.Time import measure_times, create_graph


@click.group()
def main():
    pass


@main.command()
@click.option('--start', type=int, default=1)
@click.option('--end', type=int, default=10)
@click.option('--step', type=int, default=1)
@click.option('--count', type=int, default=1)
def generate_data(start: int, end: int, step: int, count: int):
    if start > end:
        print('Чел ты херню ввёл')
    else:
        gen_data(start, end, step, count)


@main.command()
# Вот здесь КАРОЧ напишите название сортировки quick_sort or counting_sort
@click.option('--name_sort', type=str, default='quick_sort')
def measure_time(name_sort: str):
    #  ДА НУ ИДИ ТЫ НАФИГ КАКИЕ ЕЩЁ ЭКСТРА АРГУМЕНТЫ НЕОЖИДАННЫЕ, ТАМ ВСЁ ВПОЛНЕ ОЖИДАЕМО БЫЛО
    try:
        measure_times(name_sort)
    except Exception as e:
        print(e)
        print('Ладно давай я тебе проще скажу, посмотри на то что ты ввёл сюда')


@main.command()
@click.option('--file', type=str, default='1621659210')
def create_chart(file: str):
    try:
        create_graph(file)
    except Exception as e:
        print(e)
        print('Ладно давай я тебе проще скажу, посмотри на то что ты ввёл сюда')


if __name__ == '__main__':
    main()
