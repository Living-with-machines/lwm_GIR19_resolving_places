#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector
from mysql.connector import Error
import urllib.parse
import re
import json
from timeit import default_timer as timer

"""
Clean wiki title from appositions and unlikely characters:
"""
def preprocessLocName(locname):
    if locname != None:
        if not any(char.isdigit() for char in locname):
            match = re.match(r'^[\u00C0-\u017FA-Za-z\s\-\'\’]+$', locname)
            if match:
                locname = match.group()
                locname = locname.split(",_")[0]
                locname = locname.split("_(")[0]
                locname = locname.split(" (")[0]
                locname = locname.split(", ")[0]
                # Turn underscores into white spaces:
                locname = locname.replace("_", " ")
                locname = locname.replace("’", " ")
                locname = locname.replace("'", " ")
                locname = locname.replace("–", " ")
                locname = locname.replace("-", " ")
                locname = locname.strip()
                if not locname.startswith("List ") and not locname.startswith("Listed "):
                    # Trim whitespaces:
                    return re.sub(r"  *", " ", locname)

def insertRedirectIntoDB(alreadyAddedAltnames, lengthAltnames, redirectPageTitle, redirectMainTitle, altMainId):
    if preprocessLocName(redirectPageTitle):
        cleanedRedirect = preprocessLocName(redirectPageTitle)

        if not (cleanedRedirect is None):
            if altMainId in alreadyAddedAltnames:
                if not cleanedRedirect.lower() in alreadyAddedAltnames[altMainId]:
                    lengthAltnames += 1
                    lengthAltnames += 1
                    cursorGaz.execute("""
                        INSERT INTO altname(id, main_id, altname, source)
                        VALUES(%s, %s, %s, %s)
                        """, (lengthAltnames, altMainId, cleanedRedirect, "wikiredirect"))
                    alreadyAddedAltnames[altMainId].append(cleanedRedirect.lower())
            else:
                lengthAltnames += 1
                cursorGaz.execute("""
                    INSERT INTO altname(id, main_id, altname, source)
                    VALUES(%s, %s, %s, %s)
                    """, (lengthAltnames, altMainId, cleanedRedirect, "wikiredirect"))
                alreadyAddedAltnames[altMainId] = [cleanedRedirect.lower()]
    return alreadyAddedAltnames, lengthAltnames

# Control query size at each iteration:
movingLimit = 0
commitAt = 10000

dictRedirects = dict()
alreadyAddedLocations = dict()
alreadyAddedAltnames = dict()
try:
    wikiDB = mysql.connector.connect(
            host='localhost',
            database='wiki_db',
            user='xxxxxxxx',
            password='xxxxxxxx'
        )
    gazDB = mysql.connector.connect(
            host='localhost',
            database='wikiGazetteer',
            user='xxxxxxxx',
            password='xxxxxxxx')
    if wikiDB.is_connected() and gazDB.is_connected():
        cursor = wikiDB.cursor(dictionary=True)
        cursorGaz = gazDB.cursor(dictionary=True)

        uniqueMainLocs = dict()
        indexAlternateNames = 0
        indexMainLocations = 0

        ### Main pages that are not redirected and are locations:
        cursorGaz.execute("""
            SELECT wiki_title, wiki_id, id FROM location
            """)
        locations = cursorGaz.fetchall()

        for i in locations:
            wt = i["wiki_title"]
            locid = i["id"]
            wikiid = i["wiki_id"]
            if not wt in alreadyAddedLocations:
                alreadyAddedLocations[wt] = (locid, wikiid)
        print("Table `location` read.")

        ### Main pages that are not redirected and are locations:
        cursorGaz.execute("""
            SELECT altname, main_id, id FROM altname
            """)
        altnames = cursorGaz.fetchall()

        lengthAltnames = 0
        for i in altnames:
            an = i["altname"].lower()
            anid = i["main_id"]
            lengthAltnames += 1
            if not anid in alreadyAddedAltnames:
                alreadyAddedAltnames[anid] = [an]
            else:
                if not an in alreadyAddedAltnames[anid]:
                    alreadyAddedAltnames[anid].append(an)
        print("Table `altname` read.")

        ### Main pages that are not redirected and are locations:
        cursor.execute("""
            SELECT DISTINCT page.page_title as 'redirect_page_title', redirect.rd_title as 'redirect_main_title' FROM redirect
            JOIN page ON page.page_id=redirect.rd_from
            WHERE page.page_is_redirect=1
            AND page.page_namespace=0
            AND redirect.rd_namespace=0
            AND page.page_content_model="wikitext";
            """)
        results = cursor.fetchall()
        print("Query joining page and redirect tables executed.")

        for result in results:
            redirectPageTitle = result['redirect_page_title']
            redirectMainTitle = result['redirect_main_title']

            if redirectMainTitle in alreadyAddedLocations:
                altMainId = alreadyAddedLocations[redirectMainTitle][0]
                alreadyAddedAltnames, lengthAltnames = insertRedirectIntoDB(alreadyAddedAltnames, lengthAltnames, redirectPageTitle, redirectMainTitle, altMainId)

                movingLimit += 1

                if movingLimit % commitAt == 0:
                    print(movingLimit)
                    gazDB.commit()

                dictRedirects[redirectPageTitle] = altMainId

        gazDB.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    # Close connection to wikiDB
    if (wikiDB.is_connected()):
        cursor.close()
        wikiDB.close()
    if (gazDB.is_connected()):
        cursorGaz.close()
        gazDB.close()