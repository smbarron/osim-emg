"""Functions to merge measured EMG with results from SO simulations for non-measured muscles."""
import os

import pandas as pd

from osim_emg.activations_to_states import load_activation_file
from osim_emg.constants import EMG_SAMPLING_RATE, MOCAP_SAMPLING_RATE, MUSCLE_MAPPING
from osim_emg.data import COMB_EMG_DATA, SPLIT_EMG_DATA


def save_combined_activations(activation_path, tear):
    activation_data_new = combine_activations(activation_path, tear)
    output_filename = activation_path.replace("activation", "CombinedActivations")

    save_combined_activation_file(activation_data_new, output_filename)

    return output_filename


def add_muscle_to_mapping(muscle_map, tear):
    if not tear:
        muscle_map["Supraspinatus_P"] = "Supraspinatus"
        muscle_map["Supraspinatus_A"] = "Supraspinatus"

    return muscle_map


def downsample_emg(emg_data, emg_frame_rate, mocap_frame_rate):
    sampling_ratio = int(emg_frame_rate / mocap_frame_rate)
    downsampled = emg_data.groupby("Frame").apply(lambda group: group.iloc[::sampling_ratio].mean()).reset_index(drop=True)

    return downsampled


def save_combined_activation_file(df, filename):
    with open(filename, "w") as f:
        f.write("Static Optimization\n")
        f.write("version=1\n")
        f.write(f"nRows={len(df)}\n")
        f.write(f"nColumns={len(df.columns)}\n")
        f.write("inDegrees=no\n")
        f.write("This file contains static optimization results\n")
        f.write("endheader\n")

    df.to_csv(filename, mode="a", sep="\t", index=False, float_format="%.8f")


def combine_activations(activation_path, tear):
    activation_data = load_activation_file(activation_path)

    path_parts = os.path.normpath(activation_path).split(os.sep)
    subject = path_parts[-3]
    trial_full = path_parts[-1]
    trial_index = trial_full[::-1].find("_OS_") + 4
    trial = trial_full[0:-trial_index]

    measured_data = COMB_EMG_DATA[(subject, trial)]
    measured_data_cleaned = pd.concat([SPLIT_EMG_DATA[(subject, trial)][i] for i in range(3)], axis=0)

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
