"""Flask application for frontend."""
import os
import subprocess

from typing import List, Tuple

from connector import DatabaseConnector
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

# Initialize application with environment variables
app: Flask = Flask(__name__)
app.config["FLASK_HOST"] = os.environ.get("FLASK_HOST", "0.0.0.0")
app.config["FLASK_PORT"] = int(os.environ.get("FLASK_PORT", 5000))


@app.route("/", methods=["GET"])
def index() -> str:
    """Display page with scraped properties.

    Fetches property data from the database and renders an HTML template
    exposing the data.

    Raises:
        HTTPException: If data cannot be retrieved from database or
        rendering fails.

    Returns:
        str: The rendered HTML page.
    """
    try:
        properties: List[Tuple[str]] = DatabaseConnector().retrieve_all_properties()
        return render_template("index.html", flats=properties)

    except Exception as e:
        print(f"Error rendering index template: {e}")
        raise HTTPException(500, "Internal server error") from e


# If the script is run directly, start the Sreality spider and
# run the Flask development server.
if __name__ == "__main__":
    subprocess.run("scrapy crawl sreality".split())
    app.run(
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"]
    )
