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
from DISClib.Algorithms.Sorting import mergesort as ms
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
    catalog['ArtworkMedium'] = mp.newMap(10000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareArtworkMedium)
    catalog['ArtistID'] = mp.newMap(34500,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareArtworkMedium)
    catalog['ArtworkID'] = mp.newMap(34500,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareArtworkMedium)
    catalog['ArtworkNationality'] = mp.newMap(300,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareArtworkMedium)
                            

    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):

    listArtist = {'DisplayName': (artist['DisplayName']).lower(),
                'ConstituentID': (artist['ConstituentID']).replace(" ", ""),
                'BeginDate': artist['BeginDate'], 
                'EndDate': artist['EndDate'],
                'Nationality': (artist['Nationality']).lower(),
                'Gender': artist['Gender']} 
    lt.addLast(catalog['Artists'], listArtist)
    addArtistID(catalog,listArtist['ConstituentID'],artist)

def addArtwork(catalog, artwork):

    listArtwork = {'ObjectID': (artwork['ObjectID']).replace(" ", ""), 
                  'Title': (artwork['Title']).lower(),
                  'ConstituentID': (artwork['ConstituentID']).replace(" ", ""),
                  'Date': artwork['Date'],
                  'Medium': (artwork['Medium']).lower(),
                  'Dimensions': artwork['Dimensions'],
                  'CreditLine': (artwork['CreditLine']).lower(),
                  'Classification': (artwork['Classification']).lower(),
                  'Department': (artwork['Department']).lower(),
                  'DateAcquired': artwork['DateAcquired'],
                  'URL': artwork['URL'],
                  'Circumference': artwork['Circumference (cm)'],
                  'Depth': artwork['Depth (cm)'],
                  'Diameter': artwork['Diameter (cm)'],
                  'Height': artwork['Height (cm)'],
                  'Length': artwork['Length (cm)'],
                  'Weight': artwork['Weight (kg)'],
                  'Width': artwork['Width (cm)']}
    lt.addLast(catalog['Artwork'], listArtwork)
    artistsID = listArtwork['ConstituentID']
    artistsID = eval(artistsID)
    addArtworkMedium(catalog, listArtwork['Medium'], artwork)

def addArtistID(catalog, constituentID, artist):

    mediums = catalog['ArtistID']
    existmedium = mp.contains(mediums, constituentID)
    if existmedium:
        entry = mp.get(mediums, constituentID)
        medium = me.getValue(entry)
    else:
        medium = newArtistid()
        mp.put(mediums, constituentID, medium)
    lt.addLast(medium['Artistinfo'], artist)

def addArtworkMedium(catalog, mediumName, artwork):

    ArtworkFiltrada = {'ObjectID': (artwork['ObjectID']).replace(" ", ""), 
                  'Title': (artwork['Title']).lower(),
                  'ConstituentID': (artwork['ConstituentID']).replace(" ", ""),
                  'Date': artwork['Date'],
                  'Medium': (artwork['Medium']).lower(),}
    
    mediums = catalog['ArtworkMedium']
    existmedium = mp.contains(mediums, mediumName)
    if existmedium:
        entry = mp.get(mediums, mediumName)
        medium = me.getValue(entry)
    else:
        medium = newMedium()
        mp.put(mediums, mediumName, medium)
    lt.addLast(medium['Artworks'], ArtworkFiltrada)
 

# Funciones de consulta

#Opcion2:
def getArtworksMedium(catalog, medium):
    medium = mp.get(catalog['ArtworkMedium'], medium)
    if medium:
        list_artworks= me.getValue(medium)
        sortByYears(list_artworks['Artworks'])
        return list_artworks['Artworks']
    return None

def getArtistID(catalog, artwork):
    artist_value = mp.get(catalog['ArtistID'], artwork)
    if artist_value:
        list_artworks= me.getValue(artist_value)
        return list_artworks['Artistinfo']
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

def newMedium():
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    medium = {"Artworks": None}
    medium['Artworks'] = lt.newList('ARRAY_LIST', compareArtworkMedium)
    return medium
def newArtistid():
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    medium = {"Artistinfo": None}
    medium['Artistinfo'] = lt.newList('ARRAY_LIST', compareArtworkMedium)
    return medium

# Funciones utilizadas para comparar elementos dentro de una lista

def compareartists(a1, a2):
    
    if a1 < int(a2['ConstituentID']):
        return -1
    elif a1 == int(a2['ConstituentID']):
        return 0
    else:
        return 1
    
def compareArtworkMedium(medium, entry):
    mediumentry = me.getKey(entry)
    if (medium == mediumentry):
        return 0
    elif (medium > mediumentry):
        return 1
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
    return int(year1['Date']) < int(year2['Date'])

# Funciones de ordenamiento

def sortByYears(list_artworks):
    return ms.sort(list_artworks, compareYears)

