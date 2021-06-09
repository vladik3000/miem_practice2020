#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"my_login\",\"work\":\"work2\", \"git\": \"https://github.com/vladik3000/testlab.git\"}" http://localhost:8080
