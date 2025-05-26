import os
import time

import cv2

from . import io, run_ga


def main() -> None:
    start_time = time.time()

    parameters = io.load_config("./config/config.json")
    img = cv2.imread(f"input/{parameters['input_name']}")
    if img is None:
        raise ValueError(f"could not read image: input/{parameters['input_name']}")
    w, h = parameters["width_height"]
    img = cv2.resize(img, (w, h))
    output_path = f"./output/{parameters['name']}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    cv2.imwrite(f"{output_path}/goal_image.jpg", img)
    img_created, fitness_list = run_ga.run_ga(img, parameters)
    io.write_json(f"./output/{parameters['name']}/config_saved.json", parameters)
    io.write_csv(f"./output/{parameters['name']}/cycle_fitness.csv", fitness_list)
    io.plot_fitness_csv(
        f"./output/{parameters['name']}/cycle_fitness.csv",
        f"./output/{parameters['name']}/",
    )

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"time taken: {execution_time} seconds")

    pass


if __name__ == "__main__":
    # after checking config and input file
    # run with
    # caffeinate python3 -m polygon_gene_algo
    main()
