This folder contains local sqlite databases used in development and testing deployments. 
dev.db is default sqlite development database and can be manipulated directly by running:

nihlapp/db$ sqlite3 dev.db

To create or recreate local database from fixtures, run the following from nihlapp folder:

nihlapp$ python resetdb.py
