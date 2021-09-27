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
from DISClib.Algorithms.Sorting import mergesort
assert cf
import time
from datetime import date

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(listType):
    
    catalog = {'Artwork': None,
               'Artists': None,
               'ArtistsDate': None,
               'ArtworksDateAcquired': None}
    catalog['Artists'] = lt.newList(listType,
                                    cmpfunction=compareartists) 
    catalog['Artwork'] = lt.newList(listType, cmpfunction=compareartworks)
    catalog['ArtistsDate'] = lt.newList(listType, cmpfunction='')
    catalog['ArtworksDateAcquired'] = lt.newList(listType, cmpfunction='')
    

    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):

    listArtist = {'DisplayName': artist['DisplayName'],
                'ConstituentID': artist['ConstituentID'],
                'BeginDate': artist['BeginDate'], 
                'EndDate': artist['EndDate'],
                'Nationality': artist['Nationality'],
                'Gender': artist['Gender'],
                'Artworks': lt.newList('ARRAY_LIST')} 
    
    lt.addLast(catalog['Artists'], listArtist)
    
    addArtistDate(catalog, listArtist)

def addArtwork(catalog, artwork):

    listArtwork = {'ObjectID': artwork['ObjectID'], 
                  'Title': artwork['Title'],
                  'Artist': lt.newList('ARRAY_LIST'),
                  'ConstituentID': artwork['ConstituentID'],
                  'Date': artwork['Date'],
                  'Medium': artwork['Medium'],
                  'Dimensions': artwork['Dimensions'],
                  'CreditLine': artwork['CreditLine'],
                  'Department': artwork['Department'],
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

    for a in artistsID:
        addArtworkArtist(catalog, a, listArtwork)
    addArtworkDAcquired(catalog, listArtwork)

def Artistinfo(catalog,artistsID):
    Artistsfound = lt.newList(datastructure='ARRAY_LIST')
    artistsIDList = artistsID.replace('[', '').replace(']', '').split(",")
    for artist in artistsIDList:
            pos = lt.isPresent(catalog["Artists"],int(artist))
            if pos > 0:
                final = lt.getElement(catalog["Artists"],int(pos))
                lt.addLast(Artistsfound,final["DisplayName"])
            else:
                continue
    return Artistsfound





def addArtworkArtist(catalog, artist_id, Artwork):
    
    artists = catalog['Artists']
    posartist = lt.isPresent(artists,artist_id)
    if posartist > 0:
        artist = lt.getElement(artists, posartist)
        
    else:
        artist = newArtist(artist_id)
        lt.addLast(artists, artist)
    
    lt.addLast(artist['Artworks'], Artwork)
    lt.addLast(Artwork['Artist'], artist['DisplayName'])
    

def addArtistDate(catalog, listArtist):
        addDate = newArtistDate(listArtist['DisplayName'], listArtist['BeginDate'], listArtist['EndDate'], 
                                listArtist['Nationality'], listArtist['Gender'])
        lt.addLast(catalog['ArtistsDate'], addDate)

def addArtworkDAcquired(catalog, listArtwork):
    addDateAcquired = newArtworksDateAcquired(listArtwork['ObjectID'], listArtwork['Title'], listArtwork['Artist'],listArtwork['Medium'], listArtwork['Dimensions'], listArtwork['Date'], listArtwork['DateAcquired'], listArtwork['CreditLine'])
    lt.addLast(catalog['ArtworksDateAcquired'], addDateAcquired)

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

def newArtworksDateAcquired(ObjectID, artwork, artistname, Medium, Dimensions, Date, DateAcquired, CreditLine):
    ArtworkDateAcquired = {'ObjectID': '', 'Title': '', 'ArtistsName': '', 'Medium': '', 'Dimensions': '',
    'Date':'', 'DateAcquired': ''}
    ArtworkDateAcquired['ObjectID'] = ObjectID
    ArtworkDateAcquired['Title'] = artwork 
    ArtworkDateAcquired['Artists'] = artistname
    ArtworkDateAcquired['Medium'] = Medium 
    ArtworkDateAcquired['Dimensions'] = Dimensions
    ArtworkDateAcquired['Date'] = Date 
    ArtworkDateAcquired['DateAcquired'] = DateAcquired
    ArtworkDateAcquired['CreditLine'] = CreditLine

    return ArtworkDateAcquired

def newTecnique(tecnique):
    artec = {'MediumName': '',
             'Artworks': lt.newList('ARRAY_LIST')}
    artec['MediumName'] = tecnique
    return artec

def newNationality(Nationality):
    artnat = {'Nationality': '',
             'Artworks': lt.newList('ARRAY_LIST')}
    artnat['Nationality'] = Nationality
    return artnat

def subListArtwork(catalog, ListSyze):
    """
    Genera la sublista de Artworks
    """
    ArtworkSample = lt.subList(catalog['Artwork'],1,ListSyze)
    return ArtworkSample

# Funciones de consulta

#Req1:
def getArtistByDate(catalog, BeginDate, EndDate):
    start_time = time.process_time()
    
    DatesArtist = lt.newList('ARRAY_LIST')

    for a in lt.iterator(catalog['ArtistsDate']): 
        if int(a['BeginDate']) >= BeginDate and int(a['BeginDate']) <= EndDate and a['BeginDate'] != "" and a['BeginDate'] != 0:
            lt.addLast(DatesArtist, a)

    Dates_Artist = SortDates(DatesArtist)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return Dates_Artist, elapsed_time_mseg

#Req2:
def artworksByDate(catalog, inicial, final):
    start_time = time.process_time()
    artworksDate = lt.newList('ARRAY_LIST')

    inicialDate = date.fromisoformat(inicial)
    finalDate = date.fromisoformat(final)

    for a in lt.iterator(catalog['ArtworksDateAcquired']):
        if a['DateAcquired'] != '' and a['DateAcquired']!='0':
            a1 = date.fromisoformat(a['DateAcquired'])
            if a1 >= inicialDate and a1 <= finalDate and a1 != '' and a1!='0':
                lt.addLast(artworksDate, a)
                

    sort_DateAcquired = sortDateAcquired(artworksDate)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return sort_DateAcquired, elapsed_time_mseg

def artworksPurchased(sort_DateAcquired):
    count = 0
    for a in lt.iterator(sort_DateAcquired):
        if 'purchase' in a['CreditLine'].lower():
            count += 1
    
    return count


#Req 3:
def getArtistByTecnique(catalog, Artistname):
    start_time = time.process_time()
    ArtistTecnique = lt.newList('ARRAY_LIST', cmpfunction=compATecnique)
    
    for artists in lt.iterator(catalog['Artists']):
        
        if artists['DisplayName'] == Artistname:
            for a in lt.iterator(artists['Artworks']):
                tecnique = a['Medium']
                pos = lt.isPresent(ArtistTecnique,tecnique)
                if pos > 0:
                    tec = lt.getElement(ArtistTecnique, pos)
                    lt.addLast(tec['Artworks'], a)
                else:
                    tec = newTecnique(a['Medium'])
                    lt.addLast(ArtistTecnique, tec)
                lt.addLast(tec['Artworks'], a) 
              
    sort_list = ArtworkTecniqueSort(ArtistTecnique)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return sort_list, elapsed_time_mseg


#Req 4 
def getArtworksByNationality(catalog):
    start_time = time.process_time()
    ArtistNationality = lt.newList('ARRAY_LIST', cmpfunction=comparenationality)
    for artists in lt.iterator(catalog['Artists']):
        for a in lt.iterator(artists['Artworks']):
            Nation = artists['Nationality']
            position = lt.isPresent(ArtistNationality,Nation)
            if position > 0:
                Nation = lt.getElement(ArtistNationality, position)
                trabajo = lt.newList("ARRAY_LIST")
                lt.addLast(trabajo,a)
                lt.addLast(trabajo,artists["DisplayName"])
                lt.addLast(Nation['Artworks'], trabajo)
            else:
                newnation = newNationality(artists['Nationality'])
                trabajo = lt.newList("ARRAY_LIST")
                lt.addLast(trabajo,a)
                lt.addLast(trabajo,artists["DisplayName"])
                lt.addLast(ArtistNationality, newnation)
                lt.addLast(newnation['Artworks'], trabajo)
    ombe = lt.isPresent(ArtistNationality, "Nationality unknown")
    ayuda = lt.getElement(ArtistNationality, ombe)
    NationalityUnknown = lt.size(ayuda["Artworks"])
    lt.deleteElement(ArtistNationality, ombe)
    sorted_list = sortArtworkNationality(ArtistNationality)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return sorted_list, elapsed_time_mseg, NationalityUnknown
    

#Req 5

def getArtworksByDepartment(catalog, department):
    start_time = time.process_time()
    ArtworkinCategory = lt.newList('ARRAY_LIST',cmpfunction=compACategory)
    
    for artworks in lt.iterator(catalog["Artwork"]):
        if artworks['Department'] == department:
            lt.addLast(ArtworkinCategory,artworks)

    listaconprecio = precioest(ArtworkinCategory)
    pesoestim = pesoest(ArtworkinCategory, "Weight")
    precioestim = pesoest(ArtworkinCategory, "Price")
    
    sorted_listbyprice = mergesort.sort(listaconprecio, compareprice)
    artworkingsub = lt.subList(listaconprecio,1, lt.size(ArtworkinCategory))
    
    sorted_listbyage = mergesort.sort(artworkingsub, compareage)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    
    return sorted_listbyprice, sorted_listbyage, pesoestim, precioestim, elapsed_time_mseg
     
def precioest(ArtworkinCategory):
    
    for artworks in lt.iterator(ArtworkinCategory):
        if artworks["Weight"] == '':
            porPeso = 0
        else:
            porPeso = round(72 * float(artworks["Weight"]),4)
        if (artworks["Height"] == '' or artworks["Width"] == '') and artworks["Diameter"] == '':
            porArea = 0
        elif artworks["Diameter"] != '':
            radius = float(artworks["Diameter"])/200
            porArea = round((radius)**2*(3.1415)*72, 4)
        else: 
            porArea = round(((float(artworks["Height"])*float(artworks["Width"]))/ 10000)*72,4)
        if (artworks["Height"] == '' or artworks["Width"] == '' or artworks["Length"] == ''):
            porVol = 0
        else:
            porVol = round(((float(artworks["Height"])*float(artworks["Width"])*float(artworks["Length"]))/ 1000000)*72,4)

        if porVol == 0 and porArea == 0 and porPeso == 0:
            precio_final = 48
        else:
            precio_final = max(porPeso,porArea,porVol)
        artworks['Price'] = precio_final
    return ArtworkinCategory
        


def pesoest(ArtworkinCategory, category):
    suma = 0
    for artworks in lt.iterator(ArtworkinCategory):
        if artworks[category] != '':
            suma += float(artworks[category])
    return round(suma,4)
    


# Funciones utilizadas para comparar elementos dentro de una lista
def compareprice(p1,p2):
    return (float(p1['Price']) > float(p2['Price']))

def compareage(a1,a2):
    if a1['Date'] != '' and a1['Date'] != '0' and a2['Date'] != '' and a2['Date'] != '0':
        return (int(a1['Date']) < int(a2['Date']))

def compareartists(a1, a2):
    
    if a1 < int(a2['ConstituentID']):
        return -1
    elif a1 == int(a2['ConstituentID']):
        return 0
    else:
        return 1

def compareartworks(a1, a2):
    if a1['ObjectID'] < a2['ObjectID']:
        return -1
    elif a1['ObjectID'] == a2['ObjectID']:
        return 0
    else:
        return 1

def compareartistID(a1, artist):
    if str(a1) in str(artist['ConstituentID']):
        return 0
    else:
        return -1


def compArtistDate(Artist1, Artist2):
    return (int(Artist1['BeginDate']) < int(Artist2['BeginDate'])) 


def compACategory(dep, artworkD):
    if dep.lower() == artworkD["Department"].lower():
        return 0
    else:
        return -1 


def comparenationality(Nation,Nations):
    if Nation.lower() == Nations['Nationality'].lower():
        return 0
    else:
        return -1 

def compATecnique(tec, artistTecnique):
    if tec.lower() == artistTecnique['MediumName'].lower():
        return 0
    else:
        return -1 
        
    
            
def compArtworkNation(N1, N2):
    return int(lt.size(N1['Artworks'])) > int(lt.size(N2['Artworks']))

def compDateAcquired(Date1, Date2):
    if Date1['DateAcquired'] != '' and Date1['DateAcquired'] != '0' and Date2['DateAcquired'] != '0' and Date2['DateAcquired'] != '':
        return (date.fromisoformat(Date1['DateAcquired']) < date.fromisoformat(Date2['DateAcquired']))


def compTec(tec1, tec2):
    return lt.size(tec1['Artworks']) > lt.size(tec2['Artworks'])


# Funciones de ordenamiento

def SortDates(DatesArtist):
    
    sorted_list = mergesort.sort(DatesArtist, compArtistDate)
     
    return sorted_list

def sortDateAcquired(artworksDate):
    
    sorted_list = mergesort.sort(artworksDate, compDateAcquired)
        
    return sorted_list


def ArtworkTecniqueSort(ArtworkTecnique):
    
    sort_list = mergesort.sort(ArtworkTecnique, cmpfunction=compTec)
     
    return sort_list

def sortArtworkNationality(ArtistNationality):
    sort_list = mergesort.sort(ArtistNationality, compArtworkNation)
    return sort_list  
