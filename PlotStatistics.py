import matplotlib.pyplot as plt
import time
import datetime
import csv
import numpy as np

from StatisticsManager import StatisticsManager


def plot_bar_x(labels, y, title, xlabel, ylabel):
    # this is for plotting purpose
    index = np.arange(len(labels))
    plt.bar(index, y)
    plt.xlabel(xlabel, fontsize=7)
    plt.ylabel(ylabel, fontsize=7)
    plt.xticks(index, labels, fontsize=6, rotation=30)
    plt.title(title)
    plt.show()


def duration2msstring(num):
    minutes = int(num)
    seconds = int((num - minutes) * 60.0)
    return "%dm%ds" % (minutes, seconds)


def plot_winningGames(datas):
    x, y = [], []
    for d in datas:
        if d[2] <= 1 and d[3] == 21:
            x.append(d[0])
            y.append(d[4] / 60.0)  # minutes
    _avg = duration2msstring(sum(y) / len(y))
    _min = duration2msstring(min(y))
    _max = duration2msstring(max(y))
    title = "Winned games: %d. Avg: %s, Max: %s, Min: %s" % (len(y), _avg, _max, _min)
    plot_bar_x(x, y, title, 'Date', 'Duration (minutes)')


def plot_allGames(datas):
    x, y = [], []
    for d in datas:
        if d[2] <= 1 and d[3] != 0:
            x.append(d[0])
            y.append(d[3])
    _avg = "%d" % (sum(y) / len(y))
    _min = "%d" % min(y)
    _max = "%d" % max(y)
    title = "Level reached for all games: %d. Avg: %s, Max: %s, Min: %s" % (len(y), _avg, _max, _min)
    plot_bar_x(x, y, title, 'Date', 'Level arrived (number)')


def main():
    manager = StatisticsManager()
    plt.figure('Bot played games statistics')
    datas = manager._readAll()
    plot_winningGames(datas)
    plot_allGames(datas)


if __name__ == '__main__':
    main()
