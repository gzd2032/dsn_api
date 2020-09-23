# DSN API project

This is my first attempt at creating an API.  


## Background
I was super excited to finish the Udacity Full Stack Nanodegree, and i couldn't wait to start a project.  I browsed the Airmen Coders github repository to see how i could contribute, and this is where i discovered a need for a DSN Converter web app.  

Instead of creating a monolotithic full-stack web app, i decided follow the cloud-native microservices approach and create a backend API first.  This was inspired by the many public api's available such as pokeapi.co, worldtimeapi.org, and exchangeratesapi.io.

My goal was to create an API where others could freely develop a frontend to use the data.

## Server Setup Basics

This API will serve a list of DSN prefixes with its commercial prefix equivalent and associated locations.

### Installing Dependencies

#### Python 3.8.2

This application was built on the latest version of python v3.8.2

#### Virtual Enviornment

If required, in the main directory create a virtual environment: 

example setup using virtual env
``` 
virtualenv env
source ~env/bin/activate
```

#### PIP Dependencies

Once the virtual environment is setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to send and retreive data from postgres or any compatible database server. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from a frontend server. 

## Database Setup
The dsn.psql file contains a postgres database backup of all the dsn prefixes and locations.  With Postgres running, create a database named "dsn", then restore the database using the dsn.psql file. In the main directory, run the following commands in a terminal window:

```bash
createdb dsn
psql dsn < dsn.psql
```

## Running the server

The server requires the following environment variable:

DATABASE_URL=(postgres server information)

To run the server, execute the following command in the main directory:

```bash
export FLASK_APP=app.py

flask run
```

## Endpoints

### GET Endpoints
- '/' - Provides a standard static html page that describes the API.
- '/locations' - returns a "locations" object that includes an array of location objects.
- '/prefixes' - returns a "prefix_list" object that includes an array of prefix objects.
- '/prefixes/dsn' - returns a "dsn" object with an array of available dsn prefixes.
- '/prefixes/dsn/<dsn_prefix>' - returns a "prefix_list" object that includes an array of all dsn objects that match "dsn_prefix".  Allows partial DSN matching and returns an array of matches
- '/prefixes/comm' - returns a "comm" object with an array of commercial prefixes.  Allows partial text matching and returns an array of matches. 
- '/prefixes/comm/<comm_prefix>' - returns a "comm" object with an array of commercial prefixes.

### POST Endpoints
- '/locations' - Use this endpoint to add a new location. Send JSON data in the following format:
```
{ "name": "Naval Station Rota"  }
```

- '/prefixes' - Use this endpoint to add a new DSN prefix.  Send JSON data in the following format:
```
{  "comm_prefix": "+49 6119 744", 
    "description": "Germany", 
    "dsn_prefix": "570", 
    "location_id": 20
}
```

### PATCH Endpoints
- '/locations/&lt;int:location_id&gt;' - Submit a JSON object to update the name of the location.  
```
{ "name": "Naval Station Rota"  }
```

- '/prefixes/&lt;int:prefix_id&gt;' - Submit a JSON object to update information for a prefix.  Ensure the location_id associated with the prefix is a valid location id. 
```
{  "comm_prefix": "+49 6119 744", 
    "description": "Germany", 
    "dsn_prefix": "570", 
    "location_id": 20
}        
```

### DELETE Endpoints
- '/locations/&lt;int:location_id&gt;' - Delete a location by submitting a valid location_id to this endpoint. Warning! Deleting a location will also delete all prefixes associated with that location.  

- '/prefixes/&lt;int:prefix_id&gt;' - Delete a prefix by submitting a valid prefix_id to this endpoint.
