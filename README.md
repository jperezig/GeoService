# Pull Docker Image
```docker pull jperezig/geoservice```

# Run Mongo
 ```docker run --rm --name geoservice -p 5000:5000 -p 27017:27017 jperezig/geoservice```

# Run GeoService tests
 ```docker exec geoservice python3 -m unittest -v```

# Run Data Ingester
 ```docker exec  geoservice python3 /root/geoservice.py ingester /root/geoservice.conf /root/bigcsv.csv -v```

# Run Endpoint 
 ```docker exec -it geoservice python3  /root/geoservice.py endpoint /root/geoservice.conf -v```

 # Run Query
 ```curl -v -X POST -H "Content-Type: application/json" -d '{"x":460795, "y":115292, "max_distance":10000, "attributes": ["attribute1","attribute2","attribute3"]}' localhost:5000/search```
