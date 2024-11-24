touch docs/client.log
touch docs/server.log
docker logs z39_pclient > docs/client.log
docker logs z39_pserver > docs/server.log
