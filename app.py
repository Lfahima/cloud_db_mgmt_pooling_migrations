from flask import Flask, render_template, request, redirect
import pandas as pd
import random
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy import create_engine, inspect


app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('base.html', name = "Fahima")

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/random')
def randomnumber():
    number_var = random.randint(1, 10000)
    return render_template('random.html', single_number = number_var)



"""

This script uses the pymysql library for connecting to MySQL, 
so you might need to install that (pip install pymysql) if you haven't already.

It also uses python-dotenv for bringing in secrets from your .env file 

The .env should have the following in it:

DB_HOST=your_host
DB_DATABASE=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_PORT=3306
DB_CHARSET=utf8mb4

The default port is set to 3306 for MySQL, but you can override it by 
modifying the DB_PORT in your .env file.

The connection string is MySQL-specific, incorporating the specified port and charset.

"""

load_dotenv()  # Load environment variables from .env file

# Database connection settings from environment variables
DB_HOST_AZURE = os.getenv("DB_HOST_AZURE")
DB_DATABASE_AZURE = os.getenv("DB_DATABASE_AZURE")
DB_USERNAME_AZURE = os.getenv("DB_USERNAME_AZURE")
DB_PASSWORD_AZURE = os.getenv("DB_PASSWORD_AZURE")
DB_HOST_GCP = os.getenv("DB_HOST_GCP")
DB_DATABASE_GCP = os.getenv("DB_DATABASE_GCP")
DB_USERNAME_GCP = os.getenv("DB_USERNAME_GCP")
DB_PASSWORD_GCP = os.getenv("DB_PASSWORD_GCP")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string_azure = (
    f"mysql+pymysql://{DB_USERNAME_AZURE}:{DB_PASSWORD_AZURE}@{DB_HOST_AZURE}:{DB_PORT}/{DB_DATABASE_AZURE}"
    f"?charset={DB_CHARSET}"
)
ssl_args = {'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'}
# Create a database engine
db_engine_azure = create_engine(conn_string_azure, pool_size=1,connect_args=ssl_args, max_overflow=0, echo=False)

conn_string_gcp = (
    f"mysql+pymysql://{DB_USERNAME_GCP}:{DB_PASSWORD_GCP}@{DB_HOST_GCP}:{DB_PORT}/{DB_DATABASE_GCP}"
    f"?charset={DB_CHARSET}"
)
db_engine_gcp = create_engine(conn_string_gcp, pool_size=1,connect_args=ssl_args, max_overflow=0, echo=False)

def get_tables(engine): 
    """Get list of tables."""
    inspector = inspect(engine)
    return inspector.get_table_names()

def execute_query_to_dataframe(query: str, engine):
    """Execute SQL query and return result as a DataFrame."""
    return read_sql(query, engine)


# Example usage
# tables = get_tables(db_engine_azure)
# print("Tables in the database:", tables)


sql_query = "SELECT * FROM patient"  # Modify as per your table
df_azure = execute_query_to_dataframe(sql_query, db_engine_azure)
df_gcp = execute_query_to_dataframe(sql_query, db_engine_gcp)


sql_query2 = "SELECT * FROM admission"  # Modify as per your table
df2_azure = execute_query_to_dataframe(sql_query2, db_engine_azure)
df2_gcp = execute_query_to_dataframe(sql_query2, db_engine_gcp)


@app.route('/data')
def data(data_azure=df_azure, data2_azure=df2_azure, data_gcp=df_gcp, data2_gcp=df2_gcp):
    return render_template('data.html', data_azure=data_azure, data2_azure=data2_azure, data_gcp=data_gcp, data2_gcp=data2_gcp)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )