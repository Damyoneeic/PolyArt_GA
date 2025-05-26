# Polygon Art Genetic Algorithm (PolyArt_GA)

## Features

* **Genetic Algorithm** based evolutionary optimization
* **Configurable** via `config/config.json` (generations, population size, mutation/crossover rates, etc.)
* **I/O Utilities**: JSON/CSV/PNG support for loading configs and saving results

## Directory Structure

```
├── config
│   └── config_example.json    # Sample configuration
├── input                     # Input data (e.g., target images)
├── output                    # Generated output files
├── polygon_gene_algo
│   ├── io
│   │   └── io.py             # File I/O utilities
│   └── run_ga
│       ├── evolution.py      # GA core implementation
│       └── run_ga.py         # Execution flow
├── pyproject.toml            # Poetry configuration
├── poetry.lock               # Locked dependencies
├── README.md                 # Project overview and instructions
└── LICENSE                   # MIT License text
```

## Installation

Make sure you have [Poetry](https://python-poetry.org/) installed.

```bash
# Clone the repository
git clone https://github.com/Damyoneeic/PolyArt_GA.git
cd polygon_gene_algo_private

# Install dependencies and enter the virtual environment
poetry install
poetry shell
```

##  Configuration

Copy the sample config and adjust parameters as needed:

```bash
cp config/config_example.json config/config.json
```

`widt_height`: The size you want for your proccessed image.

`input_name`: The name for the output dir to store your outputs. The following dir will be created `/output/input_name`.

`threshold`: The threshold to decide when the fitness is enough. The Recommended value is 0 ~ 100.

`polygon_per_cycle`: Number of polygons/circles to place on the canvus per each cycle. Note that each cycle consists  of `num_gen` generations. The total number of polygons is cycle times  polygon_per_cycle.

`num_pop`: Number of population per generation. Recommended value is 25 ~ 50.

`num_step`: Number of steps to decide the radius of the circle. Note that it does not equal to the total number of cycles. See [Algorithm](#algorithm) for more information. Recommended value is roughly 1/4 to 1/4 of height/width.

`mutation_rate`: Mutation rate for each child gene created. Recommended value is 0.01 ~ 0.1.

`cross_rate`: Cross rate for the selected parents.  Recommended value (maybe )is 0.6 ~ 1.

## Usage

Run the GA with your settings:

```bash
poetry run python -m polygon_gene_algo
```

Results will be saved under the `output/` directory. `output_name` is configured under `name` in `config.json`:

* `output_name/cycle_fitness.csv`: Fitness history
* `output_name/config_saved.json`: config parameters used
* `output_name/cyclenumber.jpg`: Generated image per cycle
* `output_name/fitness_plot.png`: Fitness trend plot
* `output_name/goal_image`: Image used as input
  
## Algorithm

The core algorithm follows these stages:

### Canvas Initialization

The canvas starts as a uniform gray image. Subsequent shapes are drawn on top of this base to gradually approximate the target.

### Cycle Loop

For each radius value in radius_list, which typically ranges from large to small:

### Population Initialization

Create an initial population of population_size individuals.

Each individual’s gene encodes polygons_per_cycle shapes, where each shape is defined by five normalized floats: (y, x, b, g, r).

### Generation Evolution

Repeat for num_generations:

`Fitness Evaluation`: Render each individual’s shapes as filled circles on the canvas and compute the mean squared error (MSE) against the target image.

`Elitism`: Retain the top fraction of individuals (as defined by elite_fraction).

`Selection`: Choose parents via roulette-wheel selection weighted by inverse fitness.
`Crossover`: Perform one-point crossover on parent genes with probability crossover_rate.

`Mutation`: Mutate individual genes at random positions with probability mutation_rate.

`Population Update`: Form the next generation from elites and offspring.

### Radius Strategy

radius_list controls the sequence and size of shapes. Larger radii capture broad, coarse features early, while smaller radii refine details in later cycles.

### Gene Representation

A gene is a flat array of floats in [0,1]. For each shape:

`Coordinates`: Two floats (y, x) normalized to [0,1] relative to canvas height and width.

`Color`: Three floats (b, g, r) normalized to [0,1].

The total gene length is 5 × polygons_per_cycle.

### Fitness Function

Fitness is computed as the mean squared error (MSE) between the rendered canvas and the target image

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
