# recherche-data-gouv-fr

## Getting started

Start the elasticsearch and the kafka consumer:
```
docker-compose up
```

Install the python dependencies
```
pip install -r requirements.pip
```

Seed the db with datagouv catalog:
```
flask seed-db
```

Then start the client server:
```
flask run
```

Go at http://localhost:5000/ and start playing with the *Recherche*.
