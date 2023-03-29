import BusquedaDeArchivos as BuscadorArchivos
import Estructuras.ListaSimple as ListaSimple
import sys
import os
from xml.dom import minidom
import xml.etree.cElementTree as ET
import Muestra as muestraactual
import OrganismoVivo as OrganizmoV
import Organismo as OrganismoN
from graphviz import Digraph
from Generadordecolores import generarcolor

class menu:

    muestraAnalizada:muestraactual

    ListaOrganizmos      = ListaSimple.Lista_simple()
    ListaOrganizmosVivos = ListaSimple.Lista_simple()

    
    def menuprincipal():
        #os.system("cls")
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
            print("3. Graficar muestra.")
            print("4. Ingresar organizmo vivo en muestra.")
            print("5. Crear un archivo XML nuevo.")
            print("6. Salir.\n")

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
               menu.graficarMuestra() 
            
            if SeleccionMenu == 4:
                menu.agregarCeldaViva()
            
            if SeleccionMenu == 5:
                menu.generarXML()

            if SeleccionMenu == 6:
                sys.exit()





    def procesarInformacion(archivoXML):

        menu.ListaOrganizmos.cabeza = None
        menu.ListaOrganizmosVivos.cabeza = None
        
        coleccionX  = archivoXML.getElementsByTagName('filas')
        coleccionY  = archivoXML.getElementsByTagName('columnas')
        muestra     = archivoXML.getElementsByTagName('muestra')

        codigoMuestra       = muestra[0].childNodes[1].firstChild.data 
        descripcionMuestra  = muestra[0].childNodes[3].firstChild.data 

        dimensionX = coleccionX[0].childNodes[0].data
        dimensionY = coleccionY[0].childNodes[0].data

        if (int(dimensionX)> 10000 or int(dimensionY) > 10000):
            print('La dimension de la muestra es demasiado grande, ingrese un archivo que tenga dimensiones mas pequeñas:\n')

        else:
              
            nuevaMuestra  =  muestraactual.Muestra(codigoMuestra,descripcionMuestra,dimensionX,dimensionY)

            organismosXML = archivoXML.getElementsByTagName('organismo')

            for organismo in organismosXML:

                codigo = organismo.childNodes[1].firstChild.data
                nombre = organismo.childNodes[3].firstChild.data
                color = generarcolor()

                #print(codigo + ' '+ nombre + '  ' + color)

                nuevoOrganismo = OrganismoN.Organismo(codigo,nombre,color)
                menu.ListaOrganizmos.agregar_al_inicio(nuevoOrganismo)

            celdasVivasXML = archivoXML.getElementsByTagName('celdaViva')

            if(len(celdasVivasXML)>1000):
                print('Error: la muestra tiene mas de 1000 celdas vivas, ingrese una muestra con menos muestras vivas:\n')
            else:
                    

                for celdaViva in celdasVivasXML:

                    fila            = celdaViva.childNodes[1].firstChild.data
                    columna         = celdaViva.childNodes[3].firstChild.data
                    codigoOrganismo = celdaViva.childNodes[5].firstChild.data

                    
                    colorV = ''

                    listaorganizmos = menu.ListaOrganizmos
                    nodo = listaorganizmos.cabeza

                    while nodo !=None:
                        if codigoOrganismo == nodo.dato.codigo:
                            colorV = nodo.dato.color
                            break

                        else:
                            colorV = ''
                            nodo   = nodo.siguiente



                    nuevaCeldaViva  = OrganizmoV.OrganismoVivo(codigoOrganismo,fila,columna,colorV)

                    

                    menu.ListaOrganizmosVivos.agregar_al_inicio(nuevaCeldaViva)

                menu.muestraAnalizada = nuevaMuestra
        


    def graficarMuestra():

        x   = menu.muestraAnalizada.DimensionX
        y   = menu.muestraAnalizada.DimensionY

        dot = Digraph(comment= "Tabla de muestra")
        
        dot.attr('node', shape='record')
        dot.attr(label="Tabla de muestras con: Filas: "+x+" Columnas: "+ y)

        codigoGraphviz = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>'''
        
        codigoColores = '''<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'''

        cuentaX = 0
        cuentaY = -1
        while (cuentaX <= int(x)):
            if(cuentaY == -1):
                codigoGraphviz = codigoGraphviz+'''
                <TD bgcolor='lightgrey'>X,Y</TD>'''
            else:
                codigoGraphviz = codigoGraphviz+'''
                    <TD bgcolor='lightgrey'>'''+str(cuentaX-1)+'</TD>'
            
            cuentaY = 0
            
            while (cuentaY < int(y)):
                
                if(cuentaX == 0):
                    codigoGraphviz = codigoGraphviz+'''
                    <TD bgcolor='lightgrey'>'''+str(cuentaY)+'</TD>'
                else:
                    listaceldasv = menu.ListaOrganizmosVivos
                    nodoActual = listaceldasv.cabeza

                    codigoOrganizmo = ''

                    while nodoActual !=None:

                        CeldaViva:OrganizmoV.OrganismoVivo = nodoActual.dato
                        coordenadaX = CeldaViva.x
                        coordenadaY = CeldaViva.y

                        if(int(cuentaX-1) == int(coordenadaX) and int(cuentaY) == int(coordenadaY)):
                            codigoOrganizmo = '''
                            <TD bgcolor="'''+CeldaViva.color +'''">   </TD>'''
                            break
                        else:

                            codigoOrganizmo = '''
                            <TD>'''+"   "+'</TD>'
                        nodoActual = nodoActual.siguiente

                    codigoGraphviz = codigoGraphviz + codigoOrganizmo
                            
                cuentaY = cuentaY + 1
            
            cuentaX = cuentaX + 1
            
            if(cuentaX-1 == int(x)):
                codigoGraphviz = codigoGraphviz+'''
                </TR>'''
            else:
                codigoGraphviz = codigoGraphviz+'''
                </TR>
                <TR>'''

        codigoGraphviz = codigoGraphviz+ '''
