docker build -t cclient .
docker run -it --network cs_network --name cclient cclient ./udp_client cserver 8001