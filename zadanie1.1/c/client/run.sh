docker build -t cclient .
docker run -it --network cs_network --name cclient cclient ./udp_client 172.23.0.2 8001