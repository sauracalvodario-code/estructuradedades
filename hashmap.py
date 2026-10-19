class MyHashMap:
    def __init__(self, cap=13):
        self._table = cap * [None]   
        self._n = 0                  

    def _hash_function(self, key):
        return key % len(self._table) 

    # ----- Mètodes d'Alt Nivell -----

    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)
        self._bucket_put(j, key, value)
        
        # Part 2: Rehashing (factor de càrrega > 0.5)
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._hash_function(key)
        return self._bucket_get(j, key)

    def remove(self, key: int) -> None:
        j = self._hash_function(key)
        self._bucket_remove(j, key)

    def __len__(self):
        return self._n

    # ----- Mètodes Auxiliars dels Buckets (Nivell 2) -----

    def _bucket_put(self, j, key, value):
        # Si està buit, instanciem el bucket i afegim.
        if self._table[j] is None:
            self._table[j] = []
            self._table[j].append([key, value])
            self._n += 1
            return
            
        # Si ja hi ha bucket, cerquem si la clau ja existeix.
        for parella in self._table[j]:
            if parella[0] == key:
                parella[1] = value # Actualitzem valor existent
                return
                
        # Si hem iterat tot el bucket i la clau no hi era (col·lisió nova).
        self._table[j].append([key, value])
        self._n += 1

    def _bucket_get(self, j, key):
        if self._table[j] is None:
            return -1
            
        # Cerca seqüencial dins del bucket.
        for parella in self._table[j]:
            if parella[0] == key:
                return parella[1]
                
        return -1

    def _bucket_remove(self, j, key):
        if self._table[j] is None:
            return
            
        for i in range(len(self._table[j])):
            if self._table[j][i][0] == key:
                self._table[j].pop(i) # Extraiem l'element del bucket
                self._n -= 1
                return

    # ----- Part 2: Mètode de Rehashing -----

    def _resize(self, c):
        # Guardem referència a la taula vella
        taula_antiga = self._table
        
        # Generem la nova estructura i reiniciem els valors per evitar sumar dobles.
        self._table = c * [None]
        self._n = 0
        
        # Iterem l'estructura antiga per reinserir cada dada recalada a la nova.
        for bucket in taula_antiga:
            if bucket is not None:
                for parella in bucket:
                    # 'put' automàticament calcularà el nou j respecte a la nova capacitat.
                    self.put(parella[0], parella[1])