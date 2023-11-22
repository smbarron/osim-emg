"""Functions to combine the outputs of SO into a single file for use in JRA tool."""
import pandas as pd


def combine_files(states_file_path: str) -> str:
    """Wrapper to insert the measured activations into the states file and save it."""
    states_df = load_states_file(states_file_path)

    activation_file_path = states_file_path.replace("StatesReporter_states", "StaticOptimization_activation")
    activation_df = load_activation_file(activation_file_path)

    output_filename = states_file_path.replace("StatesReporter_states", "CombinedFile")

    combined_df = merge_files(activation_df, states_df)
    save_combined_file(combined_df, output_filename)

    return output_filename


def load_activation_file(filename: str) -> pd.DataFrame:
    """Load the activation file as a pandas dataframe."""
    return pd.read_table(filename, skiprows=8, header=0, delimiter="\t")


def load_states_file(filename: str) -> pd.DataFrame:
    """Load the states file as a pandas dataframe."""
    return pd.read_table(filename, skiprows=12, header=0, delimiter="\t")


def merge_files(activations: pd.DataFrame, states: pd.DataFrame) -> pd.DataFrame:
    """Merge the activations and states."""
    activation_columns = [col for col in activations.columns if not col.endswith("_res") and col != "time"]
    states_columns_to_replace = [f"/forceset/{col}/activation" for col in activation_columns]

    combined_df = states.copy()

    for act_col, state_col in zip(activation_columns, states_columns_to_replace):
        if state_col in combined_df.columns:
            combined_df[state_col] = activations[act_col]

    return combined_df


def save_combined_file(data: pd.DataFrame, filename: str):
    """Add the OpenSim header to the combined states file and save it."""
    with open(filename, "w") as f:
        f.write("ModelStates\n")
        f.write("version=1\n")
        f.write(f"nRows={len(data)}\n")
        f.write(f"nColumns={len(data.columns)}\n")
        f.write("inDegrees=no\n")
        f.write("\n")
        f.write("This file contains the states of a model during a simulation.\n")
        f.write("\n")
        f.write("Units are S.I. units (second, meters, Newtons, ...)\n")
        f.write("If the header above contains a line with 'inDegrees', this indicates whether rotational values are in degrees (yes) or radians (no).\n")
        f.write("\n")
        f.write("endheader\n")

    data.to_csv(filename, mode="a", sep="\t", index=False, float_format="%.8f")
