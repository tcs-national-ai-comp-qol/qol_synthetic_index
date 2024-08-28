# QoL Index

## Files overview

  - `synthesizing_pol.py` contains the main program to generate QoL index by calling `gemini-1.5-pro`
  - `qol_data_validator.py` validates the output using the provided JSON schema
  - `qol_combine.py` merges the generated QoL with ED census data
  - `ed_dataset` contains gz compressed csv for ED census data
  - `qol_dataset` contains the generated JSON as tar gz
  - `combined_dataset` contains the merged csv in gz

