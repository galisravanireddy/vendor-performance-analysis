import os
import time
import logging
import pandas as pd
from sqlalchemy import create_engine

# 1. Setup Logging Configuration
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# 2. Initialize Database Connection
engine = create_engine('sqlite:///inventory.db')

# 3. Definining the helper database ingestion function
def ingest_db(df, table_name, engine):
    '''this function will ingest the dataframe into database table'''
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

# 4. Defining the main file reading and timing function
def load_raw_data():
    '''this function will load the CSVs as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir('.'):
        if '.csv' in file:
            df = pd.read_csv(file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
            
    end = time.time()
    total_time = (end - start) / 60
#5 spaces of indentation here:
    logging.info('-------------------Ingestion Complete-------------------')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')
# completely left-aligned (no indentation):
load_raw_data()