# ublEnroll

Use this script to automatically reserve a seat in the Leipzig University Library.

## Requirements
* docker


## Environment Variables
To fill the ```.env``` File checkout out the following endpoints to get the possible libraries and times.
* To get all libraries: ```https://seats.ub.uni-leipzig.de/api/booking/institutions```
* To get seating areas (example: Campus Bibliothek): ```https://seats.ub.uni-leipzig.de/api/booking/areas?institution=Campus-Bibliothek```
* To get possible timeslots (example: Campus Bibliothek): ```https://seats.ub.uni-leipzig.de/api/booking/timeslots?institution=Campus-Bibliothek```
* You can choose from the fitting options, that are displayed under ```https://seats.ub.uni-leipzig.de/```

# Build
```
docker build -t ubl-enroll-bot ./bot
```

# Staging & Deployment
```
cp .env.example .env
docker run -it -v "$(pwd)/bot:/usr/src/app" --rm --env-file .env --name ubl-enroll-bot-running ubl-enroll-bot
```