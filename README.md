# crimantic
Crimantic is a website application which provides the statistical information of crimeIts collect infromation from different resources and then perfrom natural language processing on it to store it in to semmantic database. Then this system will answer the user queries anout crimes.
This system is written in python and the required libraries required to run the system can be seen from requirement.txt


Make sure [Neo4j](http://neo4j.com/download/other-releases/) is running first!

*If you're on Neo4j >= 2.2, make sure to set environment variables `NEO4J_USERNAME` and `NEO4J_PASSWORD`
to your username and password, respectively:*

set NEO4J_USERNAME=username
set NEO4J_PASSWORD=password


Or, set `dbms.security.auth_enabled=false` in `conf/neo4j-server.properties`.

Then:
open cmd in the downloaded folder
pip install -r requirements.txt
set FLASK_APP=Flask_Blog.py
flask run
```

[http://localhost:5000](http://localhost:5000)
