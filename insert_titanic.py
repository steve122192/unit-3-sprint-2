import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd 

load_dotenv() #> loads contents of the .env file into the script's environment
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION:", connection)
cursor = connection.cursor()
print("CURSOR:", cursor)
# TODO: create a new table
query = """
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    survived bool,
    pclass int,
    name varchar,
    sex varchar,
    age int,
    sib_spouse_count int,
    parent_child_count int,
    fare float8
);
"""
cursor.execute(query)
connection.commit() # actually update the database

df = pd.read_csv('https://raw.githubusercontent.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/master/module2-sql-for-analysis/titanic.csv')
df['Survived'] = df['Survived'].astype(bool)
df.rename(columns = {'Siblings/Spouses Aboard':'sibs_spouses'}, inplace=True)
df.rename(columns = {'Parents/Children Aboard':'parents_children'}, inplace=True)
df.rename(columns = {'Parents/Children Aboard':'parents_children'}, inplace=True)
df['Age'] = df['Age'].astype(int)
df['Name'] = df['Name'].str.replace("'", '')

for row in df.itertuples():
    insert_rows = """
    INSERT INTO passengers
    (survived, pclass, name, sex, age, sib_spouse_count, parent_child_count, fare)
    VALUES """ + '(' + str(row.Survived) + ', ' + str(row.Pclass) + ', '+ "'" + str(row.Name) + "'" + ", '" + str(row.Sex) + "', " +  str(row.Age) + ', ' +  str(row.sibs_spouses) + ', ' + str(row.parents_children) + ', ' + str(row.Fare) + ');'
    cursor.execute(insert_rows)

connection.commit()