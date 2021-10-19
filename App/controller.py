"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import config as cf
import model
import csv


"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import config as cf
import model
import csv
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtworks(catalog)
    loadArtists(catalog)
    
def loadArtists(catalog):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    artistsfile = cf.data_dir + 'MoMA/Artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

def loadArtworks(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8')) 
    for artwork in input_file:
        model.addArtwork(catalog, artwork)
        
def getArtworksMedium(catalog, medium):
     artworks = model.getArtworksMedium(catalog, medium)
     return artworks

#Req 1
#---------------------------------------------------------------
def getArtistByDate(catalog, anoInicial, anoFinal):
    return model.getArtistByDate(catalog, anoInicial, anoFinal)

#Req 2:
#---------------------------------------------------------------
def getArtworksByDateAcquired(catalog, Inicial, Final):
    return model.getArtworksDate(catalog, Inicial, Final)

def getartworkPurchased(datesArtworks):
    return model.getartworkPurchased(datesArtworks)

#Req 3:
#---------------------------------------------------------------
def getArtworksMedium(catalog, artisName):
    return model.getArtworksMedium(catalog, artisName)


#Req 4
#---------------------------------------------------------------
def getArtworksNationality(catalog):
    return model.getArtworkNationality(catalog)
def getArtworksOneNat(catalog, nationality):
    return model.getArtworksOneNat(catalog, nationality)
#---------------------------------------------------------------
#Req 5
#---------------------------------------------------------------
def getArtworksByDepartment(catalog,dep):
    return model.getArtworksByDepartment(catalog,dep)

#---------------------------------------------------------------

#Aux
#---------------------------------------------------------------
def getArtists(catalog, artwork):
    return model.getArtists(catalog, artwork)
#---------------------------------------------------------------