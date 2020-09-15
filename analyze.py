#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

filer = open('data.txt')
def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

            temp = []
        #temp.append(list(v.values())[0])
        #DFtemp = pandas.DataFrame(temp)
        #print("Temp Median:", Median[0])
        #print("Temp Variance:", Var[0])
        occu = []
    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    data = load_data('data.txt')
    for k in data:
        if k == 'temperature':
            print('')
            print('For lab1:')
            print('')
            print('Temperature Median: ' + str(data[k]['lab1'].median()))
            print('Temperature Variance: ' + str(data[k]['lab1'].var()))
            print('')
        if k == 'occupancy':
            print('Occupancy Median: ' + str(data[k]['lab1'].median()))
            print('Occupancy Variance: ' + str(data[k]['lab1'].var()))
            print('')

            # data[k].plot()
        time = data[k].index
        data[k].hist()
        plt.figure()
        plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        plt.xlabel("Time (seconds)")



    plt.show()
