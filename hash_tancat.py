LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"

class MyHashMap:
    """Taula de hash amb adreçament obert i sondeig lineal."""

    def __init__(self, cap=13):
        self._table = [[None, None, LLIURE] for _ in range(cap)]
        self._n = 0

    def _hash_function(self, key):
        return key % len(self._table)

    def _find(self, key):
        """
        Retorna la posició de la clau si la troba (OCUPAT), o None si no hi és.
        Continua la cerca passant per les posicions ESBORRAT.
        """
        M = len(self._table)
        j = self._hash_function(key)
        
        for i in range(M):
            idx = (j + i) % M
            
            if self._table[idx][2] == LLIURE:
                return None
            elif self._table[idx][2] == OCUPAT and self._table[idx][0] == key:
                return idx
                
        return None

    def put(self, key: int, value: int) -> None:
        M = len(self._table)
        j = self._hash_function(key)
        
        primer_esborrat = None
        
        for i in range(M):
            idx = (j + i) % M
            
            if self._table[idx][2] == ESBORRAT:
                if primer_esborrat is None:
                    primer_esborrat = idx
            
            elif self._table[idx][2] == OCUPAT and self._table[idx][0] == key:
                self._table[idx][1] = value
                return
                
            elif self._table[idx][2] == LLIURE:
                pos = primer_esborrat if primer_esborrat is not None else idx
                self._table[pos] = [key, value, OCUPAT]
                self._n += 1
                
                if self._n > M // 2:
                    self._resize(2 * M - 1)
                return
                
        if primer_esborrat is not None:
            self._table[primer_esborrat] = [key, value, OCUPAT]
            self._n += 1
            if self._n > M // 2:
                self._resize(2 * M - 1)

    def get(self, key: int) -> int:
        idx = self._find(key)
        if idx is not None:
            return self._table[idx][1]
        return -1

    def remove(self, key: int) -> None:
        idx = self._find(key)
        if idx is not None:
            self._table[idx] = [None, None, ESBORRAT]
            self._n -= 1

    def __len__(self):
        return self._n

    def _resize(self, c):
        taula_antiga = self._table
        self._table = [[None, None, LLIURE] for _ in range(c)]
        self._n = 0
        
        for casella in taula_antiga:
            if casella[2] == OCUPAT:
                self.put(casella[0], casella[1])