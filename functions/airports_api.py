import mysql.connector
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

connect = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='flight_game_user',
         password='1234',
         autocommit=True
         )

@app.route('/airports')
def airports():
    cursor = connect.cursor()
    cursor.execute("select * from airport")
    airports = cursor.fetchall()
    cursor.close()
    return jsonify(airports)

if __name__ == '__main__':
    app.run(debug=True)