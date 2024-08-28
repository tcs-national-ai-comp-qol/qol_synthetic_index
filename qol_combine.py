import csv
import json
import gzip
from pathlib import Path

import fire

ED_DATA_DIR = Path("ed_dataset").glob("*.csv.gz")
ED_DATA_FORMAT = "csv"

QOL_DATA_DIR = Path("qol_dataset").glob("*.json")
QOL_DATA_FORMAT = "json"

OUTPUT_DIR = Path("combined_dataset") / "irl_ed_qol.csv"
OUTPUT_FORMAT = "csv"

field_names = [
    "QoL", 
    "a_sense_of_control:cost_of_living", 
    "a_sense_of_control:essential_services", 
    "a_sense_of_control:influence_and_contribution", 
    "a_sense_of_control:safety", 
    "a_sense_of_wonder:distinctive_design_and_culture", 
    "a_sense_of_wonder:play_and_recreation", 
    "connected_communities:belonging", 
    "connected_communities:local_business_and_jobs", 
    "connection_to_nature:biodiversity", 
    "connection_to_nature:climate_resilience_and_adaptation", 
    "connection_to_nature:green_and_blue_spaces", 
    "getting_around:car", 
    "getting_around:public_transport", 
    "getting_around:walking_and_cycling", 
    "health_equity:air_noise_light", 
    "health_equity:food_choice", 
    "health_equity:housing_standard",
    ]

def flatten_qol_data(qol_data):
    flattened_data = []
    for qol_record in qol_data:
        flattened = {}
        flattened["QoL"] = qol_record["answer"]["QoL"]
        flattened["a_sense_of_control:cost_of_living"] = qol_record["answer"]["a_sense_of_control"]["cost_of_living"]
        flattened["a_sense_of_control:essential_services"] = qol_record["answer"]["a_sense_of_control"]["essential_services"]
        flattened["a_sense_of_control:influence_and_contribution"] = qol_record["answer"]["a_sense_of_control"]["influence_and_contribution"]
        flattened["a_sense_of_control:safety"] = qol_record["answer"]["a_sense_of_control"]["safety"]
        flattened["a_sense_of_wonder:distinctive_design_and_culture"] = qol_record["answer"]["a_sense_of_wonder"]["distinctive_design_and_culture"]
        flattened["a_sense_of_wonder:play_and_recreation"] = qol_record["answer"]["a_sense_of_wonder"]["play_and_recreation"]
        flattened["connected_communities:belonging"] = qol_record["answer"]["connected_communities"]["belonging"]
        flattened["connected_communities:local_business_and_jobs"] = qol_record["answer"]["connected_communities"]["local_business_and_jobs"]
        flattened["connection_to_nature:biodiversity"] = qol_record["answer"]["connection_to_nature"]["biodiversity"]
        flattened["connection_to_nature:climate_resilience_and_adaptation"] = qol_record["answer"]["connection_to_nature"]["climate_resilience_and_adaptation"]
        flattened["connection_to_nature:green_and_blue_spaces"] = qol_record["answer"]["connection_to_nature"]["green_and_blue_spaces"]
        flattened["getting_around:car"] = qol_record["answer"]["getting_around"]["car"]
        flattened["getting_around:public_transport"] = qol_record["answer"]["getting_around"]["public_transport"]
        flattened["getting_around:walking_and_cycling"] = qol_record["answer"]["getting_around"]["walking_and_cycling"]
        flattened["health_equity:air_noise_light"] = qol_record["answer"]["health_equity"]["air_noise_light"]
        flattened["health_equity:food_choice"] = qol_record["answer"]["health_equity"]["food_choice"]
        flattened["health_equity:housing_standard"] = qol_record["answer"]["health_equity"]["housing_standard"]
        flattened["Electoral Divisions"] = qol_record["query"]
        flattened_data.append(flattened)
    return flattened_data

def combine_data(ed_data, qol_data):
    combined_data = []
    qol_data_dict = {qol["Electoral Divisions"]: {key:value for key, value in qol.items() if key != "Electoral Divisions"} for qol in flatten_qol_data(qol_data)}
    ed_data_dict = {ed["Electoral Divisions"]: {key:value for key, value in ed.items() if key != "Electoral Divisions"} for ed in ed_data}
    assert len(set(qol_data_dict.keys()) - set(ed_data_dict.keys())) == 0, f"All EDs in qol_data must also be in ed_data, but found difference: {set(qol_data_dict.keys()) - set(ed_data_dict.keys())}"
    for ed_row in ed_data:
        ed_id = ed_row["Electoral Divisions"]
        qol_row = qol_data_dict.get(ed_id)
        assert qol_row is not None, f"No QoL data found for {ed_id}"
        combined_data.append({**ed_row, **qol_row})
    return combined_data


def read_data(data_dir, data_format):
    result_data = []
    if data_format == "csv":
        for file in data_dir:
            with gzip.open(file, "rt") as f:
                reader = csv.DictReader(f)
                result_data.extend(reader)
    elif data_format == "json":
        for file in data_dir:
            with open(file, "r") as f:
                result_data.extend(json.load(f))
    print(f"Read {len(result_data)} rows of data in {data_format} from {data_dir}")
    return result_data


def write_data(data, output_dir: Path):
    # write csv
    print(f"Writing data of length {len(data)} to {output_dir}")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with open(output_dir, "w") as f:
        w = csv.DictWriter(f, fieldnames=data[0].keys())
        w.writeheader()
        for row in data:
            w.writerow(row)


def main():
    ed_data = read_data(ED_DATA_DIR, ED_DATA_FORMAT)
    qol_data = read_data(QOL_DATA_DIR, QOL_DATA_FORMAT)
    combined_data = combine_data(ed_data, qol_data)
    write_data(combined_data, OUTPUT_DIR)


fire.Fire(main)
