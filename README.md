# Python_Assignment_5_Parking_Copenhagen

## Assignment: Parking spots info - https://github.com/rmlassesen/dataset?fbclid=IwAR2Du2t4Ji8NMNriaVH5n0rBcjO1WRyCblCHh2Pyu5ZD5L2LxC-gw7gegcU

## Group
Foolish Supermarket - Alexander (cph-ah353), Stanislav (cph-sn186), Mathias B. (cph-mb493), Mikkel L. (cph-ml474)

## Project Description
This is a program written to interact with two specific datasets.
URL to the dataset is in the code:
Parking info : http://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:p_pladser&outputFormat=csv&SRSNAME=EPSG:4326

Brutto income : https://data.kk.dk/dataset/e734af29-4e40-4754-9cce-789a7513dd8a/resource/bd5b19ee-cedd-4b69-9272-532a1bce1eee/download/indkomstbruttohustypev.csv

## How to run (from CLI)
In root of folder, in your terminal of choice, write:

This project requires Anaconda distribution of python

> To run project
```python main.py```


## Results

1. Hvor mange p-pladser er der i Indre By? 
    - Hvilken vej har flest?

    *There is 12183 in `Indre By` and the street with most spots is Stockholmsgade with 291 spots*
2. Er der i København flest p-pladser i den side af vejen med lige eller ulige husnumre?
    *There are 13381 even spots and 12168 uneven spots in Copenhagen; Most spots at the even side of the road.*
- Hvilken side har flest afmærkede parkeringsbåse?
    *- There are 2837 even marked spots and 7114 uneven marked spots; Most marked spots at the uneven side of the road.*

3. Vis med et splittet bar-plot den procentvise fordeling(y-aksen) af private og offentlige p-pladser i hver by-del(x-aksen)
    >Inkludér brutto indkomst dataset

4. Hvilken familietype har de bedste parkeringsmuligheder?

5. Vis fordelingen af private parkeringspladser og parkeringsmuligheder for el-biler ift hver bydels gennemsnitlige bruttoindkomst.

6. Farvekod på et kort bydelene i København, ud fra den gennemsnitlige bruttoindkomst. Plot markers med private (P) og el-bil-parkeringspladser (EL)
