import os
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__), ".", "sprint-review.db")
connection = sqlite3.connect(DB_FILEPATH)
c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS review (student, studied, grade, age, sex)')
connection.commit() 

# query = '''
# INSERT INTO students (student, studied, grade, age, sex)
# VALUES
#     ('Lion-O', 'True', 85, 24, 'Male'),
#     ('Cheetara', 'True', 95, 22, 'Female'),
#     ('Mumm-Ra', 'False', 65, 153, 'Male'),
#     ('Snarf', 'False', 70, 15, 'Male'),
#     ('Panthro', 'True', 80, 30, 'Male')
# '''
# c.execute(query)
# connection.commit()

query = 'select avg(age) as avg_age from students'
result = c.execute(query).fetchone()
print(f'Average Age: {str(result[0])}')









 