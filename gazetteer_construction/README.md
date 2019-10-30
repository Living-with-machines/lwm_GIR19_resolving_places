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
```

_Note:_ the Wikipedia version discussed in the GIR19 paper is `20190320`: to reproduce the same analysis, just replace `latest` by `20190320` in the URLs. If you want to create a gazetteer in any other language, change the Wikipedia language code in the URLs (e.g. `enwiki` to `cawiki`, check for [reference](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)).








Create the `wikiGazetteer` database:
```
mysql> CREATE DATABASE wikiGazetteer;
mysql> USE wikiGazetteer;
mysql> ALTER DATABASE wikiGazetteer CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
mysql> exit;
```
