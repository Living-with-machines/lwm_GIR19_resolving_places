# GIR19 paper

This repository provides underlying code for the paper '*Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources*'.  

## Citation
If you use or adapt this code in your paper, please use this citation; 

Mariona Coll Ardanuy, Katherine McDonough, Amrey Krause, Daniel CS Wilson, Kasra Hosseini, Daniel van Strien (2019), **Resolving Places, Past and Present: Toponym Resolution in Historical British Newspapers Using Multiple Resources**.

## High-resolution figures

Download figures of our GIR19 paper in high-resolution:

[Figure 1](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791076/fig01.pdf) (2.6 MB)

[Figure 2](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791083/fig02.pdf) (12.1 MB)

[Figure 3](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791087/fig03.pdf) (7 MB)

[Figure 4](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/files/3791090/fig04.pdf) (2.6 MB)

# Creating your own wikiGazetteer

To setup your own version of wikiGazetteer please;

- install the required packages via Anaconda (see below for instructions) 

## Installation of required packages 

1. Install Anaconda following [these instructions](https://docs.anaconda.com/anaconda/install/).

2. Create `gir19` environment:

```bash
conda env create -f environment.yml
```

3. Activate `gir19` environment:

```bash
source activate gir19
```

## Install MySQL 

- The steps for installing MySQL will vary by platform. A good starting place will by the MySQL [documentation](https://dev.mysql.com/doc/)
- The GIR code makes use of [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) to connect to the MySQL server. This will have been installed in the environment you created above. 

### MySQL Authentication 
- The code in this repo has a default [username and password](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/blob/master/gazetteer_construction/addLocations.py#L178
) for connecting to MySQL you will need to change this if you setup your MySQL server with a different password 

### Creating your own wikiGazetteer
[Full instructions](https://github.com/alan-turing-institute/lwm_GIR19_resolving_places/tree/master/gazetteer_construction) outline the steps to create a wikiGazetteer yourself. 


## Future work and contributing 
The authors of the paper plan to continue development of the code and extension of the Gazetteer. We welcome pull requests for improvements. 
