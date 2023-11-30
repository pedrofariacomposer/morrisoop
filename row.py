from pcset import *
from aux_f import _ALL_TTOS, _ALL_SET_OPS, _ALL_ROW_TTOS, _ALL_ROW_SET_OPS

class Row(Pcset):
    
    '''
    Classe para representar uma série dodecafônica.
    
    Parâmetros:
    -----------
    pitches: Pcset | lista[int | Pc]
        Pitch class set ou lista de pitch classes (ou inteiros)

    '''
    
    ##### Overloading #####
    
    def __repr__(self):
        return "Row"+ super().__repr__()
    
    def __eq__(self, other):
        return self.elements == other.elements
    
    ##### Testes e comparações #####
        
    def is_all_interval(self):
        intervals = self.interval_class_content()
        if len(set(intervals)) == 11:
            return True
        return False
    
    def find_tto(self, other):
        ''' Encontra (caso exista) o tto que transforma other em self '''
        if len(self) != len(other):
            return []
        for k, v in self.ttos().items():
            if v.compare(other):
                return k
    ##### Operações sobre alturas #####
    
    def transposition(self, n):
        return Row(Pcset(self.elements).transposition(n))
    
    def inversion(self, n=0):
        return Row(Pcset(self.elements).inversion(n))
    
    def multiplication(self, m=5):
        return Row(Pcset(self.elements).multiplication(m))
    
    def prime_form(self):
        return Row(list(range(12)))
    
    def normal_form(self):
        return self.transposition(-self.pitches[0])
    
    def tto(self, TTO):
        return Row(Pcseg(self.elements).tto(TTO))
    
    def q_relation(self):
        if not self.is_all_interval():
            return self
        else:
            for n in range(1,12):
                new_rot = self.rotation(n)
                if new_rot.is_all_interval():
                    return new_rot
    
    def combinatoriality(self, m=False):
        tto_source = _ALL_ROW_TTOS if m else _ALL_ROW_SET_OPS
        result  = []
        first_half  = Pcset(self[0:6])
        for tto in tto_source:
            transform = self.tto(tto)
            second_half  = Pcset(transform[6:])
            if first_half == second_half:
                result.append(tto)
        return result
        
    ##### Operações de ordem #####
    
    def rotation(self, n):
        return Row(Pcset(self.elements).rotation(n))
    
    def retrograde(self):
        pitches = self.pitches
        rev = list(reversed(pitches))
        return Row(rev)
    
    def partition(self, part):
        if sum(part) != len(self):
            return self
        else:
            first_i = 0
            result = []
            for p in part:
                newPcset = Pcset(self.elements[first_i:first_i+p])
                first_i += p
                result.append(newPcset)
            return result

    
    ##### Matrizes e vetores #####
    
    def matrix(self):
        result = []
        index = []
        columns = [f"T{x.__repr__()}I" for x in self]
        intervals = self.interval_class_content()
        inverted = self.inversion()
        for el in inverted.transposition(inverted[0].ip(self[0])):
            new_row = Pcset(build_from_intervals(el, intervals))
            result.append(new_row)
            index.append(f"T{new_row[0].__repr__()}")
        df = pd.DataFrame(result, index=index, columns=columns)
        return df

    def set_class(self):
        ''' Encontra os elementos da classe de um pcset (exclui TTOs com M) '''
        result = dict()
        for SC in _ALL_ROW_SET_OPS:
            newPcset = self.tto(SC)
            result[SC] = newPcset
        return result
    
    ##### Testes e comparações #####
    
    def has_comb(self, other, size=6):
        self_first = Pcset(self[0:size])
        other_second = Pcset(other[size:])
        return self_first == other_second
    
    ##### Matrizes de combinação #####
            
    def two_row_CM(self):
        result = defaultdict(list)
        for n in range(1,12):
            b_set = self.begin_set(n)
            e_set = self.end_set(n)
            n_dict = dict()
            inv_dict = dict()
            invs = b_set.find_invariance()
            for t in _ALL_TTOS:
                newRow = self.tto(t)
                new_e_set = newRow.end_set(n)
                if b_set == new_e_set:
                    group = [self, newRow]
                    n_dict[t] = group
                if t in invs and t != 'T0':
                    inv_group = [self.retrograde(), newRow]
                    inv_dict[t] = inv_group
            if len(n_dict) > 0:
                result[str(n)] = n_dict
            if len(inv_dict) > 0:
                result[str(n) + 'R'] = inv_dict
                
        return result

    def three_row_CM(self, n, comp):
        a = self.end_set(n)
        test = []
        perms = []
        result = dict()
        for x in permutations(a):
            if Pcset(x).partition(comp)[0] not in perms:
                test.append(Pcset(x).partition(comp))
                perms.append(Pcset(x).partition(comp)[0])
        beg = self.all_begin_sets()
        for p in test:
            pos = [beg[str(len(x))] for x in p]
            conditions = [p[i].abstract_included(pos[i]) for i in range(len(p))]
            if False not in conditions:
                group = [tuple(pos[i].find_tto(p[i])) for i in range(len(p))]
                result[tuple(group)]  = p
        return result

    def build_proto_cm(self, part):
        result = []
        final = dict()
        for k in part:
            part_frags = [((12 - sum([len(x) for x in part[k]])) % 12)] + [len(x) for x in part[k]]
            rows = [[self]]
            for el in k:
                el = el[0].split(" ")
                group = []
                for x in el:
                    group.append(self.tto(x))
                rows.append(group)
            products =  list(product(*rows))
            for prod in products:
                group = []
                for i, row in enumerate(prod):
                    pair = [row[:part_frags[i]]] + [row[part_frags[i]:]]
                    group.append(pair)
                result.append(group)
        return result

    def find_three_cms(self, ind_range=range(1,9)):
        dfs = []
        for ind in ind_range:
            for comp in [x for x in all_compositions(ind) if len(x) == 2]:
                a = self.three_row_CM(ind, comp)
                b = self.build_proto_cm(a)
                if len(b) > 0:
                    for j in b:
                        c = [x[1] for x in j]
                        n = len(c) - 1
                        test_list = [Pcset(x).ordered_partitions_n(n) for x in c]
                        prods = product(*test_list)
                        for prod in prods:
                            pos = []
                            for i in range(n):
                                pos.append([prod[x][i] for x in range(len(prod))])
                            lens = []
                            pcs = []
                            for po in pos:
                                lens.append(sum([len(x) for x in po]))
                                pcset = po[0]
                                for x in po[1:]:
                                    pcset += Pcset(x)
                                pcs.append(pcset)
                            cond1 = (lens == [len(self)] * n)
                            cond2 = ([len(x) for x in pcs] == [len(self)] * n)
                            if (cond2 and cond1):
                                columns = [
                                    [Pcset(x[0]) for x in j],
                                    [x[0] for x in prod],
                                    [x[1] for x in prod]]
                                rows = [[Pcset(x[0]) for x in columns],
                                        [x[1] for x in columns],
                                        [x[2] for x in columns]]
                                raw_rows = []
                                for r in rows:
                                    pcset = r[0]
                                    for px in r[1:]:
                                        pcset += px
                                    raw_rows.append(Row(pcset))
                                ttos_l = [x.find_tto(raw_rows[0]) for x in raw_rows]
                                df = pd.DataFrame(rows, index = [str(x) for x in ttos_l])
                                dfs.append(df)
        return dfs
            
##########################################################