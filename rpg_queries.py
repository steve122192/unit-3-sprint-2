import os
import sqlite3
# construct a path to wherever your database exists
DB_FILEPATH = os.path.join(os.path.dirname(__file__), ".", "rpg_db.sqlite3")
connection = sqlite3.connect(DB_FILEPATH)

cursor = connection.cursor()

print('How many total Characters are there?')
query = '''
select 
	count(distinct character_id)
from charactercreator_character
'''

result = cursor.execute(query).fetchall()
print(result[0])

print('\n')
print('How many of each specific subclass?')

query = '''
SELECT
    *
FROM
    (SELECT COUNT(DISTINCT character_ptr_id) as clerics FROM charactercreator_cleric)
    ,(SELECT COUNT(DISTINCT character_ptr_id) as fighters FROM charactercreator_fighter)
    ,(SELECT COUNT(DISTINCT character_ptr_id) as mages FROM charactercreator_mage)
    ,(SELECT COUNT(DISTINCT mage_ptr_id) as necromancers FROM charactercreator_necromancer)
    ,(SELECT COUNT(DISTINCT character_ptr_id) as thieves FROM charactercreator_thief)
'''

result = cursor.execute(query).fetchall()
print(result)
print('\n')

# How many total Items?
print('How many total Items?')
query = '''
select 
	count(distinct item_id)
from armory_item
'''

result = cursor.execute(query).fetchall()
print(result[0])
print('\n')

# How many of the Items are weapons? How many are not?

print('How many of the Items are weapons? How many are not?')
query = '''
select
	count(distinct item_ptr_id) as weapons_count,
	count(distinct item_id) as items_count
	
from armory_item
LEFT JOIN armory_weapon ON armory_item.item_id = armory_weapon.item_ptr_id
'''

result = cursor.execute(query).fetchall()
print(result[0])
print('\n')

# How many Items does each character have? (Return first 20 rows)

print('How many Items does each character have? (Return first 20 rows)')
query = '''
select
	charactercreator_character.name,
	count(distinct item_id) as items_count
	
from charactercreator_character_inventory
join charactercreator_character on charactercreator_character_inventory.character_id = charactercreator_character.character_id
group by name
order by items_count DESC
limit 20
'''

result = cursor.execute(query).fetchall()
print(result)
print('\n')

# How many Weapons does each character have? (Return first 20 rows)

print('How many Weapons does each character have? (Return first 20 rows)')
query = '''
select
	charactercreator_character.name,
	count(distinct item_ptr_id) as weapons_count
	
from charactercreator_character_inventory
join charactercreator_character on charactercreator_character_inventory.character_id = charactercreator_character.character_id
join armory_weapon on item_id = armory_weapon.item_ptr_id
group by name
order by weapons_count DESC
limit 20
'''

result = cursor.execute(query).fetchall()
print(result)
print('\n')

# # On average, how many Items does each Character have?
# print('On average, how many Items does each Character have?')
# query = '''
# select
# 	charactercreator_character.name,
# 	count(distinct item_ptr_id) as weapons_count
	
# from charactercreator_character_inventory
# join charactercreator_character on charactercreator_character_inventory.character_id = charactercreator_character.character_id
# join armory_weapon on item_id = armory_weapon.item_ptr_id
# group by name
# order by weapons_count DESC
# limit 20
# '''

# result = cursor.execute(query).fetchall()
# print(result)

# On average, how many Weapons does each character have?
print('On average, how many Weapons does each character have?')
query1 = '''
CREATE TABLE weapons_totals
as select
	charactercreator_character.name,
	count(distinct item_ptr_id) as weapons_count
	
from charactercreator_character_inventory
join charactercreator_character on charactercreator_character_inventory.character_id = charactercreator_character.character_id
join armory_weapon on item_id = armory_weapon.item_ptr_id
group by name
order by weapons_count DESC;
'''
query2 = '''
SELECT avg(weapons_totals.weapons_count)
FROM weapons_totals;
'''
new_table = cursor.execute(query1)
result = new_table.execute(query2).fetchall()


print(result)




print('----------------------------')
query6 = """
SELECT
	character_id,
	count(DISTINCT item_id) as item_count
FROM charactercreator_character_inventory
GROUP BY character_id
"""
result = cursor.execute(query6)
print(result)
total_items = 0
count = 0
for row in result:
    total_items += row[1]
    count += 1
print(f"On average, each character has {(total_items/count):.2f} items.")