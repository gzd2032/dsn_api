# DSN API project

This is my first attempt at creating an API.  


## Background
I was super excited to finish the Udacity Full Stack Nanodegree, and i couldn't wait to start a project.  I browsed the Airmen Coders github repository to see how i could contribute, and this is where i discovered a need for a DSN Converter web app.  

Instead of creating a monolotithic full-stack web app, i decided follow the cloud-native microservices approach and create a backend API first.  This was inspired by the many public api's available such as pokeapi.co, worldtimeapi.org, and exchangeratesapi.io.

My goal was to create an API where others could freely develop a frontend to use the data.

## Server Setup Basics

This API will serve a list of DSN prefixes in the EUCOM AOR with its commercial prefix equivalent and associated locations.

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

- '/' - This welcome page.

- '/locations' - returns a dictionary with a "locations" key and a value that is an array of location dictionaries.

Example response:  
```
{
    "locations": [{
            "id": 1, 
            "name": "Baumholder"
        }, {
            "id": 2, 
            "name": "Brunssum (NL)"
        } 
        ...] 
}
```
- '/prefixes' - returns a dicitonary with a "prefix_list" key and a value of a dictionary of prefixes.  The DSN and Commercial prefixes are stored as strings. 

Example response:  
```
{
    "prefix_list": {
    "226": "+44 1638 52:RAF Lakenheath", 
    "236": "+44 1280 70:RAF Croughton", 
    "336": "+49 6118 16:Wiesbaden", 
    ... } 
}
```
- '/prefixes/dsn' - returns a dictionary with a key of "dsn" and an array of DSN prefix dictionaries.  The DSN and Commercial prefixes are stored as strings. 

Example response: 
```
{
    "dsn": [{
        "comm_prefix": "0611-143-546", 
        "description": "", 
        "dsn_prefix": "546", 
        "id": 27, 
        "location": "Mainz/Kastel", 
        "location_id": 13
    }, 
    {
        "comm_prefix": "0611-143-523", 
        "description": "", 
        "dsn_prefix": "523", 
        "id": 30, 
        "location": "Mainz/Kastel", 
        "location_id": 13
    },
    ...]} 
```

- '/prefixes/dsn/<dsn_prefix>' - returns a dictionary with a key of "prefix_list" and a value of an array of DSN prefix dictionaries.  Allows partial DSN matching and returns an array of matches.  

Example response for '/prefixes/dsn/480' :  
```
{
    "prefix_list": [{
        "comm_prefix": "+49 6371 47", 
        "description": "", 
        "dsn_prefix": "480", 
        "id": 37, 
        "location": "Ramstein", 
        "location_id": 16
    }]
}
```

- '/prefixes/comm' - returns a dictionary with a key of "comm" and a value of an array of commercial prefixes.  The DSN and Commercial prefixes are stored as strings.  

Example response:  
```
{
    "comm": [{
        "0611-143-546": "546"
    }, {
        "0611-143-523": "523"
    }, {
        "0611-143-552": "552"
    }, 
    ...]
} 
```

- '/prefixes/comm/<comm_prefix>' - returns a an array of Commercial prefix dictionaries.  Allows partial number matching and returns an array of matches.   

Example response for '/prefixes/comm/6371 47':  
```
{
    "prefix_list": [{
        "comm_prefix": "+49 6371 47", 
        "description": "", 
        "dsn_prefix": "480", 
        "id": 37, 
        "location": "Ramstein", 
        "location_id": 16
    },
    ...]
}
```

The following Endpoints require a login
### LOGIN Endpoints

- '/login' - local login to retrieve a jwt from Auth0 to modify the database

- '/logout' - The users's session is cleared and returned back to '/'


### POST Endpoints

- '/locations' - Use this endpoint to add a new location. 

Example body: 
```
{ 
    "name": "Naval Station Rota" 
}   
```

Example response:  
```
{ 
    "success": True, 
    "name": "Naval Station Rota"  
}
```
- '/prefixes' - Use this endpoint to add a new DSN prefix. Only the location_id is an integer.  All prefixes are stored as strings.  

Example body: 
```
{ 
    "dsn_prefix": "570", 
    "comm_prefix": "+49 6119 744", 
    "description": "Germany", 
    "location_id": 20
}  
```

Example response: 
``` 
{  
    "success": True, 
    "dsns": { 
        "comm_prefix": "+49 6119 744", 
        "description": "Germany", 
        "comm_prefix": "+49 6119 744", 
        "dsn_prefix": "570", 
        "location": "Mainz/Kastel",
        "location_id": 20
    }
}
```

### PATCH Endpoints

- '/locations/<int:location_id>' - Submit a JSON object to update the name of the location. 

Example body: 
```
{ 
    "name": "Naval Station Rota" 
}  
```

Example response:  
```
{ 
    "success": True, 
    "name": "Naval Station Rota"  
}
```

- '/prefixes/<int:prefix_id>' - Submit a JSON object to update information for a prefix.  Ensure the location_id associated with the prefix is a valid location id. Only the location_id is an integer.  Both the DSN and Commercial prefixes are stored as Strings.  

Example body: 
```
{ 
    "dsn_prefix": "570", 
    "comm_prefix": "+49 6119 744", 
    "description": "Germany", 
    "location_id": 20
}  
```

Example response:  
```
{  
    "success": True, 
    "prefix_list": { 
        "comm_prefix": "+49 6119 744", 
        "description": "Germany", 
        "dsn_prefix": "570", 
        "location_id": 20
    }
}
```

### DELETE Endpoints

- '/locations/<int:location_id>' - Delete a location by submitting a valid location_id to the endpoint. 

Example response:  
```
{ 
    "success": True, 
    "location": {
        "id": 1, 
        "name": "Baumholder"
    }
}
```

- '/prefixes/<int:prefix_id>' - Delete a prefix by submitting a valid prefix_id to the endpoint. 

Example response:  
```
{ 
    "success": True, 
    "prefix": {
        "comm_prefix": "0611-143-523", 
        "description": "", 
        "dsn_prefix": "523", 
        "id": 30, 
        "location": "Mainz/Kastel", 
        "location_id": 13
    }
} 
```

### Error Handling

This API provides basic error responses. 

- Error 400: Bad request. There is an error in the data submitted to the endpoint. 
- Error 401: Permissions error. This endpoint requires the proper Authorization header. 
- Error 404: Resource not found. The requested endpoint, page or data from the database was not found.
- Error 405: Method not allowed.  The method submitted to the endpoint is not supported.
- Error 500: Server error.  An error occured on the server when attempting to process your request. 