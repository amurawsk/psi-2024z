docker exec z39_pclient tc qdisc add dev eth0 root netem delay 1000ms 500ms loss 50%
