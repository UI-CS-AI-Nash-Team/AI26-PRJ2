# AI projrct #2 - THE LAST SIGNAL 
## *A Local Seach project*

## The Story...

in the year 2145, following a series of of solar stroms and larg-scale syberattacs, much of Erth's communication infrastructure has been destroyed. the remaining cities relay on network of intelligent sensors for survival which they responsible is detecting energy resouces, identifing dangerious area, tracing vital signals, and maintaining communication between bases, However is a magor problem, the number of sensors is limited and operational environments are complex. Some regions contain impossable obtacles, while other areas include critical targets that must be covered at all costs.

You are a member of an autonomous systems design team. Your task is to develop an intelligent algorithm for sensor placement in the environment in order to:

- Maximize the number of covered targets
- Optimize network coverage
- Utilize limited resources in the most efficient way possible

## Overview

in this project we learn about **Local Searh** algorithms specially about:

- **Hill Climbing**
- **Simulated Annealing**

The objective of this project is to solve an optimization problem in a **Grid World** environment. Using **Local Search** algorithms, you must determine the optimal number and placement of sensors in order to maximize the coverage of targets within the environment while efficiently utilizing system resources.

In addition to implementing the algorithms, this project also involves analyzing the behavior of the algorithms, designing a cost function, designing a **Neighbor Function**, and comparing the performance of different methods.

## Requirements

To run the environment, you need to install the following libraries:

- pygame
- numpy
- matplotlib

## Environment

The project environment is a two-dimensional grid world of size **m × n**, consisting of targets, obstacles, and sensors.

The agent’s objective is to find the optimal locations for placing the sensors in order to maximize the coverage of targets.

### Environment Components:

- **Sensors**: Blue circular points. The agent can place a number of sensors (up to the specified limit for each map) within the environment. Each sensor has a specific range and can cover nearby targets.
- **Targets**: Red squares. The main objective of the project is to cover the maximum number of targets.
- **Obstacles**: Gray squares. Placing sensors on these cells is not allowed.
**Empty Cells**: Sensors can be placed on these cells.

## Implementation

To simplify the implementation of the algorithms, a large part of the environment has already been implemented.

The following functions are available for interacting with the environment:

1. `is_valid_position(x, y) -> bool`
   Checks whether the specified coordinates:

   * are inside the environment
   * are not located on an obstacle

2. `get_targets() -> list`
   Returns the positions of all targets.

3. `random_position(world) -> tuple`
   Generates a random valid position within the environment.

In addition, you have access to the variables `grid`, `sensor_range`, `max_sensors`, `rows`, and `cols`, which respectively represent:

* the overall map of the environment,
* the monitoring radius of each sensor,
* the maximum number of sensors available,
* the number of rows in the environment,
* and the number of columns in the environment.

### What You Need to Implement:

You are required to implement all logic related to the following algorithms:

* Hill Climbing
* Simulated Annealing
* Other algorithms (optional / bonus section)

You are also responsible for implementing the helper functions required by these algorithms, such as:

* generating neighbors,
* computing the cost function,
* and any other necessary utility functions.

Note that in the starter code, the `local_search_base` class serves as the parent class for all local search classes. You may implement shared functions within this class.

**Important Note**: Designing the Neighbor Function is considered an important part of the project. Your neighborhood design is expected to include operations such as:

- moving a sensor,
- adding a sensor,
- and removing a sensor.

## Environment Constraints

* Sensors must not be placed on obstacles.
* Sensors must be located within the boundaries of the environment.
* The number of sensors may vary, but it must not exceed the `max_sensors` value specified for each map.

## Environment Scoring System

After executing each algorithm, a report is displayed in the terminal containing:

* the name of the algorithm,
* the final cost (the implementation of the cost function is entirely your responsibility),
* and the best state.

In addition, a visual report showing:

* the trend of cost changes,
* and the number of iterations

will also be displayed.

**Note**: Students are not required to modify the visualization system.

## Algorithm Output

Each algorithm must return the following outputs:

* `best_state`
* `best_cost`
* `evaluations`
* `states_history`

### Output Descriptions

| Output           | Description                                                                    |
| ---------------- | ------------------------------------------------------------------------------ |
| `best_state`     | The best sensor arrangement, including the number and positions of the sensors |
| `best_cost`      | The best cost value                                                            |
| `evaluations`    | The trend of cost changes during execution                                     |
| `states_history` | The history of visited states                                                  |

## How to Run

Check the `main.py` file. This file sets up the environment and executes your algorithms.

Your algorithms should be implemented in the `/search` directory.

Different maps are located in the `/env/maps` directory.

## Algorithm Evaluation Criteria

Note that designing the Neighbor Function is considered an important part of the project, and the neighborhood design is expected to include operations such as:

* moving a sensor,
* adding a sensor,
* and removing a sensor.

The following criteria will be considered during evaluation:

* quality of the final solution,
* ability to escape local optima,
* convergence speed,
* performance on different maps,
* proper design of the evaluation function,
* and effective management of the trade-off between coverage quality and the number of sensors.

## Expected Analysis

The project report should include analysis of the following topics:

* the differences between the algorithms you implemented,
* the effect of each algorithm’s parameters,
* the Local Optimum problem,
* the behavior of the algorithms on different maps,
* the quality of the Neighbor Function,
* and the effect of add/remove sensor operations on search quality.

## Additional Features (Bonus)

Implementing the following algorithms will be considered bonus work:

* Genetic Algorithm
* Beam Search
* Tabu Search
