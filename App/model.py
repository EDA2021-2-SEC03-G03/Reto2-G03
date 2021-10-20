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


from DISClib.DataStructures.arraylist import size
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
               'Artists': None}

    catalog['Artists'] = lt.newList(cmpfunction=compareartists) 
    catalog['Artwork'] = lt.newList(cmpfunction=compareartworks)
    catalog['ArtistID'] = mp.newMap(34500,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
    catalog['ArtworksofArtist'] = mp.newMap(15250,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
    catalog['ArtistsDates'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
    catalog['ArtworksDateAcquired'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareArtworkDate)
    catalog['ArtworkMedium'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)                            
    catalog['ArtworkNationality'] = mp.newMap(200,
                                 maptype='CHAINING',
                                 loadfactor=4.0,
                                 comparefunction=compareCatalog)
    catalog['ArtworkDepartment'] = mp.newMap(8000,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)

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
    addArtistDate(catalog, listArtist['BeginDate'], artist)
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
        #AddArtworkMedium(catalog, artist, artwork)
    addArtworksDateAcquired(catalog, listArtwork['DateAcquired'], artwork)
    addArtworkDepartment(catalog, listArtwork['Department'], artwork)
    
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

def addArtistDate(catalog, beginDate, artists):
    
    if beginDate != '' and beginDate != '0':
        ArtistFiltrada = {'DisplayName': artists['DisplayName'], 
                    'ConstituentID': artists['ConstituentID'],
                    'BeginDate': artists['BeginDate'], 
                    'EndDate': artists['EndDate'],
                    'Nationality': artists['Nationality'],
                    'Gender': artists['Gender']}
        dates = catalog['ArtistsDates']
        existdate = mp.contains(dates, beginDate)
        if existdate:
            entry = mp.get(dates, beginDate)
            d = me.getValue(entry)
        else:
            d = newArtistDate()
            mp.put(dates, beginDate, d)
        lt.addLast(d['Artists'], ArtistFiltrada)

def addArtworksDateAcquired(catalog, dateAcquired, artwork):

    if artwork['DateAcquired'] != '' and artwork['DateAcquired']!='0':
        dateSplit = dateAcquired.split('-')
        year = int(dateSplit[0])
        artworkFiltrada = {'ObjectID': (artwork['ObjectID']).replace(" ", ""), 
                    'Title': (artwork['Title']).lower(),
                    'ConstituentID': (artwork['ConstituentID']).replace(" ", ""),
                    'Date': artwork['Date'],
                    'Medium': (artwork['Medium']).lower(),
                    'Dimensions': artwork['Dimensions'],
                    'CreditLine': artwork['CreditLine'],
                    'DateAcquired': artwork['DateAcquired']}

        datesAc = catalog['ArtworksDateAcquired']
        existdate = mp.contains(datesAc, year)
        if existdate:
            entry = mp.get(datesAc, year)
            d = me.getValue(entry)
        else:
            d = newArtworkDateAcquired(year)
            mp.put(datesAc, year, d)
        lt.addLast(d['Artworks'], artworkFiltrada)

    

"""

def AddArtworkMedium(catalog, artist_id, artwork):
    artists = catalog['Artists']
    posartist = lt.isPresent(artists,artist_id)
    if posartist > 0:
        artist = lt.getElement(artists, posartist)
        lt.addLast(artist['Artworks'], artwork)
        lt.addLast(artwork['Artist'], artist['DisplayName'])

        ArtistMedium = catalog['ArtworkMedium']   
        existartist = mp.contains(ArtistMedium, artist['DisplayName'])
        if existartist:
            entry = mp.get(ArtistMedium, artist['DisplayName'])
            artist = me.getValue(entry)
            addMedium(catalog, artwork['Medium'], artwork)
        else:
            medium = newArtistMedium(artwork['Medium'])
            addMedium(catalog, artwork['Medium'], artwork)
            mp.put(ArtistMedium, artwork['Medium'], medium)
"""
def AddArtworkMedium(catalog, mediumName, artwork):
    mediums = catalog['ArtworkMedium']
    existmedium = mp.contains(mediums, mediumName)
    if existmedium:
        entry = mp.get(mediums, mediumName)
        medium = me.getValue(entry)
    else:
        medium = newMedium()
        mp.put(mediums, mediumName, medium)
    lt.addLast(medium['Artworks'], artwork)


def addMedium(catalog, mediumName, artwork):

    ArtworkFiltrada = {'ObjectID': (artwork['ObjectID']).replace(" ", ""), 
                  'Title': (artwork['Title']).lower(),
                  'ConstituentID': (artwork['ConstituentID']).replace(" ", ""),
                  'Date': artwork['Date'],
                  'Medium': (artwork['Medium']).lower(), 
                  'Dimensions': artwork['Dimensions']}
    
    mediums = catalog['ArtworkMedium']
    existmedium = mp.contains(mediums, mediumName)
    if existmedium:
        entry = mp.get(mediums, mediumName)
        medium = me.getValue(entry)
    else:
        medium = newMedium()
        mp.put(mediums, mediumName, medium)
    lt.addLast(medium['Artworks'], ArtworkFiltrada)

def addArtworkDepartment(catalog, departmentName, artwork):
    
    mediums = catalog['ArtworkDepartment']
    existmedium = mp.contains(mediums, departmentName)
    if existmedium:
        entry = mp.get(mediums, departmentName)
        medium = me.getValue(entry)
    else:
        medium = newDepartment()
        mp.put(mediums, departmentName, medium)
    lt.addLast(medium['Artworks'], artwork)

def addArtistNationality(catalog,nationality,artist):
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
def getArtworksMediumArtist(catalog, ArtistName):
    medium = mp.get(catalog['ArtworkMedium'], ArtistName)
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
#--------------------------------------------------------------------------------------------------------------------------
def getArtistByDate(catalog, anoInicial, anoFinal):
    start_time = time.process_time()
    
    list_artistDate = lt.newList('ARRAY_LIST', compArtistsDates)
    
    i = anoInicial
    while i >= anoInicial and i <= anoFinal:
        artist_value = mp.get(catalog['ArtistsDates'], str(i))
        if artist_value:
            list_artists= me.getValue(artist_value)
            for a in lt.iterator(list_artists['Artists']):
                lt.addLast(list_artistDate, a)
        
        i += 1

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000        
    return list_artistDate, elapsed_time_mseg


#Req 2:
#--------------------------------------------------------------------------------------------------------------------------
def getArtworksDate(catalog, inicial, final):
    start_time = time.process_time()

    list_artworkDateAcquired = lt.newList('ARRAY_LIST')

    inicialDate = date.fromisoformat(inicial)
    finalDate = date.fromisoformat(final)

    inicialSplit = inicial.split('-')
    finalSplit = final.split('-')

    i = int(inicialSplit[0]) 
    print(i)
    while i >= int(inicialSplit[0]) and i <= int(finalSplit[0]):
        #print(catalog['ArtworksDateAcquired'])
        artwork_value = mp.get(catalog['ArtworksDateAcquired'], i)
        if artwork_value:
            list_artwork= me.getValue(artwork_value)
            for a in lt.iterator(list_artwork['Artworks']):
                a1 = date.fromisoformat(a['DateAcquired'])
                if a1 >= inicialDate and a1 <= finalDate and a1 != '' and a1!='0':
                    lt.addLast(list_artworkDateAcquired, a)
        i += 1

    sort_DateAcquired =  sortArtworkDateAcquired(list_artworkDateAcquired)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000     
    return sort_DateAcquired, elapsed_time_mseg


def getartworkPurchased(datesArtworks):
    count = 0
    for a in lt.iterator(datesArtworks):
        if 'purchase' in a['CreditLine'].lower():
            count += 1
    
    return count 

#Req 3:
#--------------------------------------------------------------------------------------------------------------------------
def getArtworksMediumOneArtist(catalog, artistName):
    start_time = time.process_time()
    ArtistTecnique = lt.newList('ARRAY_LIST', cmpfunction=compATecnique)
    artistID = getartistIDbyName(catalog, artistName) #Buscar el ID del artista específico
    artwork_value = mp.get(catalog['ArtworksofArtist'], artistID)
    if artwork_value:
        artworks= me.getValue(artwork_value)
        getMediumOneArtist(catalog,artworks) #Crear el mnapa de los medios de un artista con sus obras 
        artwork_value2 = mp.keySet(catalog['ArtworkMedium']) 
        for element in lt.iterator(artwork_value2):
            artist_value = mp.get(catalog['ArtworkMedium'], element)
            number_artworks= me.getValue(artist_value) #Lista de obras de ese medio en específico
            tuple_medium = {'Medium':element,'NumbArtworks':lt.size(number_artworks["Artworks"])} 
            lt.addLast(ArtistTecnique, tuple_medium)

    sortByMedium(ArtistTecnique)
    #print(ArtistTecnique)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return ArtistTecnique, elapsed_time_mseg 

def getartistIDbyName(catalog, artistName): #Sacar ID de un artista
    for artist in lt.iterator(catalog["Artists"]):
        #print(artist)
        #print(artistName, artist['DisplayName'])
        if artistName.lower() == (artist["DisplayName"]).lower():
            return artist["ConstituentID"]
    return None

def getMediumOneArtist(catalog, artworks): #Creando el mapa de medios de un artista con sus obras
    for artwork in lt.iterator(artworks['Artworks']):
        AddArtworkMedium(catalog, artwork['Medium'], artwork)

def getArtworkOneMedium(catalog, medium): #Sacar obras del medio más utilizado
    artist_value = mp.get(catalog['ArtworkMedium'], medium)
    if artist_value:
        list_artworks = me.getValue(artist_value)
        return list_artworks['Artworks']
    return None


#Req 4:
#--------------------------------------------------------------------------------------------------------------------------
def getArtworkNationality(catalog):
    start_time = time.process_time()
    nationality_pop = lt.newList('ARRAY_LIST',comparenat)
    artwork_value = mp.keySet(catalog['ArtworkNationality'])
    for element in lt.iterator(artwork_value):
        artist_value = mp.get(catalog['ArtworkNationality'], element)
        number_artworks= me.getValue(artist_value)
        tuple_nat = {"Nationality":element,"NumbArtworks":lt.size(number_artworks["Artworks"])}
        lt.addLast(nationality_pop,tuple_nat)
    unknowncorrection(nationality_pop)
    sortByNationality(nationality_pop)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return nationality_pop,elapsed_time_mseg
def getArtworksOneNat(catalog, nationality):
    artist_value = mp.get(catalog['ArtworkNationality'], nationality)
    if artist_value:
        list_artworks= me.getValue(artist_value)
        return list_artworks['Artworks']
    return None     
def unknowncorrection(nationality_pop):
    ombe1 = lt.isPresent(nationality_pop, "nationality unknown")
    ayuda1 = lt.getElement(nationality_pop, ombe1)
    lt.deleteElement(nationality_pop,ombe1)
    ombe2 = lt.isPresent(nationality_pop, "")
    ayuda2 = lt.getElement(nationality_pop, ombe2)
    final_number = int(ayuda1["NumbArtworks"])+ int(ayuda2["NumbArtworks"])
    tuple_corr = {"Nationality":"unknown", "NumbArtworks":str(final_number)}
    lt.deleteElement(nationality_pop,ombe2)
    lt.addLast(nationality_pop, tuple_corr)
    return None
#-------------------------------------------------------------------------------------------------------------------------

#Req5
#-------------------------------------------------------------------------------------------------------------------------
def getArtworksByDepartment(catalog, department):
    start_time = time.process_time()
    artist_value = mp.get(catalog['ArtworkDepartment'], department)
    if artist_value:
        list_artworks= me.getValue(artist_value)
        listaconprecio = precioest(list_artworks)
        pesoestim = pesoest(list_artworks, "Weight (kg)")
        precioestim = pesoest(list_artworks, "Price")
        sorted_listbyprice = ms.sort(listaconprecio["Artworks"], compareprice)
        print(sorted_listbyprice.keys())
        artworkingsub = lt.subList(listaconprecio["Artworks"],1, lt.size(list_artworks["Artworks"]))
        sorted_listbyage = ms.sort(artworkingsub, compareage)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        
        return sorted_listbyprice, sorted_listbyage, pesoestim, precioestim, elapsed_time_mseg
    
    return None   

    
     
def precioest(ArtworkinCategory):
    
    for artworks in lt.iterator(ArtworkinCategory["Artworks"]):
        if artworks["Weight (kg)"] == '':
            porPeso = 0
        else:
            porPeso = round(72 * float(artworks["Weight (kg)"]),4)
        if (artworks["Height (cm)"] == '' or artworks["Width (cm)"] == '') and artworks["Diameter (cm)"] == '':
            porArea = 0
        elif artworks["Diameter (cm)"] != '':
            radius = float(artworks["Diameter (cm)"])/200
            porArea = round((radius)**2*(3.1415)*72, 4)
        else: 
            porArea = round(((float(artworks["Height (cm)"])*float(artworks["Width (cm)"]))/ 10000)*72,4)
        if (artworks["Height (cm)"] == '' or artworks["Width (cm)"] == '' or artworks["Length (cm)"] == ''):
            porVol = 0
        else:
            porVol = round(((float(artworks["Height (cm)"])*float(artworks["Width (cm)"])*float(artworks["Length (cm)"]))/ 1000000)*72,4)

        if porVol == 0 and porArea == 0 and porPeso == 0:
            precio_final = 48
        else:
            precio_final = max(porPeso,porArea,porVol)
        artworks['Price'] = precio_final
    return ArtworkinCategory

def pesoest(ArtworkinCategory, category):
    suma = 0
    for artworks in lt.iterator(ArtworkinCategory["Artworks"]):
        if artworks[category] != '':
            suma += float(artworks[category])
    return round(suma,4)
#-------------------------------------------------------------------------------------------------------------------------

#Aux
#-------------------------------------------------------------------------------------------------------------------------
def getArtists(catalog,artwork):
    list_tutu = artwork["ConstituentID"].replace("[","").replace("]","").replace(" ","").split(",")
    list_names = []
    for artistId in list_tutu:
        pos = mp.get(catalog['ArtistID'],artistId)
        artist = me.getValue(pos)
        artist_clean = artist["Artistinfo"]
        list_names.append(artist_clean["DisplayName"])
    return list_names
#-------------------------------------------------------------------------------------------------------------------------
# Funciones para creacion de datos

def newArtist(artistid):
    
    artist= {'artistID': '',
             'Artworks': None,}
    artist['artistID'] = artistid

    artist['Artworks'] = lt.newList('ARRAY_LIST')

    return artist


def newArtworkDateAcquired(year):

    DateAcquired = {'Date': year, 'Artworks': None}
    DateAcquired['Artworks'] = lt.newList('ARRAY_LIST', compareCatalog)
    return DateAcquired

def newArtistMedium(medium):
    ArtistMedium = {'Medium': medium, 'Artworks': None}
    ArtistMedium['Artworks'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
    return ArtistMedium

def newMedium():
    
    medium = {"Artworks": None}
    medium['Artworks'] = lt.newList('ARRAY_LIST', compareCatalog)
    return medium

def newDepartment():

    department = {"Artworks": None}
    department['Artworks'] = lt.newList('ARRAY_LIST', compareCatalog)
    return department

def newArtistDate():
    Date = {"Artists": None}
    Date['Artists'] = lt.newList('ARRAY_LIST', compareCatalog)
    return Date

def newArtworkofArtist():
    """
    Esta funcion crea la estructura de artistas asociados
    a un ConstituentID.
    """
    medium = {"Artworks": None}
    medium['Artworks'] = lt.newList('ARRAY_LIST', compareCatalog)
    return medium

def newNationality():
    """
    Esta funcion crea la estructura de artistas asociados
    a un ConstituentID.
    """
    medium = {"Artworks": None}
    medium['Artworks'] = lt.newList('ARRAY_LIST', compareCatalog)
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
    
def compareCatalog(category, entry):
    categoryentry = me.getKey(entry)
    if (category == categoryentry):
        return 0
    elif (category > categoryentry):
        return 1
    else:
        return -1 

def compareArtworkDate(Date, entry):
    categoryentry = me.getKey(entry)
    if (int(Date) == int(categoryentry)):
        return 0
    elif (int(Date) > int(categoryentry)):
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

def compArtistsDates(a1, artists):
    if str(a1) in str(artists['BeginDate']):
        return 0
    else:
        return -1

def comparenat(a1, a2):
    if a1.lower() == a2['Nationality'].lower():
        return 0
    else:
        return -1 
def compareYears(year1, year2):
    return int(year1['Date']) < int(year2['Date'])

def cmpArtistDate(Artist1, Artist2):
    return (int(Artist1['BeginDate']) < int(Artist2['BeginDate'])) 

def cmpDateAcquired(Date1, Date2):
    if Date1['DateAcquired'] != '' and Date1['DateAcquired'] != '0' and Date2['DateAcquired'] != '0' and Date2['DateAcquired'] != '':
        return (date.fromisoformat(Date1['DateAcquired']) < date.fromisoformat(Date2['DateAcquired']))

def compMedium(tec1, tec2):
    return int(tec1['NumbArtworks']) > int(tec2['NumbArtworks'])

def comparepeople(art1, art2):
    return int(art1["NumbArtworks"]) > int(art2["NumbArtworks"])

def cmpArtistsDate(date1, date):
    if str(date1) in str(date['BeginDate']):
        return 0
    else:
        return -1

def compATecnique(tec, artistTecnique):
    if tec.lower() == artistTecnique['MediumName'].lower():
        return 0
    else:
        return -1

def compareprice(p1,p2):
    return (float(p1['Price']) > float(p2['Price']))

def compareage(a1,a2):
    if a1['Date'] != '' and a1['Date'] != '0' and a2['Date'] != '' and a2['Date'] != '0':
        return (int(a1['Date']) < int(a2['Date']))
# Funciones de ordenamiento

def sortByYears(list_artworks):
    return ms.sort(list_artworks, compareYears)

def sortArtistsDate(list_artistDate):
    return ms.sort(list_artistDate, cmpArtistDate)

def sortArtworkDateAcquired(list_artworksDA):
    return ms.sort(list_artworksDA, cmpDateAcquired)

def sortByMedium(ArtistTecnique):
    return ms.sort(ArtistTecnique, compMedium)

def sortByNationality(list_artworks):
    return ms.sort(list_artworks, comparepeople)

