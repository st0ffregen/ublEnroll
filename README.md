# ublEnroll
* Use this script to automatically reserve a seat in the Leipzig University Library.
* It's best used on a daily basis to reserve a seat for the day in seven days. If you are on unix, crontab is a good choice.  
* 

## Requirements
It's possible to run the script as a docker container or not. For the first option you'll need docker. Else you'll need python>=3.7.

## Environment Variables
To fill the ```.env``` file checkout out the following endpoints to get the possible libraries and times.
* To get all libraries: ```https://seats.ub.uni-leipzig.de/api/booking/institutions```
* To get seating areas (example: Campus Bibliothek): ```https://seats.ub.uni-leipzig.de/api/booking/areas?institution=Campus-Bibliothek```
* To get possible timeslots (example: Campus Bibliothek): ```https://seats.ub.uni-leipzig.de/api/booking/timeslots?institution=Campus-Bibliothek```
* You can choose from the fitting options, that are displayed under ```https://seats.ub.uni-leipzig.de/```
  * Now those are: "no selection", "mit Strom", "PC", "kein PC", "LAN", "Steharbeitsplatz"
  * The options are exclusive. You can not select a seat with power and lan (don't ask why...)
    
## Build and Deployment with docker
```
cp .env.example .env
docker build -t ubl-enroll-bot ./bot
docker run -it -v "$(pwd)/bot:/usr/src/app" --rm --env-file .env --name ubl-enroll-bot-running ubl-enroll-bot
```