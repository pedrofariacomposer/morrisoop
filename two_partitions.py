from pcset import *

class TwoPartition:
    
    '''
    Classe para representar uma partição de dois de um Pcset.
    
    Parâmetros:
    -----------
    elements: list[list[Pcset | int]]
        Lista de Pcsets

    '''
    
    def __init__(self, parts):
        self.parts = []
        for part in parts:
            if isinstance(part, Pcset):
                self.parts.append(part)
            else:
                self.parts.append(Pcset(part))
        self.part1, self.part2 = self.parts[0], self.parts[1]
        
    ##### Overloading #####
    
    def __eq__(self, other):
        return (self.part1 == other.part1 and self.part2 == other.part2) or (self.part1 == other.part2 and self.part2 == other.part1)
    
    def __repr__(self):
        p1 = self.part1.pitches
        p2 = self.part2.pitches
        return f"<{p1}|{p2}>"
    
    #### Métodos simples #####
    
    def apply_tto_partition(self):
        ''' Aplica todas as operações de set class a uma partição de dois '''
        result = dict()
        for n in range(12):
            t1 = TwoPartition([x.transposition(n) for x in self.parts])
            t1_label = f"T{n}"
            i1 = TwoPartition([x.inversion(n) for x in self.parts])
            i1_label = f"T{n}I"
            result[t1_label] = t1
            result[i1_label] = i1
        return result
    
    def ret_partition(self):
        ''' Encontra o retrógrado de uma partição '''
        return TwoPartition([self.part2, self.part1])
    
    def join_partitions(self):
        ''' Unifica as partes de uma partição de dois de volta em um Pcset '''
        return self.part1 + self.part2

    def is_part_in_chain(self, chain):
        ''' Dada uma corrente, diz se a partição de dois encontra-se na corrente '''
        for part in chain:
            if self == part:
                return True
        return False

    ##### Processos Composicionais #####
    ### Corrente de Pcsets de Robert Morris ###
    
    def create_raw_chain(self):
        ''' Encontra, caso exista, uma corrente formada pela partição dada '''
        CCP2 = self.part2
        chain = [self]
        while True:
            candidates = self.apply_tto_partition()
            possible_Ms = []
            for tto in candidates:
                if CCP2 == candidates[tto].part1 and self != candidates[tto]:
                    possible_Ms.append(candidates[tto])
                elif CCP2 == candidates[tto].part2 and self != candidates[tto]:
                    possible_Ms.append(candidates[tto].ret_partition())
            possible_Ms = [x for x in possible_Ms if not x.is_part_in_chain(chain)]        
            if len(possible_Ms) > 0:
                CCP = possible_Ms[0]
                CCP2 = CCP.part2
                chain.append(CCP)
            else:
                break
        return chain
    
    def find_chain_ttos(self, chain):
        ''' Encontra os ttos de uma corrente, em relação ao primeiro elemento '''
        pcsets = [x.join_partitions() for x in chain]
        first = pcsets[0]
        return ['-----'] + [first.find_sc_op(x) for x in pcsets[1:]]
    
    def display_chain(self):
        ''' Formata e imprime a corrente '''
        chain = self.create_raw_chain()
        ttos = self.find_chain_ttos(chain)
        print(pd.DataFrame(chain, index = [str(x) for x in enumerate(ttos)], columns=["Chain"]))

    ##### Complexos K- e Kh- #####
        
    def k_relation(self, other):
        ''' Diz se self e other estão em relação K '''
        if (self.join_partitions() == Pcset(list(range(12)))) and (other.join_partitions() == Pcset(list(range(12)))):
            
            cond1 = self.part1.is_subset(other.part1)
            cond2 = self.part1.is_subset(other.part2)
            cond3 = self.part2.is_subset(other.part1)
            cond4 = self.part2.is_subset(other.part2)
            cond5 = other.part1.is_subset(self.part1)
            cond6 = other.part1.is_subset(self.part2)
            cond7 = other.part2.is_subset(self.part1)
            cond8 = other.part2.is_subset(self.part2)
            if cond1 or cond2 or cond3 or cond4 or cond5 or cond6 or cond7 or cond8:
                return True
            return False
        return False
        
    def kh_relation(self, other):
        ''' Diz se self e other estão em relação Kh '''
        if (self.join_partitions() == Pcset(list(range(12)))) and (other.join_partitions() == Pcset(list(range(12)))):
            
            cond1 = self.part1.is_subset(other.part1) and self.part1.abstract_included(other.part2)
            cond2 = self.part1.is_subset(other.part2) and self.part1.abstract_included(other.part1)
            cond3 = self.part2.is_subset(other.part1) and self.part2.abstract_included(other.part2)
            cond4 = self.part2.is_subset(other.part2) and self.part2.abstract_included(other.part1)
            cond5 = other.part1.is_subset(self.part1) and other.part1.abstract_included(self.part2)
            cond6 = other.part1.is_subset(self.part2) and other.part1.abstract_included(self.part1)
            cond7 = other.part2.is_subset(self.part1) and other.part2.abstract_included(self.part2)
            cond8 = other.part2.is_subset(self.part2) and other.part2.abstract_included(self.part1)
            if cond1 or cond2 or cond3 or cond4 or cond5 or cond6 or cond7 or cond8:
                return True
            return False
        return False

    def k_part(self, other):
        ''' Encontra a corrente que ilustra a relação k entre duas partições de dois '''
        if not self.k_relation(other):
            return None
        cond1 = self.part1.is_subset(other.part1)
        cond2 = self.part1.is_subset(other.part2)
        cond3 = self.part2.is_subset(other.part1)
        cond4 = self.part2.is_subset(other.part2)
        cond5 = other.part1.is_subset(self.part1)
        cond6 = other.part1.is_subset(self.part2)
        cond7 = other.part2.is_subset(self.part1)
        cond8 = other.part2.is_subset(self.part2)
        if cond1:
            smallA = self.part1
            smallB = other.part1
            compB = other.part2
        elif cond2:
            smallA = self.part1
            smallB = other.part2
            compB = other.part1
        elif cond3:
            smallA = self.part2
            smallB = other.part1
            compB = other.part2
        elif cond4:
            smallA = self.part2
            smallB = other.part2
            compB = other.part1
        elif cond5:
            smallA = other.part1
            smallB = self.part1
            compB = self.part2
        elif cond6:
            smallA = other.part1
            smallB = self.part2
            compB = self.part1
        elif cond7:
            smallA = other.part2
            smallB = self.part1
            compB = self.part2
        elif cond8:
            smallA = other.part2
            smallB = self.part2
            compB = self.part1
            
        Y = smallA.complement(rel=smallB.pitches)
        return [smallA, Y, compB]
        
    def kh_part(self, other):
        ''' Encontra a(s) corrente(s) que ilustra(m) a relação kh entre duas partições de dois '''
        if not self.k_relation(other):
            return None
        cond1 = self.part1.is_subset(other.part1)
        cond2 = self.part1.is_subset(other.part2)
        cond3 = self.part2.is_subset(other.part1)
        cond4 = self.part2.is_subset(other.part2)
        cond5 = other.part1.is_subset(self.part1)
        cond6 = other.part1.is_subset(self.part2)
        cond7 = other.part2.is_subset(self.part1)
        cond8 = other.part2.is_subset(self.part2)
        if cond1:
            smallA = self.part1
            smallB = other.part1
            compB = other.part2
        elif cond2:
            smallA = self.part1
            smallB = other.part2
            compB = other.part1
        elif cond3:
            smallA = self.part2
            smallB = other.part1
            compB = other.part2
        elif cond4:
            smallA = self.part2
            smallB = other.part2
            compB = other.part1
        elif cond5:
            smallA = other.part1
            smallB = self.part1
            compB = self.part2
        elif cond6:
            smallA = other.part1
            smallB = self.part2
            compB = self.part1
        elif cond7:
            smallA = other.part2
            smallB = self.part1
            compB = self.part2
        elif cond8:
            smallA = other.part2
            smallB = self.part2
            compB = self.part1
        X = smallA.complement(rel=smallB.pitches)
        result = []
        options = smallA.abstract_tto(compB)
        for opt in options:
            opt = Pcset([x for x in compB if x in opt])
            Y = opt.complement(compB)
            result.append([smallA, X, Y, opt])
        return result

    def k_abstract(self, other):
        ''' Diz se self e other estão em relação K abstrata '''
        if (self.join_partitions() == Pcset(list(range(12)))) and (other.join_partitions() == Pcset(list(range(12)))):
            
            cond1 = self.part1.abstract_included(other.part1)
            cond2 = self.part1.abstract_included(other.part2)
            cond3 = self.part2.abstract_included(other.part1)
            cond4 = self.part2.abstract_included(other.part2)
            cond5 = other.part1.abstract_included(self.part1)
            cond6 = other.part1.abstract_included(self.part2)
            cond7 = other.part2.abstract_included(self.part1)
            cond8 = other.part2.abstract_included(self.part2)
            if cond1 or cond2 or cond3 or cond4 or cond5 or cond6 or cond7 or cond8:
                return True
            return False
        return False

    def kh_abstract(self, other):
        ''' Diz se self e other estão em relação Kh abstrata'''
        if (self.join_partitions() == Pcset(list(range(12)))) and (other.join_partitions() == Pcset(list(range(12)))):
            
            cond1 = self.part1.abstract_included(other.part1) and self.part1.abstract_included(other.part2)
            cond2 = self.part1.abstract_included(other.part2) and self.part1.abstract_included(other.part1)
            cond3 = self.part2.abstract_included(other.part1) and self.part2.abstract_included(other.part2)
            cond4 = self.part2.abstract_included(other.part2) and self.part2.abstract_included(other.part1)
            cond5 = other.part1.abstract_included(self.part1) and other.part1.abstract_included(self.part2)
            cond6 = other.part1.abstract_included(self.part2) and other.part1.abstract_included(self.part1)
            cond7 = other.part2.abstract_included(self.part1) and other.part2.abstract_included(self.part2)
            cond8 = other.part2.abstract_included(self.part2) and other.part2.abstract_included(self.part1)
            if cond1 or cond2 or cond3 or cond4 or cond5 or cond6 or cond7 or cond8:
                return True
            return False
        return False

    def k_complex(self):
        ''' Encontra o complexo de partições de 12 do agregado em relação k com self '''
        result = []
        for part in two_part_12:
            new_ccp = TwoPartition(part)
            if self.k_relation(new_ccp):
                result.append(new_ccp)
        return result
    
    def kh_complex(self):
        ''' Encontra o complexo de partições de 12 do agregado em relação kh com self '''
        result = []
        for part in two_part_12:
            new_ccp = TwoPartition(part)
            if self.kh_relation(new_ccp):
                result.append(new_ccp)
        return result
    
    def k_complex_abstract(self):
        ''' Encontra o complexo de partições de 12 do agregado em relação k abstrata com self '''
        result = []
        for part in two_part_12:
            new_ccp = TwoPartition(part)
            if self.k_abstract(new_ccp):
                result.append(new_ccp)
        return result
    
    def kh_complex_abstract(self):
        ''' Encontra o complexo de partições de 12 do agregado em relação kh abstrata com self '''
        result = []
        for part in two_part_12:
            new_ccp = TwoPartition(part)
            if self.kh_abstract(new_ccp):
                result.append(new_ccp)
        return result
