# Clean Build Docker

```shell
docker-compose build --force-rm
```

*Note: You might need to add sudo before docker*

# Start Host and Worker (# of worker 3) docker

```shell
docker-compose up --scale worker=3
```

# Login to host docker container

```shell
docker exec -it pdkmeans_host_1 bash
```

# Submit new job to host (k e path)

```shell
python3 submit.py 3 0 data/500_Person_Gender_Height_Weight_Index.csv
```

# Copy output plot to local

```shell
docker cp pdkmeans_host_1:/opt/app/output.png .
```
