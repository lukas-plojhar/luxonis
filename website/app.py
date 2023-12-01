"""Flask application for frontend."""
import os
import subprocess

from typing import List

from connector import DatabaseConnector
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

app: Flask = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    """Display page with scraped properties.

    Fetches property data from the database and renders an HTML template
    exposing the data.

    Raises:
        HTTPException: If data cannot be retrieved from database.

    Returns:
        str: The rendered HTML page.
    """
    try:
        data: List[List[str]] = DatabaseConnector().retrieve_all_properties()
        return render_template("index.html", flats=data)

    except Exception as e:
        print("Error rendering index template: ", e)
        raise HTTPException(500, "Internal server error") from e


# If the script is run directly, start the Sreality spider and
# run the Flask development server.
if __name__ == "__main__":
    subprocess.run("scrapy crawl sreality".split())
    app.run(
        host=os.environ.get("FLASK_HOST"),
        port=os.environ.get("FLASK_PORT")
    )
