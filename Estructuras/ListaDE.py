class doublemente_Enlazada():

    def __init__(self):
        self.cabeza : Nodo = None
        self.final  : Nodo = None
    
    def agregar_al_inicio(self,dato):
        
        nodo_nuevo = Nodo(dato)
        
        if self.final != None:
            nodo_nuevo.anterior = self.final
            self.final.siguiente = nodo_nuevo
            self.final = nodo_nuevo
            return
        
        self.cabeza = nodo_nuevo
        self.final  = nodo_nuevo
    
    
    
class Nodo():
    def __init__(self,dato ):
        self.dato = dato
        self.siguiente : Nodo = None
        self.anterior : Nodo = None