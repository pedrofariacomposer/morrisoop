from aux_f import *
from aux_f import _ALL_TTOS, _ALL_SET_OPS, _ALL_ROW_TTOS, _ALL_ROW_SET_OPS

class Pc:
    
    '''
    Classe para representar uma pitch class.
    
    Parâmetros:
    -----------
    pitch: int | Pc
        Numeral que indica a classe de altura

    '''
    
    def __init__(self, pitch: int):
        self.pitch = pitch
        self._clean_pitch()

    def _clean_pitch(self):
        if isinstance(self.pitch, Pc):
            self.pitch = self.pitch.pitch
            
    ##### Overloading #####

    def __repr__(self):
        if self.pitch in range(10):
            return f'{self.pitch}'
        elif self.pitch == 10:
            return "A"
        elif self.pitch == 11:
            return "B"
            
    def __eq__(self, other):
        return self.pitch == Pc(other).pitch
    
    def __add__(self, other):
        s1 = self
        s2 = Pc(other)
        return Pc((s1.pitch + s2.pitch) % 12)
    
    def __radd__(self, other):
        return self + other
    
    def __mul__(self, other):
        s1 = self
        s2 = Pc(other)
        return Pc((s1.pitch * s2.pitch) % 12)
    
    def __rmul__(self, other):
        return self * other
    
    def __sub__(self, other):
        return self + (-1 * other)
    
    def __rsub__(self, other):
        return (-1 * self) + other
    
    def __lt__(self, other):
        return self.pitch < Pc(other).pitch

    def __le__(self, other):
        return self.pitch <= Pc(other).pitch

    def __gt__(self, other):
        return self.pitch > Pc(other).pitch

    def __ge__(self, other):
        return self.pitch >= Pc(other).pitch
    
    def __len__(self):
        return 1
    
    ##### Métodos #####

    def transposition(self, n: int):
        ''' Aplica Tn a um Pc '''
        return self + n
    
    def multiplication(self, n: int = 5):
        ''' Aplica TnI a um Pc '''
        return self * n
                       
    def inversion(self, n: int = 0):
        ''' Aplica M a um Pc '''
        return (self * -1) + n
    
    def ip(self, other):
        ''' Encontra o invervalo ordenado entre dois Pcs '''
        return (Pc(other) - self).pitch
    
    def icn(self, other):
        ''' Encontra a classe de intervalo entre dois Pcs '''
        return min(self.ip(Pc(other)), Pc(other).ip(self))
        
    def tto(self, TTO: str):
        ''' Aplica uma TTO específica a um PC '''
        if TTO not in _ALL_TTOS:
            return None
        n = TTO[1]
        if n not in ["a", "A", "b", "B"]:
            n = int(n)
        else:
            if n in ["A", "a"]:
                n = 10
            else:
                n = 11
        if len(TTO) == 2:
            return self.transposition(n)
        elif len(TTO) == 3:
            if TTO[-1].lower() == "i":
                return self.inversion(n)
            elif TTO[-1].lower() == "m":
                return self.multiplication().transposition(n)
        elif len(TTO) == 4:
            return self.multiplication().inversion(n)

    def cycle_tto(self, TTO):
        if TTO[0] != "R":
            result = [self]
            a = self.tto(TTO)
            while a not in result:
                result.append(a)
                a = a.tto(TTO)
            return result
        else:
            return self.cycle_tto(TTO[1:])

##########################################################