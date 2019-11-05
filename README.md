# GIR19 paper

This repository provides underlying code for the paper '*Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources*'.  

## Citation
If you use or adapt this code in your paper, please use this citation; 

Mariona Coll Ardanuy, Katherine McDonough, Amrey Krause, Daniel CS Wilson, Kasra Hosseini, Daniel van Strien (2019), **Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources**. In _Proceedings of the 13th Workshop on Geographic Information Retrieval_ (GIR'19), 2019.

## High-resolution figures

Download figures of our GIR19 paper in high-resolution:

[Figure 1](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791076/fig01.pdf) (2.6 MB)

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

### Future work and contributing 
The authors of the paper plan to continue development of the code and extension of the Gazetteer. We welcome pull requests for improvements and issues for any errors you encounter.

### License

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a [Creative Commons Attribution 4.0 International
License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
