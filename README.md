# s3-dam
Digital Asset Manager

[![Build Status](https://travis-ci.com/S3Infosoft/s3-dam.svg?branch=master)](https://travis-ci.com/S3Infosoft/s3-dam)
![autoblack_push](https://github.com/S3Infosoft/s3-dam/workflows/autoblack_push/badge.svg)

#### Initial Steps
- Go to the project directory
  ```
  cd s3-dam
  ```
- Build the Docker image
  ```
  docker build .
  ```
- Build the Docker image using docker-compose
  ```
  docker-compose build
  ```
- Migrate the models to database
  ```
  docker-compose run --rm app sh -c 'python manage.py makemigrations'
  docker-compose run --rm app sh -c 'python manage.py migrate'
  ```


#### To run the server
-   ```
    docker-compose up
    ```
#### To create a superuser
- ```
  docker-compose run --rm app sh -c 'python manage.py createsuperuser'
  ```
- Login to admin page
  <http://localhost:8000/admin/>


#### To run the tests
- ```
  docker-compose run --rm app sh -c 'python manage.py test'
  ```

