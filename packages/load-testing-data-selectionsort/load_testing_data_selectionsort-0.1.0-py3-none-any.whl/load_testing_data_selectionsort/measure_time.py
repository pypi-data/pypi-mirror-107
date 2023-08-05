from selection_sort import selection_sort
from typing import List
import time
import csv
import os
import click


def measure_time(generated_list: List[List[List]]):
    for index in range(len(generated_list)):
        count_of_tests = len(generated_list[index])
        values = []

        for i in range(count_of_tests):
            start_time = time.time()
            selection_sort(generated_list[index][i])
            values.append(round((time.time() - start_time) * 1000000))

        size = len(generated_list[index][0]) - 1
        maximum = max(values)
        minimum = min(values)
        average = sum(values) // len(values)
        sort_values = sorted(values)
        medium = sort_values[len(values)//2]

        if not os.path.isdir("load_testing_measurements"):
            os.mkdir("load_testing_measurements")
        with open("load_testing_measurements/UNIX TIMESTAMP.csv", mode='a', encoding="utf-8") as f:
            file_writer = csv.writer(f, delimiter=' ')
            file_writer.writerow([size, maximum, minimum, average, medium])


@click.command()
def read_generated_tests():
    path_to_folder = "load_testing_data"
    lst = os.listdir(path_to_folder)
    all_paths, passed, result = [], [], []

    for i in range(len(lst)):
        size = lst[i].split('_')[0]
        if size not in passed:
            passed.append(size)
            all_paths.append([])
            for path in lst:
                if path.split('_')[0] == size:
                    all_paths[len(passed)-1].append(path)

    for i in range(len(all_paths)):
        result.append([])
        for path in all_paths[i]:
            with open(path_to_folder + '/' + path, 'r') as f:
                result[i].append(f.read().split(' '))

    measure_time(result)


if __name__ == "__main__":
    read_generated_tests()
