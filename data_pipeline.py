# python my_script.py
import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__), ".", "rpg_db.sqlite3")
connection1 = sqlite3.connect(DB_FILEPATH)
cursor1 = connection1.cursor()

load_dotenv() #> loads contents of the .env file into the script's environment
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION:", connection)
cursor = connection.cursor()

query = '''
CREATE TABLE IF NOT EXISTS characters (
    "character_id" SERIAL PRIMARY KEY,
    "name" varchar,
    "level" int,
    "exp" int,
    "hp" int, 
    "strength" int, 
    "intelligence" int, 
    "dexterity" int,
    "wisdom" int)
'''

cursor.execute(query)
connection.commit()

query = 'select * from charactercreator_character'
characters = cursor1.execute(query).fetchall()

#print(result)

# query = f"INSERT INTO characters {result}"

#cursor.execute(query)


for character in characters:
  insert_character = """
    INSERT INTO characters
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ';'
  # print(insert_character)
  cursor.execute(insert_character)
  
connection.commit()















# engine = create_engine('postgres://bpsdcwgr:DGRvOs3NjG5W-1e__sckBYCDRj9SGncg@rajje.db.elephantsql.com:5432/bpsdcwgr')

# df = pd.read_csv('character.csv')
# df.to_sql(name='characters', con=engine, if_exists='replace', index = False)

