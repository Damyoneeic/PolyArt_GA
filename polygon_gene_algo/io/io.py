import csv
import json
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r") as config_file:
        return json.load(config_file)


def write_json(path: str, config_data: Dict[str, Any]) -> None:
    with open(path, "w") as new_config_file:
        json.dump(config_data, new_config_file, indent=4)


def write_csv(path: str, data_list: List[List[Any]]) -> None:
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data_list)


def plot_fitness_csv(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    fig, ax = plt.subplots()
    ax.plot(df.iloc[:, 1], np.sqrt(df.iloc[:, 0]))
    ax.set_xlabel("cycle")
    ax.set_ylabel("fitness rmse")

    ticks = df.iloc[::10, 1].tolist()
    ax.set_xticks(ticks)

    labels = [
        f"{cycle}\n({val})" for cycle, val in zip(df.iloc[::10, 1], df.iloc[::10, 2])
    ]
    ax.set_xticklabels(labels)

    plt.savefig(f"{output_path}/fitness_plot.png")
    plt.close(fig)
