![Solution verification](https://github.com/dungNV3/OR-Project-Ortec/workflows/Solution%20verification/badge.svg)

# OR-Project-Ortec

Repository for the OR Lab 2020 @ ORTEC

# Using the algorithm

Run our solution by calling `python3 run.py -I /path/to/instance.yaml -S /output_name.yaml -R runtime`

`runtime` (seconds as integer) is a direction how long the algorithm should seek for a solution. The acutal runtime can be slightly longer, since the algorithm always completes the current progress to a valid solution.

You can find configurable parameters in `./config.py` (along with explanations). Ideally, these are adjusted so that the maximum runtime (given by parameter) is higher than the actual runtime.

# Using the CI

The CI automatically generates solutions based on the instances given in `.github/workflows/main.yml`. They are stored as artifacts. Furthermore, one can find the execution time, utilization and average utilization in the Action Tab.
