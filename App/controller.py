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
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog(listType):
    
    catalog = model.newCatalog(listType)
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)
    
def loadArtists(catalog):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    artistsfile = cf.data_dir + 'MoMA (1)/Artists-utf8-large.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

def loadArtworks(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    artworksfile = cf.data_dir + 'MoMA (1)/Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8')) 
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def subListArtwork(catalog, ListSyze):
    """
    Genera la sublista de Artworks
    """
    ArtworkSample = model.subListArtwork(catalog, ListSyze)
    return ArtworkSample

# Funciones de ordenamiento

def sortDateArtwork(catalog, ordenamiento, ListSyze):
    return model.sortDateAcquired(catalog, ListSyze)

    
# Funciones de consulta sobre el catálogo

def getArtistByDate(catalog, BeginDate, EndDate): 
    a = model.getArtistByDate(catalog, BeginDate, EndDate)
    return a

def getartworkPurchased(catalog):
    p = model.artworksPurchased(catalog)
    return p

def getArtworksByDateAcquired(catalog, inicial, final):
    aDateAcquired = model.artworksByDate(catalog, inicial, final)
    return aDateAcquired 

def getArtworksByNationality(catalog):

    agetArtworksByNationality = model.getArtworksByNationality(catalog)
    return agetArtworksByNationality

def getArtistByTecnique(catalog, Artist):
    ArtistByTecnique = model.getArtistByTecnique(catalog, Artist)
    return ArtistByTecnique

def getArtworksByDepartment(catalog,department):
    agetArtworksByDepartment = model.getArtworksByDepartment(catalog,department)
    return agetArtworksByDepartment
