# Sreality.cz Property Scraper and Web Application

This project utilizes Docker containers to manage a PostgreSQL database and a Flask application with a Scrapy spider. The Scrapy spider extracts property data from Sreality.cz, a Czech real estate website, and stores the information in the PostgreSQL database. The Flask application serves a webpage that displays the first 500 entries from the [Sreality.cz property listings](https://www.sreality.cz/hledani/prodej/byty).

### Configuration

To configure the environment, set the following environment variables:

| Key | Value | Description |
| ---- | ---- | ---- |
| POSTGRES_DATABASE | postgres | Name of the PostgreSQL database |
| POSTGRES_USER | postgres | Username for the PostgreSQL database |
| POSTGRES_PASSWORD | password | Password for the PostgreSQL database |
| POSTGRES_HOST | database | Database host to connect to, i.e., container name inside Docker network |
| POSTGRES_PORT | 5432 | Exposed port for the PostgreSQL database |
| FLASK_HOST | 0.0.0.0 | Flask exposed IP address |
| FLASK_PORT | 8080 | Flask exposed port for incoming connections |

### Running the Application

To launch the application, execute the following command: 

`docker-compose up -d`

This command starts both Docker containers. The Flask application becomes accessible at [http://localhost:8080](http://localhost:8080). The Scrapy spider initially crawls data from Sreality.cz and stores it in the PostgreSQL database.

### Viewing the Webpage

Access the webpage by opening a web browser and navigating to [http://localhost:8080](http://localhost:8080). The webpage showcases the first 500 property listings from Sreality.cz.