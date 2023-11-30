import subprocess
import os

from typing import List

from connector import DatabaseConnector
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

app: Flask = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    """Fetches property data from the database and renders an HTML template
    presenting the data.

    Returns:
        str: The rendered HTML page.
    """
    try:
        data: List[List[str]] = DatabaseConnector().retrieve_all_properties()
        return render_template("index.html", flats=data)

    except Exception as e:
        print("Error rendering index template: ", e)
        raise HTTPException(500, "Internal server error")


if __name__ == "__main__":
    """Starts the Sreality spider in a subprocess to scrape data
    and runs the Flask development server for connections.
    """
    subprocess.run("scrapy crawl sreality".split())
    app.run(host=os.environ.get("FLASK_HOST"), port=os.environ.get("FLASK_PORT"))
