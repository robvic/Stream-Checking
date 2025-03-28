docker run -d -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" -p 9200:9200 docker.elastic.co/elasticsearch/elasticsearch:8.12.0
