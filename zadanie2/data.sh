touch docs/example/client.log
touch docs/example/server.log
docker logs z39_cclient > docs/example/client.log
docker logs z39_pserver > docs/example/server.log