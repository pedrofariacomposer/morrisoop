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

# definir a row
row_r = [11,10,3,7,6,2,4,5,8,1,9,0]
r = Row(row_r)

# acha todas as TTOs que produzem combinatoriedade hexacordal com a row r
combs = r.combinatoriality()

# acha um dicionário com os TTOs que produzem intersecção hexacordal == 3
three_intersect = {ttos: r.tto(ttos) for ttos in _ALL_ROW_SET_OPS if len(Pcset(r.tto(ttos)[0:6]).intersection(Pcset(r[0:6]))) == 3}

# acha todas as partições de 12 com cardinalidade lynes ou menor, e preenche com zeros para que fiquem exatamente com lynes elementos
lynes = 6
comps = [x for x in partitions_n(12) if len(x) <= lynes]
for x in comps:
    if len(x) < lynes:
        while len(x) < lynes:
            x.append(0)
            

# tentando produzir um grupo com quatro rows tal que:
# 1) cada par de rows tenha combinatoriedade hexacordal (rows 1 e 2, rows 3 e 4, entre si)
# 2) a intersecção do primeiro hexacorde de cada row em cada par seja igual a 3 com o primeiro hexacorde de cada row dos outro par

# opções para primeira row:
# todas as formas da série que possuam o mesmo primeiro hexacorde que a row original r
first_row = list(sorted([ret_tto(x) for x in r.combinatoriality()]))
# opções para segunda row:
# todas as formas da série que possuam combinatoriedade hexacordal com a row original r
second_row = r.combinatoriality()
# opções para terceira row:
# todas as formas da série que possuam intersecção do primeiro hexacorde igual a 3 com a row original r
third_row = list(three_intersect.keys())

# para achar a quarta row, é criada uma função find_fourth_row, que pega um grupo de três rows,
# e tenta achar uma quarta row R4 tal que:
# 1) R4 tenha combinatoriedade hexacordal com a terceira row
# 2) R4 tenha intersecão do primeiro hexacorde igual a 3 com a segunda row
# depois, é criada uma função MAINLIST que pega todas combinações possíveis de quatro formas da série que atendem aos requisitos
a = list(product(*[first_row, second_row, third_row]))
MAINLIST = []
for y in a:
    MAINLIST.append(y)
    '''
    rows = [r.tto(x) for x in y]
    row_labels = [x for x in y]
    res = find_fourth_row(rows)
    if len(res) > 0:
        for k in res:
            new_row = row_labels + [k]
            MAINLIST.append(new_row)'''

# queremos agora encontrar uma lista com 8 grupos de 4 rows em MAINLIST tais que não repitam nenhuma forma da série entre si
# ou seja, 8 grupos com 4 formas da row r, tendo 32 versões distintas de r
# a função find_unique_sublists acha esssa lista
# idealmente, se embaralha a MAINLIST a cada vez que se quiser gerar um resultado diferente,
# já que find_unique_sublists encontra as oito primeiras listas que satisfazem a condição
# \/ \/ \/ descomentar se quiser embaralhar \/ \/ \/
shuffle(MAINLIST)
selected_sublists = find_unique_sublists(MAINLIST, 8)
selected_sublists = MAINLIST[0:8]

# agora achamos nossas oito sublistas, vamos jogá-la para um dataframe e pôr no excel
data = dict()
for x in selected_sublists:
    data[str(x)] = [r.tto(y) for y in x]
df = pd.DataFrame(data=data)
#df.to_excel("test_superarray.xlsx")

# aqui achamos, para cada grupo de formas da série, as composições que os particionam

count = 0
while True:
    selected_partitions = []
    sizes = []
    for sublist in selected_sublists:
        group = [r.tto(x) for x in sublist]
        selected_partitions.append(find_right_partitions(group, possible_threes))
        #print(f"Finished {count}")
        count += 1
    for x in selected_partitions:
        sizes.append(len(x))
    if 0 not in sizes:
        break
    
# é criado um dataframe e uma planilha do excel na qual cada coluna são:
# 1) os nomes das formas da série
# 2) as formas da série propriamente ditas
# 3) as possíveis composições que particionam essas formas
S = [[selected_sublists[i]] + [r.tto(x) for x in selected_sublists[i]] + selected_partitions[i] for i in range(len(selected_sublists))]
D = {k:pd.Series(v) for k,v in enumerate(S)}
df = pd.DataFrame(data=D)
df.to_excel("three_partitions.xlsx")
