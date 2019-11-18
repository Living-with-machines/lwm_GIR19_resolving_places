# Building a gazetteer

This document explains how to generate WikiGazetteer, a gazetteer based on Wikipedia and enriched with Geonames data. This is the alpha version of the code, and therefore does not have all the features that have been envisaged for future releases of the gazetteer.

**To cite:**

> Mariona Coll Ardanuy, Katherine McDonough, Amrey Krause, Daniel CS Wilson, Kasra Hosseini, and Daniel van Strien, “Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources,” in Proceedings of the 13th Workshop on Geographic Information Retrieval, 2019 (GIR19).

This is the step-by-step description on how to create the alpha version of the gazetteer from an English version of Wikipedia. To build a gazetteer in any other language (i.e. based on a different Wikipedia), you'll need to change the language codes in a couple of places (step 2 and step 6). Creating a gazetteer from a smaller Wikipedia (a Wikipedia in a language for which there are less entries) might be useful for testing.

## Steps to create WikiGazetteer

**1. Create the `wiki_db` database:**
```
mysql> CREATE DATABASE wiki_db;
mysql> USE wiki_db;
mysql> ALTER DATABASE wiki_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
mysql> exit;
```

**2. Download relevant Wikipedia tables and upload them to the `wiki_db` database:**

This step may take a long time (a couple of hours).
```
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-redirect.sql.gz
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-geo_tags.sql.gz

$ gzip -d enwiki-latest-geo_tags.sql.gz 
$ gzip -d enwiki-latest-page.sql.gz 
$ gzip -d enwiki-latest-redirect.sql.gz 

$ mysql -u [user] -p wiki_db < enwiki-latest-page.sql 
$ mysql -u [user] -p wiki_db < enwiki-latest-redirect.sql 
$ mysql -u [user] -p wiki_db < enwiki-latest-geo_tags.sql 

$ rm enwiki-latest-geo_tags.sql 
$ rm enwiki-latest-redirect.sql 
$ rm enwiki-latest-page.sql 
```

_Note:_ the Wikipedia version discussed in the GIR19 paper is `20190320`: to reproduce the same analysis, just replace `latest` by `20190320` in the URLs. If you want to create a gazetteer in any other language, change the Wikipedia language code in the URLs (e.g. `enwiki` to `cawiki`, check for [reference](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)).

**3. Create view that selects geographical entities:**
```
mysql> USE wiki_db;
mysql> CREATE VIEW locs AS
SELECT DISTINCT page1.page_id, page1.page_title, page1.page_len, geo.gt_id, geo.gt_lat, geo.gt_lon, geo.gt_dim, geo.gt_type, geo.gt_country, geo.gt_name, geo.gt_region FROM page AS page1
JOIN geo_tags AS geo on geo.gt_page_id=page1.page_id
WHERE page1.page_namespace=0
AND page1.page_content_model="wikitext"
AND geo.gt_globe="earth";
mysql> exit;
```

**4. Download relevant Geonames tables:**
```
$ wget http://download.geonames.org/export/dump/cities500.zip
$ wget http://download.geonames.org/export/dump/alternateNamesV2.zip
$ unzip cities500.zip
$ unzip alternateNamesV2.zip
$ rm cities500.zip
$ rm alternateNamesV2.zip
```

**5. Create the `wikiGazetteer` database:**
```
mysql> CREATE DATABASE wikiGazetteer;
mysql> USE wikiGazetteer;
mysql> ALTER DATABASE wikiGazetteer CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

mysql> CREATE TABLE `altname`
(
  `id` int PRIMARY KEY,
  `main_id` int,
  `altname` varchar(255),
  `source` varchar(255)
);
mysql> CREATE TABLE `location`
(
  `id` int PRIMARY KEY,
  `wiki_id` int,
  `wikigt_id` int,
  `geo_id` int,
  `wiki_title` varchar(255),
  `page_len` int,
  `lat` float,
  `lon` float,
  `dim` int,
  `type` varchar(255),
  `country` varchar(255),
  `region` varchar(255),
  `population` int
);
mysql> ALTER TABLE `altname` ADD FOREIGN KEY (`main_id`) REFERENCES `location` (`id`);
mysql> exit;
```

**6. Populate the `wikiGazetteer` database:**
```
$ python addLocations.py [language] [path_to_resources]
$ python addRedirections.py 
```

_Notes:_
* You will need to change your mysql connection credentials accordingly, both in `addLocations.py` (lines 181-182 and 187-188) and `addRedirections.py` (lines 69-70 and 75-76).
* These scripts have been created for English. For any other language using the Latin alphabet, add the correct language code as first argument of `addLocations.py`, and edit lines 106 and 206, as they contain language-specific filters. For languages not using the Latin alphabet, you might also want to change the regular expressions in `addLocations.py` (line 54) and `addRedirections.py` (line 17).

