# Data Directory Structure

This directory contains all the data files used in the disease outbreaks analysis project.

## Directory Structure

- `raw/`: Contains the original, immutable data dump
  - Contains raw news headlines and unprocessed data files
  - `headlines.txt` - Raw news headlines data

- `processed/`: Contains the cleaned and processed data ready for analysis
  - Will contain processed datasets generated during analysis
  - Intermediate results and transformed data

## Data Handling Guidelines

1. Never modify the raw data files directly
2. Store processed data in the appropriate subdirectory
3. Document any data transformations in the analysis notebooks
4. Keep large data files out of version control (see .gitignore)
