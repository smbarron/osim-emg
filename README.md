# osim_emg
A package with functions to merge measured EMG with the outputs of OpenSim's static optimization tool for use in Joint Reactions Analyses in OpenSim. This was designed for use with the Thoracoscapular OpenSim model, available at https://simtk.org/projects/thoracoscapular.

## Primary functions
The primary functions for using this package are 'osim_emg.activations_to_states.combine_files' and 'osim_emg.merge_measured_with_predicted.save_combined_activations'.

## Formatting EMG data
Use of these functions require two EMG data files/filepaths:

'split_emg_filepath': Path to the split EMG data file. This should be a .pkl file containing a dictionary of the form {(subject, trial): List[emg_data]}, where emg_data is a pandas dataframe containing the EMG data for a single task repetition within a trial.

'not_split_emg_filepath': Path to the non-split EMG data file. This should be a .pkl file containing a dictionary of the form {(subject, trial): emg_data}, where emg_data is a pandas dataframe containing the EMG data for whole trial.

All EMG data should be pre-filtered and normalized to maximum contraction values prior to storing in .pkl files.

## Example usage
To see an example of how these functions are used within the Joint Reactions Analyses pipeline, see 'JRA_Batch.py' within my opensim-py repository (https://github.com/smbarron/opensim-py).
