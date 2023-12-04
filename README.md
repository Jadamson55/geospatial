# Mockup, small scale, geospatial data engineering project

## Project description
geospatial data is collected from a diverse source (FTP, API, etc.) and stored in a database.
The data is then processed and analyzed to produce a report.
The report is then sent to a client via email.

## Project structure
├── README.md
├── ftp_sftp
│   ├── main.py
│   ├── requirements.txt
├── geospatial
│   ├── main.py
│   ├── requirements.txt
├── data
│   ├── 2019-01-02.csv
│   ├── 2019-01-03.csv
├── docker-compose.yml   
├── Dockerfile
├── Makefile

## Project dependencies
- Python 3.7
- Docker
- Docker-compose

## Project setup
Cloud functions deployed as microservices (can scale up and down as needed)
can be used to collect data from FTP, API, etc.
data is stored in a database (SQL, NoSQL, etc.)
data is processed and analyzed (spark, hadoop, etc.)
data is sent to a client via email (sendgrid, etc.)

Cloud functions can be triggered by a scheduler (cron, etc.) or by an event (pub/sub, etc.)

## Run the project
Makefile, docker-compose, etc.

## Project testing
deploy shell from Makefile command

```
make shell
```

```
cd src
cd geospatial
python main.py
```

## Project deployment
work up to dev, staging, prod
create a docker image and push to a registry
deploy to a kubernetes cluster
use a cloud provider like GCP, AWS, etc.
for inesive queries or data operations, develop microservices and deploy to a serverless environment
That way spark, hadoop, etc. can be used to process the data (cloud dataproc, etc.) if needed

## Project logging
cloud logging (stackdriver, etc.)

## Project alerting
slack integrations, email, etc.
