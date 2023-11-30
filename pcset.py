import pickle
from pc import *
from aux_f import *
from aux_f import _ALL_TTOS, _ALL_SET_OPS, _ALL_ROW_TTOS, _ALL_ROW_SET_OPS
from itertools import product
from more_itertools import powerset



class Pcset:
    
    '''
    Classe para representar um conjunto de classes de alturas (ordenadas ou não)
    Parâmetros:
    -----------
    pitches: lista [inteiros | Pc]
        Lista de inteiros ou de pitch classes

    '''
    
    def __init__(self, elements: list): 
        self.elements = [Pc(el) for el in elements]
        self.pitches = [el.pitch for el in self.elements]
        
    ##### Overloading #####
        
    def __repr__(self):
        result = ""
        for el in self.elements:
            result += el.__repr__().strip("Pc()")
        return f"<{result}>"
    
    def __len__(self):
        return len(self.elements)
    
    def __eq__(self, other):
        return sorted([x for x in self.pitches]) == sorted([x for x in other.pitches])
    
    def __iter__(self):
        return iter(self.elements)
    
    def __add__(self, other):
        newPcset = Pcset(self.pitches)
        for el in other:
            newPcset.append(el)
        return newPcset
    
    def __contains__(self, el):
        return Pc(el) in self.elements
    
    def __getitem__(self, key):
        return self.elements[key]
    
    def __setitem__(self, key, value):
        self.elements[key] = value
    
    def append(self, el):
        if Pc(el) not in self.elements:
            self.elements.append(Pc(el))
            self.pitches.append(self.elements[-1].pitch)
            
    ##### Operações de alturas #####

    def transposition(self, n: int):
        ''' Aplica Tn a um pcset '''
        return Pcset([x.transposition(n) for x in self.elements])
        
    def multiplication(self, m: int = 5):
        ''' Aplica M a um pcset '''
        return Pcset([x.multiplication(m) for x in self.elements])
    
    def inversion(self, n: int = 0):
        ''' Aplica TnI a um pcset '''
        return Pcset([x.inversion(n) for x in self.elements])
    
    def tto(self, TTO):
        ''' Aplica um TTO aos elementos de um pcset '''
        return Pcset([el.tto(TTO) for el in self.elements])
    
    def ttos(self):
        ''' Aplica todos os TTOs a um pcset '''
        result = dict()
        for TTO in _ALL_TTOS:
            newPcset = self.tto(TTO)
            if newPcset in result.values():
                key = [k for k in result.keys() if result[k] == newPcset][0]
                newKey = key + " " + TTO
                result[newKey] = result.pop(key)
            else:
                result[TTO] = newPcset
        return result
    
    def set_class(self):
        ''' Encontra os elementos da classe de um pcset (exclui TTOs com M) '''
        result = dict()
        for SC in _ALL_SET_OPS:
            newPcset = self.tto(SC)
            if newPcset in result.values():
                key = [k for k in result.keys() if result[k] == newPcset][0]
                newKey = key + " " + SC
                result[newKey] = result.pop(key)
            else:
                result[SC] = newPcset
        return result
    
    def interval_class_content(self):
        result = []
        for i in range(1,len(self)):
            result.append(self[i-1].ip(self[i]))
        return result
        
    ##### Operações de ordem #####
            
    def rotation(self, n: int):
        ''' Rotaciona um pcset para que o mesmo comece na posição n '''
        return Pcset(self.pitches[n % len(self):] + self.pitches[0:n % len(self)])
    
    def retrograde(self):
        ''' Encontra o retrógrado de um Pcset '''
        return Pcset([x for x in reversed(self.elements)])
    
    def ordered_partitions_n(self, n):
        parts = [x for x in all_compositions(len(self)) if len(x) <= n]
        for p in parts:
            if len(p) < n:
                while len(p) < n:
                    p.append(0)
            for pp in permutations(p):
                if list(pp) not in parts:
                    parts.append(list(pp))
        result = [self.partition(x) for x in parts]
        return result
        
    
    ##### Vetores e matrizes #####
        
    def icv(self):
        ''' Encontra o vetor de classes intervalares de um pcset '''
        vector = [0] * 7
        for i in range(len(self.elements)):
            for j in range(i, len(self.elements)):
                vector[self.elements[i].icn(self.elements[j])] += 1
        return vector
    
    def invariance_vector(self):
        ''' Encontra o vetor de invariâcia de um pcset '''
        result = [0] * 8
        invariances = self.find_invariance()
        for inv in invariances:
            if len(inv) == 2:
                result[0] += 1
            elif len(inv) == 3:
                if inv[-1] == "I":
                    result[1] += 1
                elif inv[-1] == "M":
                    result[2] += 1
            elif len(inv) == 4:
                result[3] += 1
        if len(self) < 7:
            comps = self.find_comp_invariance()
            for comp in comps:
                if len(comp) == 2:
                    result[4] += 1
                elif len(comp) == 3:
                    if comp[-1] == "I":
                        result[5] += 1
                    elif comp[-1] == "M":
                        result[6] += 1
                elif len(comp) == 4:
                    result[7] += 1
        return result
    
    def sum_vector(self, other):
        ''' Retorna um vetor de soma dos pcs de dois pcsets '''
        vec = [0] * 12
        for el in self.elements:
            for el2 in other.elements:
                vec[el + el2] += 1
        return vec

    def ic_matrix(self, other):
        ''' Encontra a matriz de classes de intervalos entre dois pcsets '''
        arr = np.eye(len(self), len(other), dtype=int)
        for i, el in enumerate(self.elements):
            for j, el2 in enumerate(other.elements):
                arr[i,j] = el2 - el
        df = pd.DataFrame(arr, index=self.pitches, columns=other.pitches)
        return df
    
    def iv_vector(self, other):
        vec = [0] * 12
        for el in self.elements:
            for el2 in other.elements:
                vec[el2-el] += 1
        return vec

    
    ##### Testes e comparações #####
    
    def most_compact(self, other):
        ''' Função auxiliar para encontrar a forma normal de um pcset '''
        a = self.pitches
        b = other.pitches
        for i in range(len(a)-1, 0, -1):
            a_diff = (a[i] - a[0]) % 12
            b_diff = (b[i] - b[0]) % 12
            if a_diff < b_diff:
                return Pcset(a)
            elif a_diff > b_diff:
                return Pcset(b)
        if a[0] < b[0]:
            return Pcset(a)
        else:
            return Pcset(b)

    def is_subset(self, other):
        ''' Diz se o pcset é subconjunto de um outro '''
        if len(other) < len(self):
            return False
        for el in self:
            if el not in other:
                return False
        return True
    
    def is_superset(self, other):
        ''' Diz se o pcset contém o outro '''
        return other.is_subset(self)
    
    def compare(self, other):
        ''' Compara dois pcsets como se fossem pcsegs '''
        return self.pitches == other.pitches
    
    def z_relation(self, other):
        if (other not in self.set_class().values() and self.icv() == other.icv()):
            return True
        return False
        
    def compare_position(self, other):
        ''' Compara dois pcsets (segs), e retorna True se todas as posições de cada um são diferentes '''
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self.pitches[i] == other.pitches[i]:
                return False
        return True
    
    def abstract_included(self, other):
        ''' Avalia se self está incluso de forma abstrata em other '''
        if len(other) < len(self):
            return False
        for pcset in other.set_class().values():
            if self.is_subset(pcset):
                return True
        return False
    
    def abstract_includes(self, other):
        ''' Avalia se self inclui de forma abstrata other '''
        return other.abstract_included(self)
    
    def abstract_complement(self, other):
        ''' Avalia se dois Pcsets são complementares de forma abstrata '''
        if len(self) + len(other) != 12:
            return False
        count = 0
        other_set_class = other.set_class()
        for el in self.set_class():
            if el.complement() in other_set_class.values():
                count += 1
        if count == len(self.set_class()):
            return True
        else:
            return False
        
    ##### Funções que retornam outros Pcsets #####
    
    def complement(self,rel=range(12)):
        ''' Encontra o complemento de um Pcset '''
        return Pcset([x for x in rel if x not in self.pitches])

    def normal_form(self):
        ''' Encontra a forma normal de um pcset '''
        pcset = self.pitches
        uniques = list(set(pcset))
        uniques.sort()
        best = Pcset(uniques)
        uniques = Pcset(uniques)
        for i in range(1, len(uniques)):
            rot = uniques.rotation(i)
            best = best.most_compact(rot)
        return best

    def prime_form(self):
        ''' Encontra a forma prima de um pcset '''
        def int_first_n(A, n):
            return (A[n]-A[0]) % 12
        n = len(self)
        P = self.pitches
        I = self.inversion().pitches
        A = sorted([x for x in P])
        IA = sorted([x for x in I])
        q = 1
        rots_P = [A[n:] + A[:n] for n in range(12)]
        rots_I = [IA[n:] + IA[:n] for n in range(12)]
        S = rots_P + rots_I
        while True:
            if q == n:
                S_line = S
                break
            else:
                subs = [int_first_n(x, n-q) for x in S]
                S_line = [x for x in S if int_first_n(x,n-q) == min(subs)]
                if len(S_line) == 1:          
                    break
                else:
                    q += 1
                    S = S_line
        result = Pcset(S_line[0])
        return result.transposition(-S_line[0][0])
    
    def intersection(self, other):
        ''' Encontra a intersecção entre dois pcsets '''
        return Pcset([x for x in self if x in other])
    
    def begin_set(self, n):
        ''' Encontra o conjunto início de cardinalidade n de self '''
        return Pcset(self[0:n])
    
    def end_set(self, n):
        ''' Encontra o conjunto fim de cardinalidade n de self '''
        return Pcset(self[len(self)-n:])
    
    def all_begin_sets(self):
        ''' Encontra todos os conjuntos início de self '''
        result = dict()
        for n in range(0,len(self)):
            result[str(n)] = self.begin_set(n)
        return result
    
    def all_end_sets(self):
        ''' Encontra todos os conjuntos fim de self '''
        result = dict()
        for n in range(0,len(self)):
            result[str(n)] = self.end_set(n)
        return result
    
    ##### Funções que retornam valores sobre o pcset e possivelmente outro(s) #####
    
    def find_sc_op(self, other):
        ''' Encontra (caso exista) a operação de set class que transforma other em self '''
        if len(self) != len(other):
            return []
        if other in self.set_class().values():
            return [k for (k,v) in self.set_class().items() if v == other]
        
    def find_tto(self, other):
        ''' Encontra (caso exista) o tto que transforma other em self '''
        if len(self) != len(other):
            return []
        if other in self.ttos().values():
            return [k for (k,v) in self.ttos().items() if v == other]

    def MUL(self, other, n):
        ''' Retorna a multiplicidade do valor n no iv_vector entre dois pcsets '''
        return self.iv_vector(other)[n]
    
    def find_invariance(self):
        ''' Encontra os ttos sob os quais um pcset é invariante '''
        all_ttos = self.ttos()
        if self not in all_ttos.values():
            return []
        else:
            candidates = [k for (k,v) in all_ttos.items() if v == self][0]
            return candidates.split(' ')

    def SUM(self, other, n):
        ''' Retorna a multiplicidade da soma n entre dois pcsets '''
        return self.sum_vector(other)[n]
    
    def EMB(self, other):
        ''' Retorna quantos membros de self que estão inclusos em um membro de other '''
        if len(self) > len(other) or not other.abstract_includes(self):
            return 0
        p_self = self.prime_form()
        p_other = other.prime_form()
        sets = p_other.n_subsets(len(self))
        count = 0
        for s in sets:
            if s.prime_form() == p_self:
                count += 1
        return count
     
    def COV(self, other):
        ''' Retorna quantos membros de other cobrem um membro de self '''
        if len(self) > len(other):
            return 0
        p_self = self.prime_form()
        p_other = other.prime_form()
        sets = p_other.set_class()
        count = 0
        for s in sets:
            if sets[s].is_superset(p_self):
                count += 1
        return count

    def find_comp_invariance(self):
        ''' Encontra os ttos sob os quais um pcset mapeia a seu complemento '''
        if len(self) > 6:
            return []
        all_ttos = self.ttos()
        comp = self.complement()
        result = []
        for k, v in all_ttos.items():
            if comp.is_subset(v):
                els = k.split(" ")
                result += els
        return result
    
    def all_subsets(self):
        ''' Encontra todos os subconjuntos de um pcset '''
        result = []
        for i in range(len(self)+1):
            combs = combinations(self.pitches, i)
            for c in combs:
                if len(c) > 0 and len(c) < len(self):
                    result.append(Pcset(list(c)))
        return result
            
    def n_subsets(self, n):
        ''' Encontra todos os subconjuntos de um pcset de cardinalidade n '''
        return [x for x in self.all_subsets() if len(x) == n]
    
    def two_partition(self, n=None):
        ''' Encontra todas as partições de um pcset (ou as que começam com conjuntos de cardinalidade n) '''
        powers = self.all_subsets()
        result = [[Pcset([]), self]]
        _used = [self]
        for p in powers:
            if p not in _used:
                comp_p = p.complement(self)
                _used.append(comp_p)
                pair = sorted([p, comp_p], key=len)
                result.append(pair)
        if n:
            return [x for x in result if (len(x[0]) == n or len(x[1]) == n) ]
        else:
            return result

    def abstract_tto(self, other):
        ''' Caso self esteja incluso de forma abstrata em other, retorna o(s) tto(s) que o transforma '''
        if not self.abstract_included(other):
            return None
        result = []
        for k,x in self.set_class().items():
            if x.is_subset(other):
                result.append(x)
        return result

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
    
    def combinatoriality(self):
        if len(self) != 6:
            return []
        result = []
        comp = self.complement()
        for x in _ALL_SET_OPS:
            if self.tto(x) == comp:
                result.append(x)
        return result
                
    
    
    ##### Processos Composicionais #####
    ### Estruturas canônicas de Robert Morris ###

    def top_group(self):
        ''' Retorna um PcSetGroup com o Pcset dado sendo o topo do mesmo '''
        forms = self.set_class()
        candidates = defaultdict(list)
        for x in forms.values():
            for i in range(1,len(self)):
                if x.rotation(i).compare_position(self):
                    candidates[i].append(x.rotation(i))
        candidate_values = [candidates[key] for key in sorted(candidates.keys())]
        groups = [PcsetGroup([self] + list(combination)) for combination in product(*candidate_values)]
        non_dup_groups = [x for x in groups if x.compare_group()]
        prime_groups = [x for x in non_dup_groups if x.invert_group().same_primes()]
        return prime_groups
    
    def bottom_group(self):
        ''' Retorna um PcSetGroup com o Pcset dado sendo o último do mesmo '''
        forms = self.set_class()
        candidates = defaultdict(list)
        for x in forms.values():
            for i in range(1,len(self)):
                if x.rotation(i).compare_position(self):
                    candidates[i].append(x.rotation(i))
        candidate_values = [candidates[key] for key in sorted(candidates.keys())]
        groups = [PcsetGroup(list(combination)+[self]) for combination in product(*candidate_values)]
        non_dup_groups = [x for x in groups if x.compare_group()]
        prime_groups = [x for x in non_dup_groups if x.invert_group().same_primes()]
        return prime_groups
    
    def find_group(self, pos="b"):
        if pos == "b":
            return self.bottom_group()
        elif pos == "t":
            return self.top_group()
        
    def compositions(self):
        comps = all_compositions(len(self))
        result = []
        for c in comps:
            result.append(self.partition(c))
        return result

