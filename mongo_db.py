from pymongo import MongoClient
import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

# Connect to RPG Database
DB_FILEPATH = os.path.join(os.path.dirname(__file__), ".", "rpg_db.sqlite3")
connection1 = sqlite3.connect(DB_FILEPATH)
cursor1 = connection1.cursor()

# Connect to and name Mongo DB
client = MongoClient('mongodb+srv://steve122192:Sr122192@steves-cluster-blrmh.mongodb.net/test?retryWrites=true&w=majority')
db = client.sprint_practice

# 'Characters Table'-------------------------------------------------------------------------------------------

# Pull character table fom RPG DB
query = 'select * from charactercreator_character'
characters_table = cursor1.execute(query).fetchall()

# Loop through table and create dictionary to insert into new 'characters' collection in Mongo DB
characters = db.characters
for character in characters_table:
    insert_character = {
        "name":str(character[1]),
        "level":character[2],
        "exp":character[3],
        "hp":character[4],
        "strenghth":character[5],
        "intelligence":character[6],
        "dexterity":character[7],
        "wisdom":character[8]
        }
    characters.insert_one(insert_character)

# 'Items Table'-------------------------------------------------------------------------------------------

# Pull items table from RPG DB
query = 'select * from armory_item'
items_table = cursor1.execute(query).fetchall()
# Loop through table and create dictionary to insert into new 'items' collection in Mongo DB
items = db.items
for item in items_table:
    insert_item = {
        "name":str(item[1]),
        "value":item[2],
        "weight":item[3]
        }
    items.insert_one(insert_item)


# 'Titanci Data"---------------------------------------------------------------------------------------------
df = pd.read_csv('https://raw.githubusercontent.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/master/module2-sql-for-analysis/titanic.csv')

df['Survived'] = df['Survived'].astype(bool)
df.rename(columns = {'Siblings/Spouses Aboard':'sibs_spouses'}, inplace=True)
df.rename(columns = {'Parents/Children Aboard':'parents_children'}, inplace=True)
df.rename(columns = {'Parents/Children Aboard':'parents_children'}, inplace=True)
df['Age'] = df['Age'].astype(int)
df['Name'] = df['Name'].str.replace("'", '')


db = client.titanic
passengers = db.passengers
for row in df.itertuples():
    insert_row = {
        "survived":row.Survived,
        "class":row.Pclass,
        "name":str(row.Name),
        "sex":str(row.Sex),
        "age":row.Age,
        "sibs_spouses":row.sibs_spouses,
        "parents_children":row.parents_children,
        "fare":row.Fare
        }
    passengers.insert_one(insert_row)