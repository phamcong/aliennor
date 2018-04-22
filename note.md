### POSTGRESQL
```
PGPASSWORD=mypassword pg_dump -Fc --no-acl --no-owner -h localhost -U myuser mydb mydb.dump
```

### HEROKU
#### Common commands
 
```
heroku ps # see all services running
heroku ps:stop run.xxxx (or web.x) # stop a service
heroku run bash # enter to bash mode (check current direct, etc.)
```

#### Restore exported database into local database

```
pg_restore -d local_db db.dump # assume that local_db was created before
```

+ After restoring the database, if the migration is denied, privileges need to be granted to user in SCHEMA public of local_db
([link](https://stackoverflow.com/questions/12233046/django-permission-denied-when-trying-to-access-database-after-restore-migratio/12236582)):

```
sudo -u postgres psql database -c "GRANT ALL ON ALL TABLES IN SCHEMA public to user;"
sudo -u postgres psql database -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to user;"
sudo -u postgres psql database -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to user;"
``` 
