docker build -t pclient .
docker run -it --network cs_network --name pclient pclient pserver 8001
