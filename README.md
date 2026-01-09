# Airflow-docker setup on Mac os

# docker installation

mkdir airflow-docker
cd airflow-docker
# To install docker

brew --version
# version shows up you are good to go 
# if not

# run this

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# now check for 

brew --version

# you’ll see something like

Homebrew 5.0.9

# to install docker run

brew install --cask docker

# Now check for docker version 

docker —version

# It would not show, it would still say, docker not found. Then do

open -a Docker 

# login and give necessary permissions 

# then do the following

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Create required folders:

mkdir dags logs plugins


# Create .env file (important for permissions):

echo -e "AIRFLOW_UID=$(id -u)" > .env 

Initialize and Start Airflow

docker-compose up airflow-init

docker-compose up  -d

#Open localhost 8080

http://localhost:8080

# Here is something more to do

# clone this repo into your Github

git clone <url> docker-airflow

# Connect your github to your docker

git pull origin main

# It will ask you to login

# File structure I used

airflow-docker/
├── docker-compose.yaml
├── docker-airflow/
│   └── docker-airflow/
│       └── dags/
│           └── hello_dag.py


# Then make sure you point dags in the repo to airflow dags

#before that

x-airflow-common:
  &airflow-common
  # In order to add custom dependencies or upgrade provider distributions you can use your extended image.
  # Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
  # and uncomment the "build" line below, Then run `docker-compose build` to build the images.
  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:3.1.5}
  # build: .
  env_file:
    - ${ENV_FILE_PATH:-.env}
  environment:
    &airflow-common-env
    AIRFLOW__CORE__LOAD_EXAMPLES: 'False'

# Set the higlighted variable to False in your docker-compose.yaml, this ensures you do not see the exampl dags in your airflow

# Then 

  volumes:
  - ./docker-airflow/docker-airflow/dags:/opt/airflow/dags
  - ./logs:/opt/airflow/logs
  - ./config:/opt/airflow/config
  - ./plugins:/opt/airflow/plugins

# make sure the higlighted line points to the dags in your folder structure

# Then restart your airflow

docker-compose down -v
docker-compose up airflow-init
docker-compose up -d

# To stop airflow

docker-compose down

