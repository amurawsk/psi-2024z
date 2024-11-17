docker build -t pserver .
docker run -it --network-alias pserver --hostname pserver --network z39_network --name pserver pserver 8001
