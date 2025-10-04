import mysql.connector

yhteys = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    database = 'flight_game',
    user = 'flight_game_user',
    password = '1234',
    autocommit = True
)

username = input('Enter your username: ')
sql = f'''
insert into game(name)
values('{username}')
'''