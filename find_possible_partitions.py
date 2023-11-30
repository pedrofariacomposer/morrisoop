from aux_f import *
from aux_f import _ALL_TTOS, _ALL_SET_OPS, _ALL_ROW_TTOS, _ALL_ROW_SET_OPS
from pc import *
from pcset import *
from pickle_vars import *
from row import *
from two_partitions import *
from pcsetgroup import *
from collections import defaultdict
from random import shuffle, choices
from test_parts import *
from more_functions import *


'''
num_ind = 6
parts = [x for x in partitions_n(12) if len(x) <= num_ind]
for x in parts:
    if len(x) < num_ind:
        while len(x) < num_ind:
            x.append(0)
            
mainlists = list(combinations(parts, num_ind))
possible_partitions = []
count = 0
for mainlist in mainlists:
    checks = check_part_list(mainlist)
    if len(checks) > 0:
        possible_partitions.append(checks)
    print(count)
    print(len(mainlists))
    count += 1

all_pos = []
for x in possible_partitions:
    for y in x:
        all_pos.append(y)'''
'''
if len(all_pos) > 0:
    with open(f"possible_compositions_{str(num_ind)}.pkl", "wb") as f:
              pickle.dump(all_pos, f)'''
    
print("______________")

a = Pcset([1,3,7,9,2,10])
print(a, a.tto("T8MI"))