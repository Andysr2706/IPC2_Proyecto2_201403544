import re
import codecs
import os
from tkinter import *
from tkinter import filedialog

def LeerArchivo():
    filename    = filedialog.askopenfilename(initialdir = "/", title = "Seleccione el archivo", filetypes = (("XML Files", "*.xml*" ), ("All files", "*.*")))
    
    RutaArchivo = str(filename)


    return RutaArchivo
