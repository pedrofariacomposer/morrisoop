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


def ret_tto(tto):
    if tto[0] == "R":
        return tto[1:]
    else:
        return "R" + tto
    
def test_part(group_rows, part):
    perms = distinct_permutations(part)
    result = []
    for p in perms:
        sl = []
        sl_s = []
        for i, el in enumerate(p):
            sl += group_rows[i][0:el]
            sl_s.append(group_rows[i][0:el])
        if list(sorted(sl)) == list(range(12)):
            result.append(sl_s)
    return result


def find_fourth_row(rows):
    prime_row, second_row, third_row = rows
    candidates = [x for x in prime_row.set_class() if prime_row.tto(x).has_comb(third_row)]
    first_third_inter = Pcset(prime_row[0:6]).intersection(Pcset(third_row[0:6]))
    result = []
    for el in candidates:
        new_int = Pcset(second_row[0:6]).intersection(Pcset(prime_row.tto(el)[0:6]))
        if len(new_int) == 3 and len(new_int.intersection(first_third_inter)) == 0:
            result.append(el)
    return result


            
def find_unique_sublists(main_list, num_sublists_to_select):
    selected_sublists = []

    for sublist in main_list:
        all_strings = set(sublist)
        unique_strings = all_strings - set().union(*selected_sublists)
        
        if len(unique_strings) >= 4:
            selected_sublists.append(sublist)
        
        if len(selected_sublists) == num_sublists_to_select:
            break

    if len(selected_sublists) != num_sublists_to_select:
        return None
    return selected_sublists

def test_part(group, parts):
    inds = [0] * len(group)
    for i, el in enumerate(parts):
        partition = [group[x][inds[x]:inds[x]+el[x]] for x in range(len(el))]
        new_inds = [inds[x] + el[x] for x in range(len(el))]
        inds = new_inds
        s = []
        for x in partition:
            s += x
        new_s = [x.pitch for x in s]
        if len(set(new_s)) != 12:
            return False
    return True

def find_right_partitions(group, possible_partitions):
    right_parts = []
    for p in possible_partitions:
        for x in permutations(p):
            if test_part(group, x) == True:
                right_parts.append(x)
    return right_parts