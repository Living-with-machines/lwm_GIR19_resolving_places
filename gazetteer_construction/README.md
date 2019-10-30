# Building a gazetteer

This document explains how to generate WikiGazetteer, a gazetteer based on Wikipedia and enriched with Geonames data. This is the alpha version of the code, and therefore does not have all the features that have been envisaged for future releases of the gazetteer.

**To cite:**

> Mariona Coll Ardanuy, Katherine McDonough, Amrey Krause, Daniel CS Wilson, Kasra Hosseini, and Daniel van Strien, “Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources,” in Proceedings of the 13th Workshop on Geographic Information Retrieval, 2019 (GIR19).

This is the step-by-step description on how to create the alpha version of the gazetteer from an English version of Wikipedia.

To build a gazetteer in any other language (i.e. based on a different Wikipedia), you'll need to change:

```CHAAAANGE!!!```

Creating a gazetteer out of a smaller Wikipedia might be useful for testing purposes.

## Steps to create WikiGazetteer

**1. Create the `wiki_db` database:**
```
mysql> CREATE DATABASE wiki_db;
mysql> USE wiki_db;
mysql> ALTER DATABASE wiki_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
mysql> exit;
```

**2. Download relevant Wikipedia tables and upload them to the `wiki_db` database:**
```
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-redirect.sql.gz
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-geo_tags.sql.gz

$ gzip -d enwiki-latest-geo_tags.sql.gz 
$ gzip -d enwiki-latest-page.sql.gz 
$ gzip -d enwiki-latest-redirect.sql.gz 

$ mysql -u root -p wiki_db < enwiki-latest-page.sql 
$ mysql -u root -p wiki_db < enwiki-latest-redirect.sql 
$ mysql -u root -p wiki_db < enwiki-latest-geo_tags.sql 

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

**Populate the `wikiGazetteer` database:**
```
$ python addLocations.py 
$ python addRedirections.py 
```

**Add indices to `wikiGazetteer` database:**
```
mysql> use wikiGazetteer
mysql> ALTER TABLE location ADD INDEX(id); 
mysql> ALTER TABLE altname ADD INDEX(altname); 
mysql> exit;
```
