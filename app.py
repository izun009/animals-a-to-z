from flask import Flask, g, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('animals.db')
    return db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET'])
def get_animals():
    db = get_db()
    query = db.execute('SELECT * FROM animals')
    animals = [
    	dict(
    		id=row[0],
    		name=row[1], 
    		facts=row[2],
    		) for row in query.fetchall()
    	]
    return jsonify(animals)

if __name__ == '__main__':
    app.run(debug=True)
