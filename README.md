# about

docker containers, images, layers sum size as well as container size by name and containers discovery in zabbix format

# examples

## discovery
```
$ ./docker_df.py -D
{"data": [{"{#DOCKER_CONTAINER}": "zabbix-proxy-01"}]}
```

## containers sum size
```
$ ./docker_df.py -sc
276044870
```

## layers sum size
```
$ ./docker_df.py -sl
1206685062
```

## images sum size
```
$ ./docker_df.py -si
1391919482
```

## one container size
```
$ ./docker_df.py -c zabbix-proxy-01
8358087
```
