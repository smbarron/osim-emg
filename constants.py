"""
Constants for measured/predicted EMG combination. 

MUSCLE_MAPPING: Dictionary with keys the muscle names in the OpenSim model and values the muscle names in the EMG dataframes.
    None values correspond to non-measured muscles, for which the predicted activations will be used.
EMG_SAMPLING_RATE: Sampling rate of the EMG data. 
MOCAP_SAMPLING_RATE: Sampling rate of the motion capture data.
"""

MUSCLE_MAPPING = {
            'time': None,
            'TrapeziusScapula_M': 'Upper trapezius' , 
            'TrapeziusScapula_S': 'Upper trapezius',
            'TrapeziusScapula_I': 'Lower trapezius', 
            'TrapeziusClavicle_S': 'Upper trapezius', 
            'SerratusAnterior_I': 'Serratus anterior',
            'SerratusAnterior_M': 'Serratus anterior', 
            'SerratusAnterior_S': 'Serratus anterior', 
            'Rhomboideus_S': None,
            'Rhomboideus_I': None, 
            'LevatorScapulae': None, 
            'Coracobrachialis': None,
            'DeltoideusClavicle_A': "Anterior deltoid", 
            'DeltoideusScapula_P': 'Posterior deltoid', 
            'DeltoideusScapula_M': 'Middle deltoid',
            'LatissimusDorsi_S': 'Latissimus dorsi', 
            'LatissimusDorsi_M': 'Latissimus dorsi', 
            'LatissimusDorsi_I': 'Latissimus dorsi',
            'PectoralisMajorClavicle_S': 'Pectoralis major', 
            'PectoralisMajorThorax_I': 'Pectoralis major',
            'PectoralisMajorThorax_M': 'Pectoralis major', 
            'TeresMajor': None, 
            'Infraspinatus_I': 'Infraspinatus',
            'Infraspinatus_S': 'Infraspinatus', 
            'PectoralisMinor': None, 
            'TeresMinor': 'Teres minor', 
            'Subscapularis_S': 'Subscapularis',
            'Subscapularis_M': 'Subscapularis', 
            'Subscapularis_I': 'Subscapularis', 
            'TRIlong': None, 
            'BIC_long': None, 
            'BIC_brevis': None,
}

EMG_SAMPLING_RATE = 3000
MOCAP_SAMPLING_RATE = 120
