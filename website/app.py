import subprocess
import os

from flask import Flask, render_template
from connector import connect_to_database, DatabaseConnector
from typing import List

app: Flask = Flask(__name__)


def _retrieve_all_property_query() -> List[List[str]]:
    try:
        c = connect_to_database()
        cur = c.cursor()
        cur.execute("SELECT * FROM results;")
        return cur.fetchall()

    except Exception as e:
        print("Error fetiching database: ", e)
        return []


@app.route("/", methods=["GET"])
def index() -> str:
    """Flask view to return a HTML template with rendered
    Properties from the database.

    Returns:
        str: HTML page
    """
    try:
        data: List[List[str]] = DatabaseConnector().retrieve_all_property()
        return render_template("index.html", flats=data)

    except Exception as e:
        print("Error rendering index template: ", e)
        return "Error rendering page."


if __name__ == "__main__":
    """Function that runs the Sreality spider in a subprocess
    and runs Flask development server for connections.
    """
    subprocess.run("scrapy crawl sreality".split())
    app.run(host=os.environ.get("FLASK_HOST"), port=os.environ.get("FLASK_PORT"))