###################################################################
    

class PcsetGroup:
    
    '''
    Classe para representar um grupo de Pcsets.
    
    Parâmetros:
    -----------
    elements: list[Pcset | list[int | Pcset]]
        Lista de Pcsets

    '''
    
    def __init__(self, elements):
        self.elements = []
        for el in elements:
            if isinstance(el, Pcset):
                self.elements.append(el)
            else:
                self.elements.append(Pcset(el))
    
    ##### Overloading #####
    
    def __repr__(self):
        return f"PcsetGroup{self.elements}"
    
    def __len__(self):
        return len(self.elements)
    
    def __iter__(self):
        return iter(self.elements)
    
    ##### Testes e comparações #####
    
    def compare_group(self):
        ''' Checa se um grupo é uma non-duplicating array '''
        group = self.elements
        for pcset1 in group:
            for pcset2 in group:
                if not pcset1.compare(pcset2) and not pcset1.compare_position(pcset2):
                    return False
        return True
    
    def is_square(self):
        ''' Checa se o grupo é quadrado '''
        for el in self.elements:
            if len(el) != len(self):
                return False
        return True

    def same_primes(self):
        ''' Checa se todos os Pcsets de um grupo tem a mesma forma prima '''
        group = self.elements
        result = []
        for el in group:
            pr = el.prime_form()
            if pr not in result:
                result.append(pr)
        if len(result) == 1:
            return True
        else:
            return False
    
    ##### Operações sobre grupos (retornam outro grupo) #####
        
    def invert_group(self):
        ''' Transpõe o grupo (como uma matriz) '''
        if self.is_square() == False:
            return None
        result = []
        for i in range(len(self)):
            result.append(Pcset([x.pitches[i] for x in self.elements]))
        return PcsetGroup(result)

    ##### Métodos para formatar, mostrar e salvar grupos #####

    def parse_group(self):
        ''' Retorna um objeto formatado para ser impresso '''
        inverted = self.invert_group()
        index = [str(self.elements[0].find_sc_op(x)[0]) for x in self.elements]
        columns = [str(inverted.elements[0].find_sc_op(x)[0]) for x in inverted.elements]
        df = pd.DataFrame(self.elements, index=index, columns=columns)
        return df

