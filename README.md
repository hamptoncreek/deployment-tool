# Warehouse

## Setup

For local environment you may want to use virtualenv

    virtualenv -p python3.5 env
    
### Pushing a new jenkins image

    docker build -f Dockerfile -t justhc/ecs-deploy .
    docker tag justhc/ecs-deploy justhc/ecs-deploy:latest
    docker push justhc/ecs-deploy