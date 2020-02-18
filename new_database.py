import os
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__), ".", "buddymove_holidayiq.sqlite3")
connection = sqlite3.connect(DB_FILEPATH)
c = connection.cursor()
c.execute('CREATE TABLE Review (User Id, Sports, Religious, Nature, Theatre, Shopping, Picnic)')
connection.commit() 

import pandas as pd
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00476/buddymove_holidayiq.csv')

df.to_sql(name='BuddyMove', con=connection, if_exists='replace', index = False)