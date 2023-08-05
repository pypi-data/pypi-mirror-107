from typing import List, Union
import click


@click.command()
@click.argument('data', nargs=-1, required=True)
def selection_sort(data: List[Union[int, float]]) -> List[Union[int, float]]:
    data = [int(i) for i in data if i != '']
    for i in range(len(data)):
        low = i
        for j in range(i + 1, len(data)):
            if data[j] < data[low]:
                low = j
        data[low], data[i] = data[i], data[low]
    return data


if __name__ == "__main__":
    selection_sort()
