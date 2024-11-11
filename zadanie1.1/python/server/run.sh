docker build -t pserver .
docker run -it --network-alias pserver --hostname pserver --network cs_network --name pserver pserver 8001
