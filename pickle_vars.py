import pickle
from pcset import *
from pc import *



with open('two_partition_12.pkl', 'rb') as file:
    two_part_12 = pickle.load(file)
    two_part_12.append([Pcset(list(range(12))), Pcset([])])
    '''
        Todas as partições de dois do agregado
    '''

with open('all_interval_rows.pkl', 'rb') as f:
    all_interval_row_sequences = pickle.load(f)
    '''
        Todas as sequências intervalares que geram all interval rows
    '''
    
with open("possible_compositions_four.pkl", "rb") as f:
    possible_fours = pickle.load(f)
    
with open("possible_compositions_three.pkl", "rb") as f:
    possible_threes = pickle.load(f)