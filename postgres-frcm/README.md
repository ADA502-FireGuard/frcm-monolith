# postgres-frcm
FireRisk PostgreSQL DB in with Adminer and cron docker containers

[![asciicast](https://asciinema.org/a/Twysf3V2gQWLZXeDl7hzJLP2v.svg)](https://asciinema.org/a/Twysf3V2gQWLZXeDl7hzJLP2v)

## Access the DB
`Adminer` is set up to be accessible at `http://localhost:8888`. The PostgreSQL, Adminer and cron container's networks are bridged, so to access the DB from Adminer you will need to use the DB container name. The container name should be `postgres-frcm_postgres_1`, but you can also find it through `docker ps`. 

Direct access from host to PostgreSQL DB is `localhost:5432`. You can use clients like `psql` or `DBeaver` for this. 

`psql -h localhost -d fireriskdb -U admin` or `-U firerisk`