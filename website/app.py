import subprocess
from flask import Flask, render_template
from connector import connect_to_database
from typing import List


app: Flask = Flask(__name__)


def _retrieve_all_property_query() -> List[List[str]]:
    c = connect_to_database()
    cur = c.cursor()
    cur.execute("SELECT * FROM results;")
    return cur.fetchall()

@app.route("/", methods=["GET"])
def index() -> str:
    """Flask view to return a HTML template with rendered
    Properties from the database.

    Returns:
        str: HTML page
    """
    data: List[List[str]] = _retrieve_all_property_query()
    return render_template("index.html", flats=data)

if __name__ == "__main__":
    """Function that runs the Sreality spider in a subprocess 
    and runs Flask development server for connections.
    """
    subprocess.run("scrapy crawl sreality".split())
    app.run(host="0.0.0.0", port=8080)
    