##########################################################

class Pcseg(Pcset):
    
    def tto(self, TTO):
        if TTO[0] != "R":
            return Pcseg([Pc(x).tto(TTO) for x in self])
        else:
            return Pcseg(list(reversed([Pc(x).tto(TTO[1:]) for x in self])))
        
    def combinatoriality(self):
        if len(self) != 6:
            return []
        result = []
        comp = self.complement()
        for x in _ALL_ROW_SET_OPS:
            if self.tto(x) == comp:
                result.append(x)
        return result
    

##########################################################


class TTO:
    
    def __init__(self, tto):
        self.tto = tto
        self.find_cycles()
        self.type = self.find_type()
        
    def find_cycles(self):
        result = []
        used = []
        for i in range(12):
            if i not in used:
                cyc = Pc(i).cycle_tto(self.tto)
                used += cyc
                result.append(cyc)
        self.cycles = result
    
    def find_type(self):
        if self.tto[0] != "R":
            if len(self.tto) == 2:
                return "transposition"
            elif len(self.tto) == 3:
                if self.tto[-1] == "I":
                    return "inversion"
                elif self.tto[-1] == "M":
                    return "multiplication"
            else:
                return "multiplication inversion"
        else:
            return "retrograde " + TTO(self.tto[1:]).find_type()
            
        
    def cas(self):
        result = []
        for cyc in self.cycles:
            if len(cyc) == 1:
                result.append(cyc)
            else:
                for i in range(len(cyc)):
                    pair = [cyc[i], cyc[(i+1) % len(cyc)]]
                    result.append(pair)
        return result
                
    def find_cross_sections(self):
        prods = product(*self.cycles)
        pcsets = []
        for prod in prods:
            pcset = Pcset(prod)
            if pcset not in pcsets:
                pcsets.append(pcset)
        return pcset
    
    def find_invariant_scs(self):
        cycles = self.cycles
        unions = []
        i_groups = [list(x) for x in powerset(list(range(len(cycles)))) if len(x) > 0]
        for group in i_groups:
            pcgroup = []
            for i in group:
                pcgroup += cycles[i]
            unions.append(Pcset(pcgroup))
        return unions
        
    def __repr__(self):
        return self.tto