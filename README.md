# VoteProject

###"Active Citizen" voting monitoring service

Use docker compose in the project directory to start the service.
```
docker-compose up
```

Then, when all services are running and all migrations have been made, create a user.
```
docker-compose exec web bash
python manage.py createsuperuser
```
After that, you will be able to view the votes at the localhost:8000 address
