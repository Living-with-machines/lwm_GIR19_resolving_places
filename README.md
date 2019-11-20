[![DOI](https://zenodo.org/badge/218500126.svg)](https://zenodo.org/badge/latestdoi/218500126)

# GIR19 paper

This repository provides underlying code for the paper '*Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources*'.  

## Citation
If you use or adapt this code in your paper, please use this citation; 

Mariona Coll Ardanuy, Katherine McDonough, Amrey Krause, Daniel CS Wilson, Kasra Hosseini, Daniel van Strien, **Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources**. In _Proceedings of the 13th Workshop on Geographic Information Retrieval_ (GIR'19), Forthcoming.

## What is this?

**Resolving Places** is one of the first outputs of Living with Machines, a collaborative digital history project at The Alan Turing Institute and the British Library. This research is part of our work to build a nineteenth-century gazetteer that combines place names derived from historical sources ([GB1900](http://www.beta.visionofbritain.org.uk/gbhdb/section/gb1900)) with online resources (Wikipedia and Geonames). GB1900 is the result of a crowdsourced project that transcribed all text labels on the 2nd edition 6-inch to 1 mile Ordnance Survey maps of Great Britain (ca. 1900) held by the National Library of Scotland ([NLS Maps online](https://maps.nls.uk/os/6inch-england-and-wales/)). 

The Living with Machines gazetteer follows best practices in combining multiple existing resources, and is novel in accounting for places that have different scales (e.g. streets, buildings, cities, counties). In the future, we will be adding records and enriching current records with information from OS map 1st edition map label data and other sources.


## High-resolution figures

Download figures of our GIR19 paper in high-resolution:

[Figure 1](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3815472/manual_dorset_newspapers.pdf) (3 MB)

[Figure 2](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791083/fig02.pdf) (12.1 MB)

[Figure 3](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791087/fig03.pdf) (7 MB)

[Figure 4](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791090/fig04.pdf) (2.6 MB)

## Creating your own wikiGazetteer and reproducing the analysis

To setup your own version of wikiGazetteer and reproducing the analysis in the paper please;
- install the required packages via Anaconda (see below for instructions) 

### Install the required packages 

1. Install Anaconda following [these instructions](https://docs.anaconda.com/anaconda/install/).

2. Create `gir19` environment:

```bash
conda env create -f environment.yml
```

3. Activate `gir19` environment:

```bash
source activate gir19
```

### Install MySQL 

#### Creating your own wikiGazetteer
[Full instructions](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/tree/master/gazetteer_construction) outline the steps to create a wikiGazetteer yourself. You will need MySQL installed:
- The steps for installing MySQL will vary by platform. A good starting place will by the MySQL [documentation](https://dev.mysql.com/doc/).
- The GIR code makes use of [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) to connect to the MySQL server. This should have been installed in the environment you created above. 

#### MySQL Authentication 
- The code in this repo has a default username and password (see [here](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/blob/master/gazetteer_construction/addLocations.py#L178) and [here](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/blob/master/gazetteer_construction/addRedirections.py#L66)) for connecting to MySQL you will need to change this if you setup your MySQL server with a different password .

## Future work and contributing 
The authors of the paper plan to continue development of the code and extension of the Gazetteer. We welcome pull requests for improvements and issues for any errors you encounter.

## Get in touch
You can reach us by email:
- Mariona Coll Ardanuy, mcollardanuy[at]turing.ac.uk
- Katherine McDonough, kmcdonough[at]turing.ac.uk
- Amrey Krause, akrause[at]turing.ac.uk
- Daniel CS Wilson, dwilson[at]turing.ac.uk
- Kasra Hosseini, khossienizad[at]turing.ac.uk
- Daniel van Strien, Daniel.Van-Strien[at]bl.uk


## Acknowledgements 

This work is part of the [Living with Machines project](http://livingwithmachines.ac.uk). Living with Machines is a multidisciplinary programme funded by the Strategic Priority Fund which is led by UK Research and Innovation (UKRI) and delivered by the Arts and Humanities Research Council (AHRC). Newspaper data was kindly shared by [Findmypast](https://www.findmypast.co.uk/). We thank Chris Fleet and the [National Library of Scotland](https://www.nls.uk) for sharing digital map images and metadata for OS collections as well as context about GB1900. Thank you also to Humphrey Southall, Paula Aucott, and Richard Light for discussing the future of GB1900.

## License

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a [Creative Commons Attribution 4.0 International
License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
