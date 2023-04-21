# Destroy all docker containers!!!
#
# Stop all containers
docker kill $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all docker images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)
