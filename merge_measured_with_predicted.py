"""Functions to merge measured EMG with results from SO simulations for non-measured muscles."""
import os
import pickle
from typing import Dict, Optional, Union

import pandas as pd

from osim_emg.activations_to_states import load_activation_file
from osim_emg.constants import EMG_SAMPLING_RATE, MOCAP_SAMPLING_RATE, MUSCLE_MAPPING


def save_combined_activations(activation_path: str, split_emg_filepath: str, not_split_emg_filepath: str, tear: Optional[bool]) -> str:
    """Wrapper to combine measured and predicted activations and save them to a file."""
    activation_data_new = combine_activations(activation_path, split_emg_filepath, not_split_emg_filepath, tear)
    output_filename = activation_path.replace("activation", "CombinedActivations")

    save_combined_activation_file(activation_data_new, output_filename)

    return output_filename


def add_muscle_to_mapping(muscle_map: Dict[str, Union[str, None]], tear: Optional[bool]) -> Dict[str, Union[str, None]]:
    """Add muscles to the mapping that are measured but only in the model for participatns without a tear."""
    if not tear:
        muscle_map["Supraspinatus_P"] = "Supraspinatus"
        muscle_map["Supraspinatus_A"] = "Supraspinatus"

    return muscle_map


def downsample_emg(emg_data: pd.DataFrame, emg_frame_rate: int, mocap_frame_rate: int) -> pd.DataFrame:
    """Downsample the EMG data to the same frequency as the motion capture data."""
    sampling_ratio = int(emg_frame_rate / mocap_frame_rate)
    downsampled = emg_data.groupby("Frame").apply(lambda group: group.iloc[::sampling_ratio].mean()).reset_index(drop=True)

    return downsampled


def save_combined_activation_file(data: pd.DataFrame, filename: str):
    """Add the OpenSim header to the combined activation file and save it."""
    with open(filename, "w") as f:
        f.write("Static Optimization\n")
        f.write("version=1\n")
        f.write(f"nRows={len(data)}\n")
        f.write(f"nColumns={len(data.columns)}\n")
        f.write("inDegrees=no\n")
        f.write("This file contains static optimization results\n")
        f.write("endheader\n")

    data.to_csv(filename, mode="a", sep="\t", index=False, float_format="%.8f")


def load_emg_data(split_filepath: str, notsplit_filepath: str):
    """Load the measured EMG data from pickle files."""
    with open(split_filepath, "rb") as file:
        split_emg_data = pickle.load(file)
    with open(notsplit_filepath, "rb") as file:
        comb_emg_data = pickle.load(file)

    return split_emg_data, comb_emg_data


def combine_activations(activation_path: str, split_emg_filepath: str, not_split_emg_filepath: str, tear: Optional[bool]) -> pd.DataFrame:
    """Load the measured and predicted activations and combine them."""
    activation_data = load_activation_file(activation_path)

    path_parts = os.path.normpath(activation_path).split(os.sep)
    subject = path_parts[-3]
    trial_full = path_parts[-1]
    trial_index = trial_full[::-1].find("_OS_") + 4
    trial = trial_full[0:-trial_index]

    split_emg_data, comb_emg_data = load_emg_data(split_emg_filepath, not_split_emg_filepath)
    measured_data = comb_emg_data[(subject, trial)]
    measured_data_cleaned = pd.concat([split_emg_data[(subject, trial)][i] for i in range(3)], axis=0)

    merged = measured_data.where(measured_data_cleaned.notnull())
    merged_new = merged.dropna(axis=0, how="all")

    merged_2 = pd.DataFrame()
    for col in measured_data.columns:
        if not merged_new.isnull().any()[col]:
            merged_2[col] = measured_data[col]
        else:
            merged_2[col] = merged[col]

    downsampled = downsample_emg(merged_2, EMG_SAMPLING_RATE, MOCAP_SAMPLING_RATE)

    muscle_map = add_muscle_to_mapping(MUSCLE_MAPPING, tear)
    activation_data_new = pd.DataFrame()
    for key in muscle_map.keys():
        if muscle_map[key]:
            if downsampled[muscle_map[key]].notnull().all():
                activation_data_new[key] = downsampled[muscle_map[key]]
            else:
                activation_data_new[key] = activation_data[key]
        else:
            activation_data_new[key] = activation_data[key]

    return activation_data_new
