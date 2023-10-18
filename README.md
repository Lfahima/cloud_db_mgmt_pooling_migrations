# cloud_db_mgmt_pooling_migrations
This is assignment #4C for HHA 504


## Explain the setup and configuration of connection pooling for Azure and GCP databases.
For the setup and configuration of connection pooling for Azure databases I first clicked on server parameters which is on the left hand side under settings. I then located connect_timeout and typed a 3 in the bar next to it and then located max_connections and typed a 20 in the bar next to it. 


## Describe the database schema structure, including the rationale behind it.
I created two tables, one table titled patient, which included id as the primary key and patient_DOB (date of birth). My second table was titled admission, which included id as the primary key, admission_datetime (which is the date and time the patient had their admission), and patient_id as the foreign key. 


## Document the steps and challenges encountered during the database migration process.
#### Steps :
I followed the steps for the database migration process provided by Professor Hants in the python files. 
The first step I conducted was I updated the classes to reflect what I wanted, I then updated the engine connection detials. I then followed by running the migration init command. 
I updated the alembic.ini file with the url. 
The first migration I performed was on GCP, so I updated the env.py file to use the gcp file. from there I ran the migration. 
At first I had issues with connecting to the database, but then I realized my connection stream was wrong and I fixed it. I also realized that my classes had incorrect column values, so I updated the classe in the file, and then droped the tables. I then created the tables again, inserted fake values in the tables, and re-ran the migration. After a successful run, I proceeded to perform the same migration on Azure and it also ran successfully.  