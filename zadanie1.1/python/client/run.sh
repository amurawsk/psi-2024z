docker build -t pclient .
docker run -it --network z39_network --name pclient pclient pserver 8001
