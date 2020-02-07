# Oriole Data Migration

Scripts to transfer data from the Xerces MySQL database to Oriole.

## Prerequisites

pipenv is used to manage python packages. Install it first and them install the packages

```
pipenv install
```

Xlint is used to check the XML format. 

## Extract data from Xerces MySQL

Xerces data are stored in MySQL in XML format. To extract the data, run the following:

Export data from MySQL:2yeR6cSdy3

```
mysql --user=xerxes --password -h mysql.mse.jhu.edu -e "SELECT data from xerxes.xerxes_databases;" > data.txt
```

```
mysql --user=xerxes --password -h mysql.mse.jhu.edu -e "SELECT subcat_2_db.database_id as database_id, cat.name AS catname, subcat.name AS subname FROM xerxes.xerxes_user_categories cat INNER JOIN xerxes.xerxes_user_subcategories subcat ON cat.id = subcat.category_id INNER JOIN xerxes.xerxes_user_subcategory_databases subcat_2_db ON subcat.id = subcat_2_db.subcategory_id WHERE cat.published = TRUE ORDER BY 2, 3, 1" > data/xerxes_tags.csv
```

Make it an XML and clean up
```
cat data.txt | tail -n +2 | sed 's/^<\?xml.*\?>\\n//' | sed 's/\&\#xD;//g' | sed 's/\\n//g' | sed 's/<!--[^>]*-->//g' | sed '1s/^/<?xml version="1.0"?><databases>/' | sed '$s/$/<\/databases>/'  > data.xml
```

Check the format
```
xmllint --noout data.xml
```
## Load data into Oriole

Create `.env` file and configure the environment variables. Follow the example in `.env.example`.

Simply run the following:

```
pipenv run python load.py
```

## Files

- load.py: the main script to load data into Oriole
- publishers.py: the script to extract publisher data from Xerces data. See jira:OR-137
- settings.py: Loading environment variables
- .env: environment variables used by the scripts
- data: Data directory
  - data.txt, data.xml: data extracted from Xerces.
  - fast_facets.txt: list of FAST facets
  - fast_terms.txt: list of FAST terms
  - oriole_map_db_to_terms.txt: mapping of FAST term to databases.
