# Warehouse

## Setup

For local environment you may want to use virtualenv

    virtualenv -p python3.5 env
    
### Pushing a new base image

    docker build -f docker/base/Dockerfile -t justhc/python3-graphviz-nginx-supervisor-pip .
    docker tag justhc/python3-graphviz-nginx-supervisor-pip justhc/python3-graphviz-nginx-supervisor-pip:latest
    docker push justhc/python3-graphviz-nginx-supervisor-pip
    
### Pushing a new jenkins image

    docker build -f docker/jenkins/Dockerfile -t justhc/ecs-deploy .
    docker tag justhc/ecs-deploy justhc/ecs-deploy:latest
    docker push justhc/ecs-deploy