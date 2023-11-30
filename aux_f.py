import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import pandas as pd
from itertools import combinations, product, permutations
from collections import defaultdict
import networkx as nx
from more_itertools import distinct_permutations

_ALL_TTOS = [f"T{n}" for n in range(10)] + ["Ta", "Tb"] + [f"T{n}I" for n in range(10)] + ["TaI", "TbI"] + [f"T{n}M" for n in range(10)] + ["TaM", "TbM"] + [f"T{n}MI" for n in range(10)] + ["TaMI", "TbMI"]

_ALL_SET_OPS = _ALL_TTOS[:24]

_ALL_ROW_TTOS = _ALL_TTOS + ["R" + x for x in _ALL_TTOS]

_ALL_ROW_SET_OPS = _ALL_SET_OPS + ["R" + x for x in _ALL_SET_OPS]


def partitions_n(n):
    a = [0 for i in range(n+1)]
    k = 1
    y = n-1
    while k != 0:
        x = a[k-1] + 1
        k -= 1
        while 2*x <= y:
            a[k] = x
            y-= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k+2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k+1]

def all_compositions(n):
    parts = partitions_n(n)
    result = []
    for p in parts:
        for c in distinct_permutations(p):
            result.append(list(c))
    return result
        

def build_from_intervals(first_el, intervals):
    result = [first_el]
    for i in intervals:
        result.append(result[-1] + i)
    return result

def display_groups(group):
    ''' group: lista de PcSetGroup
        Formata e imprime uma coleção de PcSetGroup
    '''
    print(f"Total groups = {len(group)}")
    for i,x in enumerate(group):
        print(f"--------------------{i}--------------------")
        print(f"Row: {x.elements[0].prime_form()}")
        print(f"Col: {x.invert_group().elements[0].prime_form()}")
        print(x.parse_group())

def write_groups(group,sheet_name="Grupos",filename="test.xlsx"):
    ''' group: lista de PcSetGroup
        sheet_name: nome da aba
        filename: nome do arquivo (.xlsx)
        Salva um grupo em um arquivo .xlsx
    '''
    df1 = pd.DataFrame([f"Total de grupos: {len(group)}"])
    start_row = 0
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name=sheet_name, index=False, startrow=start_row, startcol=0)
        for i, x in enumerate(group):
            df2 = pd.DataFrame([f"--------------------{i}--------------------"])
            df3 = pd.DataFrame([f"Row: {x.elements[0].prime_form()}"])
            df4 = pd.DataFrame([f"Col: {x.invert_group().elements[0].prime_form()}"])
            df5 = x.display_group()
            df2.to_excel(writer, sheet_name=sheet_name, header=False, index=False, startrow=start_row + 2, startcol=0)
            df3.to_excel(writer, sheet_name=sheet_name, header=False, index=False, startrow=start_row + 4, startcol=0)
            df4.to_excel(writer, sheet_name=sheet_name, header=False, index=False, startrow=start_row + 6, startcol=0)
            df5.to_excel(writer, sheet_name=sheet_name, startrow=start_row + 8, startcol=0)
            start_row = start_row + len(df4) + 12

def multiple_dfs(df_list, sheets, file_name, spaces):
    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        row = 0
        for dataframe in df_list:
            dataframe.to_excel(writer, sheet_name=sheets, startrow = row, startcol = 0)
            row = row + len(dataframe.index) + spaces + 1
