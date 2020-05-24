![Solution verification](https://github.com/dungNV3/OR-Project-Ortec/workflows/Solution%20verification/badge.svg)

# OR-Project-Ortec

Repository for the OR Lab 2020

# Using the algorithm

Run it by calling `python run.py /path/to/instance.yaml /output_name.yaml`

Parameters are set in `config.py`

For fast runtime bypass the tree search (exchange this: `            packed_block = search_block(packState, candidate_list, block_list, available_items)`with this: `packed_block = candidate_list[0]`)

# Using the CI

The CI automatically generates solutions based on the instances given in `.github/workflows/main.yml`. They are stored as artifacts.
