import Funciones.BusquedaDeArchivos as BuscadorArchivos
import Estructuras.ListaSimple as ListaSimple
import sys
import os
from xml.dom import minidom
import xml.etree.cElementTree as ET
import Objetos.ElementoQuimico as ElementoQuimico
import Objetos.Pin as Pin
import Objetos.Maquina as Maquina
from graphviz import Digraph

class menu:

    ListaElementos        = ListaSimple.Lista_simple()
    ListaMaquinas         = ListaSimple.Lista_simple()
    ListaCompuestos       = ListaSimple.Lista_simple()

    ListaElementos.cabeza = None


    
    def menuprincipal():
        ruta = ''

        print("\n-----------------------Proyecto 2 IPC 2-----------------------")
        print("            Andy Jeferson Salas Ramirez 201403544")

        CondicionMenu = True
        SeleccionMenu = 0

        while CondicionMenu == True:
            print("-------------------------------------------------------")
            print("Seleccione la opcion a utilizar:")
            print("1. Cargar XML")
            print("2. Analizar Archivo XML.")
            print("3. Ver lista de elementos quimicos.")
            print("4. Agregar un elemento quimico nuevo.")
            print("5. Ver listado de compuestos.")
            print("6. Ver listado de maquinas.")
            print("7. Graficar instrucciones para realizar compuestos.")
            print("8. acerca de.")
            print("9. Salir.\n")

            SeleccionMenu = int(input())

            if SeleccionMenu ==1:
               
                print("-------------------------------------------------------")
                print("Busque el archivo:") 
                ruta = ''
                
                
                ruta = BuscadorArchivos.LeerArchivo()
                
                print('Archivo encontrado en: '+ruta)


                

                print("Desea Continuar: S/N")
                SeleccionMenu = input()

                if SeleccionMenu == 's' or SeleccionMenu == 'S':
                    CondicionMenu ==True
                elif SeleccionMenu == 'n' or SeleccionMenu == 'N': 
                    print("Gracias por utilizar el programa")
                    CondicionMenu == False
                    sys.exit()
            
            
            if SeleccionMenu == 2:
                archivo = minidom.parse(ruta)
                menu.procesarInformacion(archivo)
            
                
            if SeleccionMenu == 3:
               menu.graficarTablaElementos() 
            
            if SeleccionMenu == 4:
                menu.agregarCeldaViva()
            
            if SeleccionMenu == 5:
                menu.generarXML()

            if SeleccionMenu == 6:
                sys.exit()



    def procesarInformacion(archivoXML):

        menu.ListaMaquinas.cabeza   = None
        menu.ListaCompuestos.cabeza = None

        elementospin = 0

        ElementosXML = archivoXML.getElementsByTagName('elemento')
        
        try:

            for elemento in ElementosXML:
                NumeroAtomico  = elemento.childNodes[1].firstChild.data
                Simbolo        = elemento.childNodes[3].firstChild.data
                NombreElemento = elemento.childNodes[5].firstChild.data

                #print(NumeroAtomico+' '+ Simbolo+' '+ NombreElemento)

                nuevoElemento  = ElementoQuimico.ElementoQuimico(NumeroAtomico, Simbolo, NombreElemento)

                menu.ListaElementos.agregar_al_inicio(nuevoElemento)

        except IndexError:
            pass

        

              
    def AgregarElementoQuimico():

        

        print("\n ingrese numero atomico.")
        numeroA: input()

        print("\n ingrese Simbolo")
        simboloA: input()
        
        print("\n ingrese nombre del elemento")
        NombreE: input()
        
        ListaAuxiliar = menu.ListaElementos.cabeza

        while ListaAuxiliar != None:
            if numeroA == ListaAuxiliar.dato.NumeroAtomico or simboloA == ListaAuxiliar.dato.Simbolo or NombreE == ListaAuxiliar.dato.NombreElemento:
                print('No se puede agregar un elemento ya existente en la lista.')
                ListaAuxiliar = ListaAuxiliar.siguiente

            else:
                nuevoElemento  = ElementoQuimico.ElementoQuimico(numeroA, simboloA, NombreE)
                menu.ListaElementos.agregar_al_inicio(nuevoElemento)
                break



    def ordenarListaElementos(cabeza):
        nodolista           = ListaSimple.Nodo(None)
        nodolista.siguiente = cabeza
        
        NumeroAtomicoActual    = 0
        NumeroAtomicoSiguiente = 0
        ExisteOrden            = True

        while ExisteOrden:
            ExisteOrden  = False
            nodotemporal = nodolista
            
            while nodotemporal.siguiente and nodotemporal.siguiente.siguiente:

                primero = nodotemporal.siguiente
                segundo = primero.siguiente

                NumeroAtomicoActual    = int(primero.dato.NumeroAtomico)
                NumeroAtomicoSiguiente = int(segundo.dato.NumeroAtomico)


                if NumeroAtomicoActual > NumeroAtomicoSiguiente :
                    nodotemporal.siguiente = segundo
                    primero.siguiente      = segundo.siguiente
                    segundo.siguiente      = primero
                    ExisteOrden = True 
                nodotemporal = nodotemporal.siguiente
            
        cabeza = nodolista.siguiente

        return cabeza

    def graficarTablaElementos():

        menu.ListaElementos.cabeza = menu.ordenarListaElementos(menu.ListaElementos.cabeza)

        dot = Digraph(comment= "Tabla de Elementos quimicos")
        
        dot.attr('node', shape='none', fontname = 'calibri')
        codigoGraphviz = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR><TD colspan = "3" bgcolor="#45ff8c">Tabla de Elementos Quimicos</TD></TR>
  <TR>
  <TD bgcolor="#adffcd">Numero atomico</TD>
  <TD bgcolor="#adffcd">Simbolo</TD>
  <TD bgcolor="#adffcd">Elemento</TD>
  </TR>'''
        
        nodo = menu.ListaElementos.cabeza

        while nodo != None:
            codigoGraphviz = codigoGraphviz + '''<TR>
            <TD>'''+nodo.dato.NumeroAtomico +'''</TD>
            <TD>'''+nodo.dato.Simbolo +'''</TD>
            <TD>'''+nodo.dato.NombreElemento +'''</TD>
            </TR>'''
            nodo = nodo.siguiente

        codigoGraphviz = codigoGraphviz + '''</TABLE>>'''
        
        dot.node('tabla de elementos quimicos', codigoGraphviz)
        dot.render('./renders/tablaelementos.gv', view = True)