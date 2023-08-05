import pandas
import matplotlib.pyplot as plt
import os
import csv
import click


@click.command()
@click.option('--file', type=str)
def create_chart(file: str):
    size, minimum, maximum, average, median = [], [], [], [], []
    minimum_curve, maximum_curve, avr_curve, median_curve = {}, {}, {}, {}

    with open(file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            lst = row[0].split(' ')
            size.append(lst[0])
            minimum.append(lst[1])
            maximum.append(lst[2])
            average.append(lst[3])
            median.append(lst[4])

    for i in range(len(size)):
        minimum_curve[size[i]] = minimum[i]
        maximum_curve[size[i]] = maximum[i]
        avr_curve[size[i]] = average[i]
        median_curve[size[i]] = median[i]

    data_min = pandas.Series(minimum_curve)
    data_max = pandas.Series(maximum_curve)
    data_avr = pandas.Series(avr_curve)
    data_med = pandas.Series(median_curve)

    plt.title("Selection sort")
    plt.plot(data_min, label="minimum")
    plt.plot(data_max, label="maximum")
    plt.plot(data_avr, label="average")
    plt.plot(data_med, label="medium")
    plt.legend()

    if not os.path.isdir("load_testing_plots"):
        os.mkdir("load_testing_plots")
    plt.savefig('load_testing_plots/UNIX TIMESTAMP.jpg')


if __name__ == "__main__":
    create_chart()
