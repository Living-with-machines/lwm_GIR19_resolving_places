#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector
from mysql.connector import Error
import urllib.parse
import regex as re
import os
import sys
from timeit import default_timer as timer

# Geonames language pseudocodes (https://www.geonames.org/manual.html):
geoPseudocodes = ["post", "link", "iata", "icao", "faac", "tcid", "unlc", "abbr", "wkdt", "phon", "piny"]

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else '.'
LIMIT = sys.argv[2] if len(sys.argv) > 2 and int(sys.argv[2]) > 0 else None

start_time = timer()

"""
Collect information from alternateNamesV2 table from geonames DB:
* Links between geonames and wikipedia:
    * dWikititleGeo (dict): key is wikipedia title, value is geonames id
    * dGeoWikititle (dict): key is geonames id, value is wikipedia title
* Alternate names:
    * dWikititleAltname (dict): key is wikipedia title, value is list of geonames alternate names.
"""

print('Loading alternate names')

re_enwiki = r'.*en\.wikipedia\.org/wiki/.+'
dWikititleGeo = dict()
dGeoWikititle = dict()
dWikititleAltname = dict()
dGeoMaininfo = dict()
with open(os.path.join(os.path.join(DATA_DIR, "alternateNamesV2"), "alternateNamesV2.txt")) as fr:
    lines = fr.readlines()
    for line in lines:
        line = line.strip().split("\t")
        geonameid = int(line[1])
        isolanguage = line[2]
        alternatename = line[3]
        if isolanguage == "link":
            if re.match(re_enwiki, alternatename):
                shortWikiTitle = urllib.parse.unquote(alternatename).split("/")[-1]
                dWikititleGeo[shortWikiTitle] = geonameid
                dGeoWikititle[geonameid] = shortWikiTitle
    for line in lines:
        line = line.split("\t")
        geonameid = int(line[1])
        isolanguage = line[2]
        alternatename = line[3]
        if geonameid in dGeoWikititle and not isolanguage in geoPseudocodes:
            match = re.match(r'^[\p{Latin}[A-Za-z\s\-\'\’]+$', alternatename)
            if match:
                altname = match.group()
                shortWikiTitle = dGeoWikititle[geonameid]
                if shortWikiTitle in dWikititleAltname:
                    if not altname in dWikititleAltname[shortWikiTitle]:
                        dWikititleAltname[shortWikiTitle].append(altname)
                else:
                    dWikititleAltname[shortWikiTitle] = [altname]

print('Completed loading alternate names: {} seconds'.format(timer() - start_time))

"""
Collect information from cities500 table from geonames DB
(from http://download.geonames.org/export/dump/: all cities
with a population > 500 or seats of adm div to PPLA4 (ca 185.000),
see 'geoname' table for columns):
    * dGeoMaininfo (dict): key is geonames id, value is tuple with:
        * location name according to geonames
        * ascii version of the name
        * population of the location
"""
with open(os.path.join(DATA_DIR,"cities500.txt")) as fr:
    lines = fr.readlines()
    for line in lines:
        line = line.strip().split("\t")
        geonameid = int(line[0])
        mainname = line[1]
        asciiname = line[2]
        country = line[8]
        population = line[14]
        dGeoMaininfo[geonameid] = (mainname, asciiname, country, population)

print('Completed loading cities500 table: {} seconds'.format(timer() - start_time))


"""
Clean wiki title from appositions and unlikely characters:
"""
def preprocessLocName(locname):
    if locname != None:
        if not any(char.isdigit() for char in locname):
            locname = locname.split(",_")[0]
            locname = locname.split("_(")[0]
            locname = locname.split(" (")[0]
            locname = locname.split(", ")[0]
            # Turn underscores into white spaces:
            locname = locname.replace("_", " ")
            locname = locname.replace("'", " ")
            locname = locname.replace("–", " ")
            locname = locname.replace("-", " ")
            locname = locname.strip()
            if not locname.startswith("List ") and not locname.startswith("Listed "):
                # Trim whitespaces:
                return re.sub(r"  *", " ", locname)

# Control query size at each iteration:
movingLimit = 0
commitAt = 10000

