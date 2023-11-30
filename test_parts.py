from more_itertools import distinct_permutations
from itertools import product

# Example MAINLIST
MAINLIST = [
    [4, 4, 2, 2],
    [3, 4, 3, 2],
    [1, 3, 5, 3],
    [5, 1, 3, 3]
]

def check_part_list(partlist):
    perms = [distinct_permutations(x) for x in partlist]
    combs = list(product(*list(perms)))
    result = []
    for comb in combs:
        sums = [0] * len(comb)
        for sublist in comb:
            for i, el in enumerate(sublist):
                sums[i] += el
        if sums == [12] * len(comb):
            result.append(comb)
    return result