from random import randint
import os
import shutil
import threading
import click


@click.command()
@click.option('--start', type=int, default=1)
@click.option('--end', type=int, default=10)
@click.option('--step', type=int, default=1)
@click.option('--count', type=int, default=1)
def generate_data(start: int, end: int, step: int, count: int):
    if os.path.isdir("load_testing_data"):
        shutil.rmtree("load_testing_data", ignore_errors=True)

    os.mkdir('load_testing_data')
    os.chdir('load_testing_data')

    for i in range(start, end, step):
        for j in range(count):
            file = open(f"{i}_{j}.txt", 'w')
            create_in_time = threading.Thread(target=create_test, args=(file, i))
            create_in_time.start()
            create_in_time.join()


def create_test(file, range_i):
    for k in range(range_i):
        file.write(f'{randint(-1, 15000)} ')


if __name__ == '__main__':
    generate_data()