**7. Add indices to `wikiGazetteer` database:**
```
mysql> use wikiGazetteer
mysql> ALTER TABLE location ADD INDEX(id); 
mysql> ALTER TABLE altname ADD INDEX(altname); 
mysql> exit;
```

## WikiGazetteer: tables and contents (alpha version)

The resulting DB `gazetteer` will have the following tables (and, in parentheses, where this data has been taken from):

* Table `location`:
  * `id`: id of the location in the gazetteer
  * `wiki_id`: id of the corresponding wikipedia entry (wikipedia `page.page_id`)
  * `wikigt_id`: id of the corresponding entry in wikipedia `geo_tags` table (wikipedia `geo_tags.gt_id`)
  * `geo_id`: id of the corresponding entry in geonames (geonames `geoname.id`)
  * `wiki_title`: wikipedia title, which is the last part of a Wikipedia URL (wikipedia `page.page_title`)
  * `page_len`: wikipedia page length (wikipedia `page.page_len`)
  * `lat`: latitude corresponding to the location (wikipedia `geo_tags.gt_lat`)
  * `lon`: longitude corresponding to the location (wikipedia `geo_tags.gt_lat`) 
  * `dim`: approximate size of an object, default in metres, optional km suffix (wikipedia `geo_tags.dim`)
  * `type`: type of object with these coordinates, can be one of the following: country, satellite, state, adm1st, adm2nd, adm3rd, city, isle, mountain, river, waterbody, event, forest, glacier, airport, railwaystation, edu, pass, camera, landmark (wikipedia `geo_tags.type`)
  * `country`: country code of location (wikipedia `geo_tags.country` and geonames `geoname.countrycode`)
  * `region`: region of location (wikipedia `geo_tags.region`)
  * `population`: population of location if populated place (geonames `geoname.population`)

* Table `altname`:
  * `id`: id of the altname in the gazetteer
  * `main_id`: reference to `location.id`
  * `altname`: alternate name of the location
  * `source`: source of the alternate name. Types:
    * `wikimain`: Wikipedia title, cleaned (wikipedia `page.page_title`)
    * `wikiredirect`: Wikipedia title of a redirecting page, cleaned (wikipedia `page.page_title`)
    * `geonamesmain`: Main geonames name of location (geonames `geoname.name`)
    * `geonamesascii`: Main geonames name of location, ascii-ed, if different (geonames `geoname.asciiname`)
    * `geonamesalt`: Alternate name from geonames (geonames `alternateNamesV2.alternatename`)
    
## WikiGazetteer: Examples of queries

#### Return all locations that may be known as "Barcelona"
```
mysql> SELECT wiki_title, lat, lon, type, country, region FROM location
JOIN altname ON altname.main_id=location.id
WHERE altname="Barcelona";
```

| wiki_title                                       | lat      | lon      | type   | country | region |
|--------------------------------------------------|----------|----------|--------|---------|--------|
| Barcelona                                        |  41.3833 |  2.18333 | city   | ES      | NULL   |
| Province_of_Barcelona                            |    41.45 |  2.08333 | adm2nd | ES      | NULL   |
| Sorsogon                                         |  12.8663 |  124.145 | city   | PH      | SOR    |
| Blooming_Grove,_Ohio                             |  40.7078 | -82.7167 | city   | US      | OH     |
| Barcelona,_Venezuela                             |  10.1167 | -64.7167 | city   | NULL    | NULL   |
| Barcelona,_Sorsogon                              |    12.87 |   124.13 | NULL   | PH      | NULL   |
| Barcelona_(Congress_of_Deputies_constituency)    |    41.45 |  2.08333 | NULL   | NULL    | NULL   |
| Barcelona,_Cornwall                              |  50.3552 |  -4.5047 | NULL   | NULL    | NULL   |
| Barcelona,_Rio_Grande_do_Norte                   | -5.93333 | -35.9333 | city   | BR      | NULL   |
| Barcelona,_Arkansas                              |  35.6206 | -94.4561 | city   | US      | AR     |
| Barcelona_(Parliament_of_Catalonia_constituency) |    41.45 |  2.08333 | NULL   | NULL    | NULL   |

#### Return all possible names for Quebec City: 
```
mysql> SELECT altname, source, wiki_title FROM altname
JOIN location ON location.id=altname.main_id
WHERE wiki_title="Quebec_City";
```
| altname          | source        | wiki_title  |
|------------------|---------------|-------------|
| Quebec City      | wikimain      | Quebec_City |
| Quebec llaqta    | geonamesalt   | Quebec_City |
| Siudad ti Quebec | geonamesalt   | Quebec_City |
| Kota Quebec      | geonamesalt   | Quebec_City |
| Quebecstad       | geonamesalt   | Quebec_City |
|...|...|...|
| Kebek            | geonamesalt   | Quebec_City |
| Kebeku           | geonamesalt   | Quebec_City |
| Quebecum urbs    | geonamesalt   | Quebec_City |
| Kvebeka          | geonamesalt   | Quebec_City |
| Kebeko           | geonamesalt   | Quebec_City |
