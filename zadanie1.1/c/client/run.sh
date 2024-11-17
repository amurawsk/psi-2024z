docker build -t cclient .
docker run -it --network z39_network --name cclient cclient ./udp_client cserver 8001
