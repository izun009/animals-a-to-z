from flask import Flask, g, jsonify
import sqlite3
import mysql.connector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from animals_a_to_z.spiders.animals import AnimalsSpider

app = Flask(__name__)

# def get_db():
#     db = sqlite3.connect('animals.db')
#     return db

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


# @app.route('/', methods=['GET'])
# def get_animals():
#     db = get_db()
#     query = db.execute('SELECT * FROM animals')
#     animals = [
#     	dict(
#     		id=row[0],
#     		name=row[1], 
#     		facts=row[2],
#     		) for row in query.fetchall()
#     	]
#     return jsonify(animals)

def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="izzen",
        password="1234",
        database="animals_a_to_z"
    )
    return db

@app.route('/api/mydata', methods=['GET'])
def get_data():
    db = get_db()
    # Run the Scrapy spider and store data in MySQL
    process = CrawlerProcess(get_project_settings())
    process.crawl(AnimalsSpider, db=db)
    process.start()

    # Retrieve the data from MySQL and return as JSON
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM animals")
    data = cursor.fetchall()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
