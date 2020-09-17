# omdemna_web_scrapping
## Description
Information extraction from official Sources for different states of latinoamerica.

Structured using Country codes and States codes. (GADM)
## Includes:
Including: Leyes Federales de México (145 - 0)
Including: Asamblea Legislativa de México (70 - 0)

## Deployment:
*  Install python dependencies

        pip install requests
        pip install pickle
        pip install bs4
        pip install tqdm
        pip install pandas
        
*  run main.py in root folder.

It's configured in order to start exploring the web looking for all references, storing them as **resources.p** file. 
It will generate a *.CSV* with a table with all the references.
Next it will download all documents using multiple threads as **filename.pdfs** in **codes/country/** directory.
    