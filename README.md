# Weather-Advisor
Weather Advisor using Open Meteo APIs

## Features
- Search weather by city or town name
- Covert location names into coordinates via Open Meteo Geocoding API
- Cache previously queried city coordinates locally in locations_cache.json
- Fetch real time weather metrices such as temp, apparent temp, humidity, wind speed, precipitation, WMO condition code via Open Meteo Weather API
- Condition based advice for outdoor activities

## Issues
- [x] **Task 1: Project setup**
  - Set up local branch to start working on the lab
- [x] **Task 2: Handling Geocoding API**
  - Steps
    - 1: Send a GET request to Open Meteo geocoding API endpoint with a valid city/town name
    - 2: Validate the API response
    - 3: If multiples found, allow the user to pick out the correct location
    - 4: Get Coordiantes for the city/town name
  - Challenges: I had an issue where querying a city/town name returned multiple locations across different states, which wasn't handled in the original Lab 3 report.
  - Solution: Updated the query to request up to 5 results and added a selection prompt so the user can pick their exact location.
- [x] **Task 3: Persistent JSON Cache**
  - Steps
    - Check whether the locations_cache.json exists, if not create
    - If found, load in cache to check against user input for city/town
    - If not found, Call get_location_coordinates() and then save results to cache 
  - Challenges: I had an issue where loading empty locations_cache.json caused an error
  - Solutions: I added an exception handler that return empty dictonary
- [ ] **Task 4: Handling Weather API**
  - Send a Get Request to Open Meteo weather API endpoint with parameters of temperature, relative humidity, apparent temperature, precipitation, wind speed, and weather code. 
  - Parse the API response
- [ ] **Task 5: Condition based advice**
