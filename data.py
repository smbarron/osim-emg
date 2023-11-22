"""
Script to load EMG data from pkl files.

COMB_EMG_DATA: Dictionary with keys (subject, trial) and values a pandas dataframe with EMG data.
    The EMG data should already be cleaned and normalized to maximum contraction values.
SPLIT_EMG_DATA: Dictionary with keys (subject, trial) and values a list of pandas dataframes with EMG data.
    The EMG data should already be cleaned and normalized to maximum contraction values.
    Additionally, this data should be split into individual trial repetitions.
"""


import os
import pickle

# Path to the pkl files with EMG data
SPLIT_FILEPATH = "splitnorm_EMG_cleaned.pkl"
NOTSPLIT_FILEPATH = "normalized_emg_not_split.pkl"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

split_filename = os.path.join(BASE_DIR, SPLIT_FILEPATH)
notsplit_filename = os.path.join(BASE_DIR, NOTSPLIT_FILEPATH)

with open(split_filename, "rb") as file:
    SPLIT_EMG_DATA = pickle.load(file)

with open(notsplit_filename, "rb") as file:
    COMB_EMG_DATA = pickle.load(file)