</TABLE>>'''


        listaorganizmos = menu.ListaOrganizmos
        nodo = listaorganizmos.cabeza

        while nodo !=None:
            codigoColores = codigoColores + '''<TR>
            <TD>'''+nodo.dato.nombre +'''</TD>
            <TD bgcolor="'''+nodo.dato.color +'''">   </TD>
            
            </TR>''' 
            nodo = nodo.siguiente

        codigoColores =codigoColores+ '''
</TABLE>>'''


        
        dot.node('tabla de organismos', codigoGraphviz)

        dot.node('tabla de colores', codigoColores)



        dot.render('./renders/tabla.gv', view=True)

        
    def agregarCeldaViva():

        x  = -1
        y  = -1
        xv =  0
        yv =  0
        codigoOrganizmo      = ''
        colorOrganizmo       = ''
        listaorganizmosvivos = menu.ListaOrganizmosVivos
        listaorganizmos      = menu.ListaOrganizmos
        nodo                 = listaorganizmos.cabeza
        nodovivos            = listaorganizmosvivos.cabeza

        print("Ingrese el codigo del organizmo: ")
        codigoOrganizmo = str(input())
        while nodo !=None:
            if nodo.dato.codigo == codigoOrganizmo :
                colorOrganizmo = nodo.dato.color
                print("ingrese coordenada en X:")
                x=int(input())

                print("ingrese coordenada en Y:")
                y=int(input())

                while(nodovivos != None):
                    xv = int(nodovivos.dato.x)
                    yv = int(nodovivos.dato.y)

                    if(x==xv and y==yv):
                        
                        x = -2
                        y = -2
                        break
                    else:
                        nodovivos = nodovivos.siguiente
                
                break
            else:
                nodo = nodo.siguiente

        if(x==-1 or y==-1):
            print("Codigo del organizmo no existe, ingrese un organizmo que exista en la muestra")

        elif(x==-2 or y==-2):
            print("no se puede ingresar un organizmo vivo donde se encuentra un organizmo vivo actualmente")
        else:

            nuevaceldaviva = OrganizmoV.OrganismoVivo(codigoOrganizmo,x,y,colorOrganizmo)
            menu.ListaOrganizmosVivos.agregar_al_inicio(nuevaceldaviva)
            print("Organizmo vivo ingresado exitosamente!\n")


    def generarXML():

        listaOrganismos  = menu.ListaOrganizmos
        listaCeldasVivas = menu.ListaOrganizmosVivos
        nodoOrganismos   = listaOrganismos.cabeza
        nodoCeldasVivas  = listaCeldasVivas.cabeza
        m_encoding = 'UTF-8'

        root = ET.Element("datosMarte")
        doc  = ET.SubElement(root, 'listaOrganismos')
        
        while nodoOrganismos != None:
            org = ET.SubElement(doc, "organismo")
            ET.SubElement(org, 'codigo').text = str(nodoOrganismos.dato.codigo)
            ET.SubElement(org, 'nombre').text = str(nodoOrganismos.dato.nombre)

            nodoOrganismos = nodoOrganismos.siguiente

        doc2     = ET.SubElement(root, 'listadoMuestras')
        muestraA = ET.SubElement(doc2, 'muestra')
        ET.SubElement(muestraA, 'codigo').text      = str(menu.muestraAnalizada.codigo)
        ET.SubElement(muestraA, 'descripcion').text = str(menu.muestraAnalizada.descripcion)
        ET.SubElement(muestraA, 'filas').text       = str(menu.muestraAnalizada.DimensionX)
        ET.SubElement(muestraA, 'columnas').text    = str(menu.muestraAnalizada.DimensionY)
        listadoCV = ET.SubElement(muestraA, 'listadoCeldasVivas')

        
        while nodoCeldasVivas != None :
            CV = ET.SubElement(listadoCV, 'celdaViva')
            ET.SubElement(CV, 'fila').text            = str(nodoCeldasVivas.dato.x)
            ET.SubElement(CV, 'columna').text         = str(nodoCeldasVivas.dato.y)
            ET.SubElement(CV, 'codigoOrganismo').text = str(nodoCeldasVivas.dato.organismo)

            nodoCeldasVivas = nodoCeldasVivas.siguiente
        

        dom = minidom.parseString(ET.tostring(root))
        xml_string   = dom.toprettyxml()
        part1, part2 = xml_string.split('?>')

        with open("./XML/Muestranueva.XML", 'w') as xfile:
            xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
            xfile.close()
           
        print("Archivo XML generado en la carpeta XML")

             


        
        