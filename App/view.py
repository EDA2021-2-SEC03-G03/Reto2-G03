"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from typing import List
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time

defaul_time = 1000
sys.setrecursionlimit(defaul_time*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Las obras más antiguas para un medio específico")

catalog = None

#funciones de print


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        #listType = input('Ingrese el tipo de lista que quiere implementar (ARRAY_LIST o LINKED_LIST): ').upper()
        catalog = controller.initCatalog()
        controller.loadData(catalog)
        
        
        

    elif int(inputs[0]) == 2:
        medium = input("Buscando obras de arte con que medio?: ").lower()
        n_artworks = int(input('TOP? (número): '))
        artws = controller.getArtworksMedium(catalog, medium)
        if lt.size(artws) < n_artworks:
            n_artworks = lt.size(artws)
        artw_sublist = lt.subList(artws, 1, n_artworks)
        print('Las ' + str(n_artworks) + ' obras más antiguas del medio "' + medium + '" son:')
        for artws in lt.iterator(artw_sublist):
            print(artws)
    else:
        sys.exit(0)
sys.exit(0)
