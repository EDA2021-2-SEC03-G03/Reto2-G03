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
    catalog['ArtworkMedium'] = mp.newMap(8000,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareArtworkMedium)
    catalog['ArtistID'] = mp.newMap(34500,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareArtworkMedium)
    catalog['ArtworksofArtist'] = mp.newMap(15250,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareArtworkMedium)
    catalog['ArtistsDates'] = mp.newMap(10000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareArtworkMedium)
    catalog['ArtworkNationality'] = mp.newMap(200,
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
    addArtistNationality(catalog,listArtist['Nationality'],artist)

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
    list_tutu = artwork["ConstituentID"].replace("[","").replace("]","").replace(" ","").split(",")
    for artist in list_tutu:
        addArtworkofArtist(catalog, artist,artwork)
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
    medium['Artistinfo'] = artist

def addArtworkofArtist(catalog,artist,artwork):
    mediums = catalog['ArtworksofArtist']
    existmedium = mp.contains(mediums, artist)
    if existmedium:
        entry = mp.get(mediums, artist)
        medium = me.getValue(entry)
    else:
        medium = newArtworkofArtist()
        mp.put(mediums, artist, medium)
    lt.addLast(medium['Artworks'], artwork)

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
def addArtistDate(catalog, beginDate, artists):
    ArtistFiltrada = {'DisplayName': artists['DisplayName'], 
                'ConstituentID': (artists['ConstituentID']).replace(" ", ""),
                'BeginDate': artists['BeginDate'], 
                'EndDate': artists['EndDate'],
                'Nationality': (artists['Nationality']).lower(),
                'Gender': artists['Gender']}
    dates = catalog['ArtistDates']
    existdate = mp.contains(dates, beginDate)
    if existdate:
        entry = mp.get(dates, beginDate)
        d = me.getValue(entry)
    else:
        d = newArtistDate()
        mp.put(dates, beginDate, d)
    lt.addLast(d['Artist'], ArtistFiltrada)

 
def addArtistNationality(catalog,nationality,artist):
    if nationality == None or nationality == "" or nationality == " " or nationality == "Nationality unknown" or nationality == "0":
        nationality = "Unknown"
    mediums = catalog['ArtworkNationality']
    existmedium = mp.contains(mediums, nationality)
    artworks = getArtworkofArtist(catalog,artist["ConstituentID"])
    if existmedium:
        entry = mp.get(mediums, nationality)
        medium = me.getValue(entry)
    else:
        medium = newNationality()
        mp.put(mediums, nationality, medium)
    if artworks != None:
        for artwork in lt.iterator(artworks):   
            lt.addLast(medium['Artworks'], artwork)
# Funciones de consulta

#Lab 6:
def getArtworksMedium(catalog, medium):
    medium = mp.get(catalog['ArtworkMedium'], medium)
    if medium:
        list_artworks= me.getValue(medium)
        sortByYears(list_artworks['Artworks'])
        return list_artworks['Artworks']
    return None

def getArtistID(catalog, artistID):
    artist_value = mp.get(catalog['ArtistID'], artistID)
    if artist_value:
        list_artworks= me.getValue(artist_value)
        return list_artworks['Artistinfo']
    return None

def getArtworkofArtist(catalog, artistID):
    artist_value = mp.get(catalog['ArtworksofArtist'], artistID)
    if artist_value:
        list_artworks= me.getValue(artist_value)
        return list_artworks['Artworks']
    return None

#Req 1
def getArtistByDate(catalog, anoInicial, anoFinal):
    start_time = time.process_time()
    
    list_artistDate = lt.newList('ARRAY_LIST', )
    for a in catalog['ArtistsDates']:
        if int(a['BeginDate']) >= anoInicial and int(a['BeginDate']) <= anoFinal and a['BeginDate'] != "" and a['BeginDate'] != 0:
                lt.addLast(list_artistDate, a)


    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000        
    return list_artistDate, elapsed_time_mseg
      
#Lab 6:
def getArtworkNationality(catalog, nationality):
    artist_value = mp.get(catalog['ArtworkNationality'], nationality)
    if artist_value:
        list_artworks= me.getValue(artist_value)
        return list_artworks['Artworks']
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
    Esta funcion crea la estructura de obras de arte asociados
    a un medio.
    """
    medium = {"Artworks": None}
    medium['Artworks'] = lt.newList('ARRAY_LIST', compareArtworkMedium)
    return medium

def newArtistDate():
    Date = {"Artists": None}
    Date['Artists'] = lt.newList('ARRAY_LIST', compareArtworkMedium)
    return Date

def newArtworkofArtist():
    """
    Esta funcion crea la estructura de artistas asociados
    a un ConstituentID.
    """
    medium = {"Artworks": None}
    medium['Artworks'] = lt.newList('ARRAY_LIST', compareArtworkMedium)
    return medium

def newNationality():
    """
    Esta funcion crea la estructura de artistas asociados
    a un ConstituentID.
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

def cmpArtistsDate(date1, date):
    if str(date1) in str(date['BeginDate']):
        return 0
    else:
        return -1

# Funciones de ordenamiento

def sortByYears(list_artworks):
    return ms.sort(list_artworks, compareYears)