def insertIntoDB(newAltname, cursorGaz, indexMainLocations, uniqueMainLocs, indexAlternateNames, uniqueAltnames, dWikititleGeo, dGeoMaininfo, dWikititleAltname, mainPageId, mainPageTitle, gtId, mainPageLen, gtLat, gtLon, gtDim, gtType, gtCountry, gtRegion, altnameSource):
    dGeoAltnames = dict()

    if preprocessLocName(newAltname):
        cleanedMainTitle = preprocessLocName(newAltname)
        population = None
        maingeoname = None
        asciigeoname = None
        if not (cleanedMainTitle.lower(), mainPageId) in uniqueAltnames:
            if not (mainPageId, mainPageTitle, gtId) in uniqueMainLocs:
                indexMainLocations += 1
                geonamesId = None
                if mainPageTitle in dWikititleGeo:
                    geonamesId = int(dWikititleGeo[mainPageTitle])
                if not geonamesId is None:
                    if geonamesId in dGeoMaininfo:
                        if not dGeoMaininfo[geonamesId] is None:
                            maingeoname, asciigeoname, country, population = dGeoMaininfo[geonamesId]
                cursorGaz.execute("""
                    INSERT INTO location(id, wiki_id, wikigt_id, geo_id, wiki_title, page_len, lat, lon, dim, type, country, region, population)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (indexMainLocations, mainPageId, gtId, geonamesId, mainPageTitle, mainPageLen, gtLat, gtLon, gtDim, gtType, gtCountry, gtRegion, population))

                uniqueMainLocs[(mainPageId, mainPageTitle, gtId)] = indexMainLocations

            uniqueAltnames.add((cleanedMainTitle.lower(), mainPageId))

            indexAlternateNames += 1
            cursorGaz.execute("""
                INSERT INTO altname(id, main_id, altname, source)
                VALUES(%s, %s, %s, %s)
                """, (indexAlternateNames, indexMainLocations, cleanedMainTitle, altnameSource))
            # print("\t", indexAlternateNames, indexMainLocations, cleanedMainTitle, altnameSource)

        if not (maingeoname is None) and not (maingeoname.lower(), mainPageId) in uniqueAltnames:
            # print("\t", indexAlternateNames, indexMainLocations, maingeoname, "(geonamesmain)")
            uniqueAltnames.add((maingeoname.lower(), mainPageId))
            dGeoAltnames[maingeoname] = "geonamesmain"

        if not (asciigeoname is None) and not (asciigeoname.lower(), mainPageId) in uniqueAltnames:
            # print("\t", indexAlternateNames, indexMainLocations, asciigeoname, "(geonamesascii)")
            uniqueAltnames.add((asciigeoname.lower(), mainPageId))
            dGeoAltnames[asciigeoname] = "geonamesascii"

        # Add alternate names from alternateNamesV2 table:
        if mainPageTitle in dWikititleAltname:
            names = dWikititleAltname[mainPageTitle]
            for name in names:
                if not name in dGeoAltnames and not (name.lower(), mainPageId) in uniqueAltnames:
                    uniqueAltnames.add((name.lower(), mainPageId))
                    dGeoAltnames[name] = "geonamesalt"

        for gn in dGeoAltnames:
            indexAlternateNames += 1
            cursorGaz.execute("""
                INSERT INTO altname(id, main_id, altname, source)
                VALUES(%s, %s, %s, %s)
                """, (indexAlternateNames, indexMainLocations, gn, dGeoAltnames[gn]))

    return indexMainLocations, uniqueMainLocs, indexAlternateNames, uniqueAltnames

wikiDB = None
gazDB = None
try:
    wikiDB = mysql.connector.connect(
            host='localhost',
            database='wiki_en',
            user='root',
            password='1234'
        )
    gazDB = mysql.connector.connect(
            host='localhost',
            database='gazetteer',
            user='root',
            password='1234')
    if wikiDB.is_connected() and gazDB.is_connected():
        cursor = wikiDB.cursor(dictionary=True)
        cursorGaz = gazDB.cursor(dictionary=True)

        uniqueAltnames = set()
        uniqueMainLocs = dict()
        indexAlternateNames = 0
        indexMainLocations = 0

        ### Main pages that are not redirected and are locations:
        query = 'SELECT * FROM locs'
        if LIMIT:
            query += ' LIMIT {};'.format(LIMIT)
        print('Executing locations query: {}'.format(query))
        cursor.execute(query)
        results = cursor.fetchall()
        print('Completed locations query: {}'.format(timer()-start_time))
        total_rows = 0

        for result in results:
            gtName = result['gt_name']
            mainPageId = result['page_id']
            mainPageTitle = result['page_title']
            mainPageLen = result['page_len']
            gtId = result['gt_id']
            gtLat = result['gt_lat']
            gtLon = result['gt_lon']
            gtDim = result['gt_dim']
            gtType = result['gt_type']
            gtCountry = result['gt_country']
            gtRegion = result['gt_region']

            ### Insert alternate names from wiki title:
            indexMainLocations, uniqueMainLocs, indexAlternateNames, uniqueAltnames = insertIntoDB(mainPageTitle, cursorGaz, indexMainLocations, uniqueMainLocs, indexAlternateNames, uniqueAltnames, dWikititleGeo, dGeoMaininfo, dWikititleAltname, mainPageId, mainPageTitle, gtId, mainPageLen, gtLat, gtLon, gtDim, gtType, gtCountry, gtRegion, "wikimain")

            ### Insert alternate names from wiki title:
            indexMainLocations, uniqueMainLocs, indexAlternateNames, uniqueAltnames = insertIntoDB(gtName, cursorGaz, indexMainLocations, uniqueMainLocs, indexAlternateNames, uniqueAltnames, dWikititleGeo, dGeoMaininfo, dWikititleAltname, mainPageId, mainPageTitle, gtId, mainPageLen, gtLat, gtLon, gtDim, gtType, gtCountry, gtRegion, "wikigt")

            movingLimit += 1
            total_rows += 1

            if movingLimit >= commitAt:
                print("Row {}: {}".format(total_rows, timer()-start_time))
                gazDB.commit()
                movingLimit = 0
        gazDB.commit()

        print('Total rows in query: {}'.format(total_rows))

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    # Close connection to wikiDB
    if (wikiDB and wikiDB.is_connected()):
        cursor.close()
        wikiDB.close()
    if (gazDB and gazDB.is_connected()):
        cursorGaz.close()
        gazDB.close()

print('Completed: {}'.format(timer()-start_time))
