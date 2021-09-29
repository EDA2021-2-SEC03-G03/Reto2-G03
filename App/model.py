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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
"""


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import time
from datetime import date

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    
    catalog = {'Artwork': None,
               'Artists': None,
               'ArtworkMedium': None}

    catalog['Artists'] = lt.newList(cmpfunction=compareartists) 
    catalog['Artwork'] = lt.newList(cmpfunction=compareartworks)
    catalog['ArtworkIds'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareartworks)
    catalog['ArtworkMedium'] = mp.newMap(40,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareArtworkMedium)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    
    lt.addLast(catalog['Artworks'], artwork)
    mp.put(catalog['ArtworkIds'], artwork['ObjectID'], artwork)
    #artists = artwork['Artists'].split(",")  # Se obtienen los autores
    #for artist in artists:
        #addBookAuthor(catalog, artist.strip(), book)
    addArtworkMedium(catalog, artwork) 


def newMedium(medartwork):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'Medium': "", "Artworks": None}
    entry['Medium'] = medartwork
    entry['Artworks'] = lt.newList('SINGLE_LINKED', compareArtworkMedium)
    return entry
def addArtworkMedium(catalog, artwork):
    """
    Esta funcion adiciona un libro a la lista de libros que
    fueron publicados en un año especifico.
    Los años se guardan en un Map, donde la llave es el año
    y el valor la lista de libros de ese año.
    """
    try:
        meme = catalog['Medium']
        if (artwork['Medium'] != ''):
            medartwork = artwork['Medium']
        else:
            medartwork = "Unknown"
        existmedium = mp.contains(meme, medartwork)
        if existmedium:
            entry = mp.get(meme, medartwork)
            medium = me.getValue(entry)
        else:
            medium = newMedium(medartwork)
            mp.put(meme, medartwork, medium)
        lt.addLast(medium['Medium'], artwork)
    except Exception:
        return None

# Funciones para creacion de datos

def newArtist(artistid):
    artist= {'artistID': '',
             'Artworks': None,}
    artist['artistID'] = artistid

    artist['Artworks'] = lt.newList('ARRAY_LIST')

    return artist

def newArtistDate(artist, BeginDate, EndDate, nationality, gender):
    artistDate = {'Name': '', 'BeginDate': '', 'EndDate': '', 'Nationality': '', 'Gender': ''}
    artistDate['Name'] = artist
    artistDate['BeginDate'] = BeginDate
    artistDate['EndDate'] = EndDate
    artistDate['Nationality'] = nationality
    artistDate['Gender'] = gender

    return artistDate
    
def getArtworksMedium(catalog, medium):
    medium = mp.get(catalog['ArtworkMedium'], medium)
    if medium:
        return me.getValue(medium)['Artworks']
    return None


# Funciones utilizadas para comparar elementos dentro de una lista

def compareartists(a1, a2):
    
    if a1 < int(a2['ConstituentID']):
        return -1
    elif a1 == int(a2['ConstituentID']):
        return 0
    else:
        return 1
def compareArtworkMedium(a1,a2):
    if a1['Medium'].lower() == a2['Medium'].lower():
        return 0
    else:
        return -1 
def compareartworks(a1, a2):
    if int(a1['ObjectID']) < int(a2['ObjectID']):
        return -1
    elif int(a1['ObjectID']) == int(a2['ObjectID']):
        return 0
    else:
        return 1

def compareartistID(a1, artist):
    if str(a1) in str(artist['ConstituentID']):
        return 0
    else:
        return -1  

def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return 0

# Funciones de ordenamiento

