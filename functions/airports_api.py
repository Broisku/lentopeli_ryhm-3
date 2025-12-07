import mysql.connector
from flask import Flask, jsonify
from flask_cors import CORS

from functions.get_bank_balance import give_bank_balance
from functions.view_own_airports import view_own_airports

app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='flight_game_user',
        password='1234',
        autocommit=True
    )


@app.route('/airports')
def airports():
    connect = get_connection()
    cursor = connect.cursor()
    cursor.execute("select * from airport")
    airports = cursor.fetchall()
    cursor.close()
    connect.close()
    return jsonify(airports)

@app.route('/airports/owned/<player>')
def owned_airports(player):
    connect = get_connection()
    own_airports = view_own_airports(connect, player)
    if not own_airports:
        connect.close()
        return jsonify([])
    else:
        connect.close()
        return jsonify(own_airports)

@app.route('/airports/afford/<player>')
def afford_airports(player):
    connect = get_connection()
    cursor = connect.cursor()
    if give_bank_balance(connect, player) < 3_000_000:
        connect.close()
        return jsonify([])

    elif give_bank_balance(connect, player) < 6_000_000:
        cursor.execute("select * from airport where type = 'small_airport'")
        airports = cursor.fetchall()
        cursor.close()
        connect.close()
        return jsonify(airports)

    elif give_bank_balance(connect, player) < 12_000_000:
        cursor.execute("select * from airport where type in ('medium_airport', 'small_airport')")
        airports = cursor.fetchall()
        cursor.close()
        connect.close()
        return jsonify(airports)

    else:
        cursor.execute("select * from airport")
        airports = cursor.fetchall()
        cursor.close()
        connect.close()
        return jsonify(airports)


@app.route('/money/<player>')
def money(player):
    connect = get_connection()
    bal = give_bank_balance(connect, player)
    connect.close()
    return jsonify(bal)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)