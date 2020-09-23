# DSN API project

This is first attempt at creating an API.  


## Background
I was super excited to finish the Udacity Full Stack Nanodegree, and i couldn't wait to start a project.  I browsed the Airmen Coders github repository to see how i could contribute, and this is where i discovered a need for a DSN Converter web app.  

Instead of creating a monolotithic full-stack web app, i decided follow the cloud-native microservices approach and create a backend API first.  This was inspired by the many public api's available such as pokeapi.co, worldtimeapi.org, and exchangeratesapi.io.

My goal was to create an API where others could freely develop a frontend to use the data.

## Server Setup Basics

This API can be used to retrieve lists of DSN prefixes with its commercial prefix equivalent and associated locations.

### Installing Dependencies

#### Python 3.8.2

This application was built on the latest version of python 3.8.2

#### Virtual Enviornment

In the main directory create a virtual environment: 

example setup using virtual env
``` virtual env
source ~env/bin/activate
```

#### PIP Dependencies

Once the virtual environment is setup and running, install dependencies by  running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from a frontend server. 

## Database Setup
The dsn.psql file contains a backup of a postgres database with all the dsn prefixes and locations.  With Postgres running, create a database name dsn, then restore the database using the dsn.psql file. From the backend folder in terminal run:
```bash
createdb dsn
psql dsn < dsn.psql
```

## Running the server

In the mail directory, make sure you are working using your created virtual environment.
To run the server, execute:

```bash
export FLASK_APP=app.py

flask run
```

## Endpoints

### GET Endpoints
- '/' - This welcome page
- '/locations' - returns a "locations" object that includes an array of location objects.
- '/prefixes' - returns a "prefix_list" object that includes an array of prefix objects.
- '/prefixes/dsn' - returns a "dsn" object with an array of available dsn prefixes.
- '/prefixes/dsn/<dsn_prefix>' - returns a "prefix_list" object that includes an array of all dsn objects that match "dsn_prefix".  Allows partial DSN matching and returns an array of matches
- '/prefixes/comm' - returns a "comm" object with an array of commercial prefixes.  Allows partial text matching and returns and array of matches. 
- '/prefixes/comm/<comm_prefix>' - returns a "comm" object with an array of commercial prefixes.

### POST Endpoints
- '/locations' - Use this endpoint to add a new location. 
{ "name": "Naval Station Rota"  }
- '/prefixes' - Use this endpoint to add a new DSN prefix 
{  "comm_prefix": "+49 6119 744", 
    "description": "Germany", 
    "dsn_prefix": "570", 
    "location_id": 20
}
           
### PATCH Endpoints
- '/locations/<int:location_id>' - Submit a JSON object to update the name of the location. 
{ "name": "Naval Station Rota"  }
- '/prefixes/<int:prefix_id>' - Submit a JSON object to update information for a prefix.  Ensure the location_id is a valid id. 
{  "comm_prefix": "+49 6119 744", 
    "description": "Germany", 
    "dsn_prefix": "570", 
    "location_id": 20
}        

### DELETE Endpoints
- '/locations/<int:location_id>' - Delete a location by submitting a valid location_id to the endpoint. 
- '/prefixes/&l
