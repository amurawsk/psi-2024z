docker build -t cserver .
docker run -it --network-alias cserver --hostname cserver --network cs_network --name cserver cserver ./udp_server cserver 8001