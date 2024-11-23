touch docs/client.log
touch docs/server.log
docker logs pclient > docs/client.log
docker logs pserver > docs/server.log
