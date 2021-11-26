# Django Backend technical challenge for Cumplo

You can check the values of the USD, UDIS and TIIE's along the time. 
you can check it out in http://xshaffter.pythonanywhere.com/

#### Set it up in local for development.
1. Go to the project base folder.
2. Run docker-compose up --build
3. It's working now

#### Set it up in production.
1. Go to the project base folder.
2. You've got to export COMPOSE_FILE as production.yml 
 in your envionment. (export COMPOSE_FILE=production.yml)
3. Configure .env file (check .env_example) with your db, postgres and django credentials.
4. If you wanted to use a dockerized db you can create it with
 db container.
5. Run docker-compose up --build -d
6. Run docker-compose exec app pythom manage.py migrate

##### Django arquitecture.
- config/: Django configuration, with settings and wsgi and awsgi interfaces.
- api/: api application with views and serializers.
- cat/: Django catalogues (models) and home function.
- templates/: Templates with Django templates.

##### Another files.
- docker-compose.yml: Default docker conf for local.
- production.yml: Docker configuration for production.
- compose/: Docker images and compose files.